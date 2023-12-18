import sys
import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, \
    QDockWidget, QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QPixmap, QAction, QKeySequence


class NodoCancion:
    def __init__(self, nombre, artista, album, ruta):
        self.nombre = nombre
        self.artista = artista
        self.album = album
        self.ruta = ruta
        self.siguiente = None
        self.anterior = None

class ListaCanciones:
    def __init__(self):
        self.inicio = None
        self.actual = None

    def agregar_cancion(self, nombre, artista, album, ruta):
        nueva_cancion = NodoCancion(nombre, artista, album, ruta)
        if not self.inicio:
            self.inicio = nueva_cancion
            self.actual = nueva_cancion
            nueva_cancion.siguiente = nueva_cancion
            nueva_cancion.anterior = nueva_cancion
        else:
            nueva_cancion.siguiente = self.inicio
            nueva_cancion.anterior = self.actual
            self.actual.siguiente = nueva_cancion
            self.inicio.anterior = nueva_cancion
            self.actual = nueva_cancion

    def obtener_cancion_actual(self):
        return self.actual

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.barra_estado = self.statusBar()
        self.current_music_folder = ""
        self.player = None
        self.canciones_info = {}
        self.canciones_infoNodo = {}
        self.lista_canciones = ListaCanciones()
        self.connect_signals()

    def initialize_ui(self):
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle("IPC Music")
        self.generate_window()
        self.bar_list()
        self.control_music()
        self.create_menu()
        self.show()

    def connect_signals(self):
        self.songs_list.itemClicked.connect(self.song_selected)

    def song_selected(self, item):
        selected_song = item.text()
        self.show_song_info(selected_song)

    def generate_window(self):
        barra = QTabWidget(self)
        self.reproductor = QWidget()
        barra.addTab(self.reproductor, "Reproductor")

        self.generate_barra_reproductor()

        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(barra)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def generate_barra_reproductor(self):
        main_i_music = QVBoxLayout()
        buttons_music = QHBoxLayout()

        imagen_music = QLabel()
        pixmap = QPixmap("/home/vicente/Documentos/pr/PruebaIPC2/proyecto_ipc_music/Proyecto_1/images/song_image.jpg").scaled(512, 512)
        imagen_music.setPixmap(pixmap)
        imagen_music.setScaledContents(True)

        self.button_repeat = QPushButton("↺")
        self.button_before = QPushButton("⏮")
        self.button_play = QPushButton("▶")
        self.button_next = QPushButton("⏭")
        self.button_random = QPushButton("🔀")

        buttons_music.addWidget(self.button_repeat)
        buttons_music.addWidget(self.button_before)
        buttons_music.addWidget(self.button_play)
        buttons_music.addWidget(self.button_next)
        buttons_music.addWidget(self.button_random)
        buttons_container = QWidget()
        buttons_container.setLayout(buttons_music)

        main_i_music.addWidget(imagen_music)
        main_i_music.addWidget(buttons_container)

        self.reproductor.setLayout(main_i_music)

    def control_music(self):
        self.barra_music = QAction('Listar musica', self, checkable=True)
        self.barra_music.setShortcut(QKeySequence("Ctrl+L"))
        self.barra_music.setStatusTip("Aqui puedes listar o no la musica a reproducir")
        self.barra_music.triggered.connect(self.list_music)
        self.barra_music.setChecked(True)

        self.open_folder_music = QAction('Abrir Carpeta', self)
        self.open_folder_music.setShortcut(QKeySequence("Ctrl+O"))
        self.open_folder_music.setStatusTip("Abre tu carpeta de musica")
        self.open_folder_music.triggered.connect(self.open_folder)

        self.open_graphiz = QAction('Abrir Graphiz', self)
        self.open_graphiz.setShortcut(QKeySequence("Ctrl+G"))
        self.open_graphiz.setStatusTip("Abre la lista de Graphiz")
        self.open_graphiz.triggered.connect(self.L_graphiz)

        self.button_before.clicked.connect(self.button_before_clicked)
        self.button_play.clicked.connect(self.button_play_clicked)
        self.button_next.clicked.connect(self.button_next_clicked)

    def create_menu(self):
        menu_file = self.menuBar().addMenu("Abrir")
        menu_file.addAction(self.open_folder_music)
        menu_view = self.menuBar().addMenu("Vista")
        menu_view.addAction(self.barra_music)
        menu_view = self.menuBar().addMenu("Graphiz")
        menu_view.addAction(self.open_graphiz)

    def bar_list(self):
        self.songs_list = QListWidget()

        self.song_info_label = QLabel("Información de la canción:")
        self.song_label = QLabel("Canción:")
        self.artist_label = QLabel("Artista:")
        self.album_label = QLabel("Album:")
        self.dock = QDockWidget()
        self.dock.setWindowTitle("Lista de canciones")
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea)
        self.dock.setWidget(self.songs_list)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.song_info_label)
        info_layout.addWidget(self.song_label)
        info_layout.addWidget(self.artist_label)
        info_layout.addWidget(self.album_label)

        dock_layout = QVBoxLayout()
        dock_layout.addLayout(info_layout)
        dock_layout.addWidget(self.songs_list)

        dock_widget = QWidget()
        dock_widget.setLayout(dock_layout)

        self.songs_list.itemSelectionChanged.connect(self.escuchar)
        self.dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    def read_xml_file(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for cancion_element in root.findall('cancion'):
                nombre = cancion_element.get('nombre')
                artista_element = cancion_element.find('artista')
                album_element = cancion_element.find('album')
                ruta_element = cancion_element.find('ruta')

                artista = artista_element.text if artista_element is not None else "Desconocido"
                album = album_element.text if album_element is not None else "Desconocido"
                ruta = ruta_element.text if ruta_element is not None else ""

                self.canciones_info[nombre] = {'artista': artista, 'album': album, 'ruta': ruta}
                self.canciones_infoNodo[nombre] = {'artista': artista, 'album': album, 'ruta': "\n"}
                self.lista_canciones.agregar_cancion(nombre, artista, album, ruta)
                self.songs_list.addItem(nombre)

        except ET.ParseError as e:
            print(f"Error al analizar el archivo XML: {str(e)}")

    def show_song_info(self, selected_song):
        song_info = self.canciones_info.get(selected_song)

        if song_info:
            self.song_label.setText(f'Canción: {selected_song}')
            self.artist_label.setText(f'Artista: {song_info["artista"]}')
            self.album_label.setText(f'Álbum: {song_info["album"]}')

    def open_folder(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Archivos XML (*.xml)")
        file_dialog.setWindowTitle("Selecciona un archivo XML")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.current_music_folder = file_dialog.selectedFiles()[0]
            self.read_xml_file(self.current_music_folder)

    def list_music(self):
        if self.barra_music.isChecked():
            self.dock.show()
        else:
            self.dock.hide()

    def L_graphiz(self):
        pass

    def create_player(self):
        if self.player:
            self.player.deleteLater()
        self.player = QMediaPlayer()
        self.audioutput = QAudioOutput()
        self.player.setAudioOutput(self.audioutput)
        self.player.mediaStatusChanged.connect(self.media_Status_Changed)
        self.audioutput.setVolume(1.0)

    def media_Status_Changed(self, status):
        print('status:', status)
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()
            self.actualizar_info_reproductor()

    def escuchar(self):
        selected_item = self.songs_list.currentItem()
        if selected_item:
            song_name = selected_item.text()
            current_song = self.lista_canciones.obtener_cancion_actual()
            self.show_song_info(current_song.nombre)
            self.create_player()
            source = QUrl.fromLocalFile(current_song.ruta)
            self.player.setSource(source)

    def button_before_clicked(self):
        self.lista_canciones.actual = self.lista_canciones.actual.anterior
        self.actualizar_info_reproductor()

    def button_play_clicked(self):
        if self.player.state() == QMediaPlayer.State.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def button_next_clicked(self):
        self.lista_canciones.actual = self.lista_canciones.actual.siguiente
        self.actualizar_info_reproductor()

    def toggle_repeat(self):
        pass

    def toggle_random(self):
        pass

    def actualizar_info_reproductor(self):
        current_song = self.lista_canciones.obtener_cancion_actual()
        self.show_song_info(current_song.nombre)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec())