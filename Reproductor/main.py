import sys
import os
import random
import graphviz
from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QStatusBar, QTabWidget,
                             QWidget, QHBoxLayout, QVBoxLayout, QDockWidget, QListWidget, QFileDialog,
                             QListWidgetItem)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, Qt, QStandardPaths
from PyQt6.QtGui import QPixmap, QIcon, QAction, QKeySequence, QImageReader
from generar_reporte import * #ulimas modificaciones

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.current_music_folder = ""
        with open('estilos.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
        self.player = None
        self.playing_reproductor = False
        # Prueba para informacion de las canciones
        self.canciones_info = {}
        self.connect_signals()
        
        
    def initialize_ui(self):
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle("Reproductor de música")
        self.generate_main_window()
        self.create_dock()
        self.create_action()
        self.create_menu()
        self.show()
        
    # Agregando las clases nuevas de la info
    def connect_signals(self):
        self.songs_list.itemClicked.connect(self.song_selected)
        
    def song_selected(self, item):
        selected_song = item.text()
        self.show_song_info(selected_song)
        
    def generate_main_window(self):
        tab_bar = QTabWidget(self)
        self.reproductor_container = QWidget()
        self.settings_container = QWidget()
        tab_bar.addTab(self.reproductor_container, "Reproductor")
        tab_bar.addTab(self.settings_container, "Reportes")
        
        self.generate_reproductor_tab()
        self.generate_settings_tab()
        
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        
        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)
        
    def generate_reproductor_tab(self):
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()
        
        song_image = QLabel()
        pixmap = QPixmap("recursos/imagenes/iconoMusica01.png").scaled(500, 500)  
        song_image.setPixmap(pixmap)
        song_image.setScaledContents(True)
        
        button_quitar_cancion = QPushButton()
        button_quitar_cancion.setObjectName('button_quitar_cancion')
        button_quitar_cancion.clicked.connect(self.remove_selected_song)
        button_repeat = QPushButton()
        button_repeat.setObjectName('button_repeat')
        button_repeat.clicked.connect(self.repeat_song)
        button_before = QPushButton()
        button_before.setObjectName('button_before')
        self.button_play = QPushButton()
        button_before.clicked.connect(self.play_previous_song)
        self.button_play.setObjectName('button_play')
        self.button_play.clicked.connect(self.play_pause_song)
        button_next = QPushButton()
        button_next.setObjectName('button_next')
        button_next.clicked.connect(self.play_next_song)
        button_random = QPushButton()
        button_random.setObjectName('button_random')
        button_random.clicked.connect(self.play_random_song)
        button_favoritos = QPushButton()
        button_favoritos.setObjectName('button_favoritos')
        button_quitar_cancion.setFixedSize(40, 40)
        button_repeat.setFixedSize(40, 40)
        button_before.setFixedSize(40, 40)
        self.button_play.setFixedSize(50, 50)
        button_next.setFixedSize(40, 40)
        button_random.setFixedSize(40, 40)
        button_favoritos.setFixedSize(40, 40)
        buttons_h_box.addWidget(button_quitar_cancion)
        buttons_h_box.addWidget(button_repeat)
        buttons_h_box.addWidget(button_before)
        buttons_h_box.addWidget(self.button_play)
        buttons_h_box.addWidget(button_next)
        buttons_h_box.addWidget(button_random)
        buttons_h_box.addWidget(button_favoritos)
        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)
        
        main_v_box.addWidget(song_image)
        main_v_box.addWidget(buttons_container)
        
        self.reproductor_container.setLayout(main_v_box)
        
    def generate_settings_tab(self):
        main_v_box = QVBoxLayout()
    
        button_generate_html_report = QPushButton("Generar Reporte HTML")
        button_generate_html_report.clicked.connect(self.generate_html_report)
    
        button_generate_graphviz_report = QPushButton("Generar Reporte Graphviz")
        button_generate_graphviz_report.clicked.connect(self.generate_graphviz_report)
    
        main_v_box.addWidget(button_generate_html_report)
        main_v_box.addWidget(button_generate_graphviz_report)


        self.settings_container.setLayout(main_v_box)
        
        button_generate_html_report.clicked.connect(self.generate_html_report)
        button_generate_graphviz_report.clicked.connect(self.generate_graphviz_report)
    
    def create_action(self):
        self.listar_musica_action = QAction('Listar musica', self, checkable=True)
        self.listar_musica_action.setShortcut(QKeySequence("Ctrl+L"))
        self.listar_musica_action.setStatusTip("Aqui puede listar o no la música a reproducir")
        self.listar_musica_action.triggered.connect(self.list_music)
        self.listar_musica_action.setChecked(True)
        
        self.listar_musica_favorita_action = QAction('Listar musica', self, checkable=True)
        self.listar_musica_favorita_action.setShortcut(QKeySequence("Ctrl+F"))
        self.listar_musica_favorita_action.setStatusTip("Aqui van sus canciones favoritas")
        self.listar_musica_favorita_action.triggered.connect(self.list_music)
        self.listar_musica_favorita_action.setChecked(True)
        
        self.open_xml_file_action = QAction('Abrir Archivo XML', self)
        self.open_xml_file_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_xml_file_action.setStatusTip("Abrir archivo XML")
        self.open_xml_file_action.triggered.connect(self.open_xml_file)
    
    def create_menu(self):
        self.menuBar()
        
        menu_file = self.menuBar().addMenu("Archivo")
        menu_file.addAction(self.open_xml_file_action)
        
        menu_view = self.menuBar().addMenu("Listas")
        menu_view.addAction(self.listar_musica_action)
        menu_view.addAction(self.listar_musica_favorita_action)
        
    def create_dock(self):
        
        self.song_info_label = QLabel("Información de la canción:")
        self.song_label = QLabel("Canción:")
        self.artist_label = QLabel("Artista:")
        self.album_label = QLabel("Album:")
        #-------------------------------
        self.songs_list = QListWidget()
        self.dock = QDockWidget()
        self.dock.setWindowTitle("Lista de canciones")
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | 
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        
        #-----------------------------------
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
        
        
        self.songs_list.itemSelectionChanged.connect(self.handle_song_selection)
        self.dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
    
    # Nueva funcion para ver la informacion de la lista
    def show_song_info(self, selected_song):
        song_info = self.canciones_info.get(selected_song)

        if song_info:
            self.song_label.setText(f'Canción: {selected_song}')
            self.artist_label.setText(f'Artista: {song_info["artista"]}')
            self.album_label.setText(f'Álbum: {song_info["album"]}')
    
    def list_music(self):
        if self.listar_musica_action.isChecked():
            self.dock.show()
        else:
            self.dock.hide()
            
    def open_xml_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos XML (*.xml)")
        file_dialog.setWindowTitle("Seleccionar archivo XML")
        file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar archivo XML", "", "Archivos XML (*.xml)")

        if file_path:
            self.process_xml(file_path)
        #
        # 
        # generar reporte Graphviz  
        
        # listaCanciones = MainWindow()
        # listaCanciones = listaCanciones.retonarLista()
        # generar_grafo(listaCanciones, "reporteGrap.dot")

        # 
        #     

    def process_xml(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            icon = QIcon("recursos/imagenes/iconoPlay.png")

            for cancion_element in root.findall(".//cancion"):
                nombre = cancion_element.attrib.get("nombre", "")
                artista = cancion_element.find("artista").text
                album = cancion_element.find("album").text
                imagen = cancion_element.find("imagen").text
                ruta = cancion_element.find("ruta").text

                artista = artista if artista is not None else "Desconocido"
                album = album if album is not None else "Desconocido"
                ruta = ruta if ruta is not None else ""
                #nueva_cancion = Cancion(nombre, artista, album, imagen, ruta) # ERRORES 
                #self.lista_canciones.agregar_cancion(nueva_cancion) # ERRORES
                self.canciones_info[nombre] = {'artista': artista, 'album': album, 'ruta': ruta}
                item = QListWidgetItem(nombre)
                item.setIcon(icon)
                self.songs_list.addItem(item)

        except ET.ParseError as e:
            print(f"Error al analizar el archivo XML: {e}")

    def create_player(self):
        if self.player:
            self.player.deleteLater()
        self.player = QMediaPlayer()
        self.audioOutpot = QAudioOutput()
        self.player.setAudioOutput(self.audioOutpot)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.audioOutpot.setVolume(1.0)
        
        
    def play_pause_song(self):
        if self.player is not None:
            if self.playing_reproductor:
                self.button_play.setStyleSheet("image: url(recursos/imagenes/botonPausa.png);")
                self.player.pause()
                self.playing_reproductor = False
            else:
                self.button_play.setStyleSheet("image: url(recursos/imagenes/iconoPlay.png);")
                self.player.play()
                self.playing_reproductor = True
        else:
            print("No se ha cargado ninguna canción. Seleccione una canción antes de reproducir.")

    def play_previous_song(self):
        if self.songs_list.count() > 0:
            current_row = self.songs_list.currentRow()
            previous_row = (current_row - 1) % self.songs_list.count()
            self.songs_list.setCurrentRow(previous_row)
            self.handle_song_selection()
    
    def play_next_song(self):
        if self.songs_list.count() > 0:
            current_row = self.songs_list.currentRow()
            next_row = (current_row + 1) % self.songs_list.count()
            self.songs_list.setCurrentRow(next_row)
            self.handle_song_selection()
            
    def repeat_song(self):
        if self.player is not None:
            self.player.setPosition(0)  
            if self.playing_reproductor:
                self.player.play()
                
    def play_random_song(self):
        if self.songs_list.count() > 0:
            random_row = random.randint(0, self.songs_list.count() - 1)
            self.songs_list.setCurrentRow(random_row)
            self.handle_song_selection()

        
    def remove_selected_song(self):
        selected_item = self.songs_list.currentItem()
        if selected_item:
            row = self.songs_list.currentRow()
            self.songs_list.takeItem(row)
    
    
    def generate_html_report(self):
        pass

    def generate_graphviz_report(self):
        pass
    def media_status_changed(self, status):
        print('status', status)
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()
                
    def handle_song_selection(self):
        selected_item = self.songs_list.currentItem()
        if selected_item:
            song_name = selected_item.data(0)
            song_folder_path = os.path.join( self.current_music_folder, song_name)
            self.create_player()
            source = QUrl.fromLocalFile(song_folder_path)
            self.player.setSource(source)
            self.playing_reproductor = True
            
        
        
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
