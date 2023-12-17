import os
import pygame
from tkinter import Tk, Label, Button, Frame, filedialog, Listbox, scrolledtext, Canvas
from PIL import Image, ImageTk
from graphviz import Digraph
import xml.etree.ElementTree as ET
from Song import Song
from node import Node
from DoublyLinkedList import DoublyLinkedList
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        
        self.root = root
        self.root.title("Reproductor de Música")
        self.root.geometry(f"{1065}x{636}+{100}+{50}")
        self.root.config(bg="#09223b")        #w
        
        # Inicializar Pygame
        pygame.init()

        # Variables de estado
        self.playing = False
        self.current_song = None
        self.playlist = []
        self.played_songs_list = DoublyLinkedList()  # Lista doblemente enlazada para canciones reproducidas
        self.songs = [Song("path1", "Song1"), Song("path2", "Song2"), Song("path3", "Song3")]
        self.current_song_index = 0


# ************************************************************
        backGroundInterfaz = "#0c131a"
        colorFont = "white"
        altoPanel = root.winfo_screenheight()
        anchoPanel = root.winfo_screenwidth()
        anchoPanel = anchoPanel - 583
        # Crear el panel
        panelMenu = Frame(root, bg="#041424", width="350", height=altoPanel)
        panelMenu.place(x=0, y=70)
        #botones dentro del panelMenu
        boton = Button(panelMenu, text="PlayListalgo ", font=("", "16"),
                          command=lambda num="playlist": accion_boton(num), bg="#0c131a", fg="white", width="29",
                          height="1")
        boton.place(x="0", y="0")

        boton = Button(panelMenu, text="Biblioteca ", command=lambda num="playlist": accion_boton(num),
                          font=("", "16"), width="29", height="1", bg="#0c131a", fg="white")
        boton.place(x="0", y="42")


        colorPanel = "#041424"

        def crear_bordes_redondeados(canvas, x, y, width, height, radio, colorPanel):
            # Crear bordes redondeados
            canvas.create_arc(x, y, x + 2 * radio, y + 2 * radio, start=90, extent=90, fill=colorPanel,
                              outline=colorPanel)
            canvas.create_arc(x + width - 2 * radio, y, x + width, y + 2 * radio, start=0, extent=90, fill=colorPanel,
                              outline=colorPanel)
            canvas.create_arc(x, y + height - 2 * radio, x + 2 * radio, y + height, start=180, extent=90,
                              fill=colorPanel, outline=colorPanel)
            canvas.create_arc(x + width - 2 * radio, y + height - 2 * radio, x + width, y + height, start=270,
                              extent=90, fill=colorPanel, outline=colorPanel)

            # Crear segmentos rectos
            canvas.create_rectangle(x + radio, y, x + width - radio, y + height, fill=colorPanel, outline=colorPanel)
            canvas.create_rectangle(x, y + radio, x + width, y + height - radio, fill=colorPanel, outline=colorPanel)

            # Configurar las dimensiones del panel

        ancho_panel = 700
        alto_panel = 500
        radio_bordes = 5

        # Crear el Canvas para el panel
        panelImagenArtista = Canvas(root, width=ancho_panel, height=alto_panel, bg="#09223b", highlightthickness=0)
        panelImagenArtista.place(x="360", y="70")

        panelReproduccion = Canvas(root, width=ancho_panel, height=50, bg="#09223b", highlightthickness=0)
        panelReproduccion.place(x="360", y="580")

        panel_imagenCancion = Canvas(panelImagenArtista, width=ancho_panel, height=300, bg="#041424", highlightthickness=0)
        panel_imagenCancion.place(x="9", y="150")


        # Crear bordes redondeados en el Canvas
        crear_bordes_redondeados(panelImagenArtista, 0, 0, ancho_panel, alto_panel, radio_bordes, colorPanel)
        crear_bordes_redondeados(panelReproduccion, 0, 0, ancho_panel, alto_panel, radio_bordes, colorPanel)
        crear_bordes_redondeados(panel_imagenCancion, 0, 0, 680, 300, radio_bordes, "#09223b")

        # ************************************************************

        # ************************************************************


        # Crear widgets LOGICA DEL FRONT
        self.song_info_label = Label(panelImagenArtista, text="Artista: - Álbum: - Canción: ", bg =backGroundInterfaz, fg =colorFont)
        # self.song_info_label.pack()
        self.song_info_label.place(x="10", y="450")

        self.song_image_label = Label(root)
        self.song_image_label.pack()

        self.controls_frame = Frame(root)
        self.controls_frame.pack()

        self.play_button = Button(panelReproduccion, text="▶️ Play", command=self.play_pause_toggle)
        # self.play_button.grid(row=0, column=0)
        self.play_button.place(x="10", y="11")

        self.pause_button = Button(panelReproduccion, text="⏸️ Pause", command=self.pause)
        self.pause_button.place(x="80", y="11")

        self.stop_button = Button(panelReproduccion, text="⏹️ Stop", command=self.stop)
        self.stop_button.place(x="150", y="11")

        self.prev_button = Button(panelReproduccion, text="⏮️ Prev", command=self.play_prev)
        self.prev_button.place(x="220", y="11")

        self.next_button = Button(panelReproduccion, text="⏭️ Next", command=self.play_next)
        self.next_button.place(x="300", y="11")

        self.choose_file_button = Button(root, text="Seleccionar archivo XML", command=self.load_playlist_from_xml, font = ("", "14"), bg = backGroundInterfaz, fg=colorFont, width="20", height ="2")
        self.choose_file_button.place(x="4", y="4")

        self.playlist_label = Label(panelMenu, text="Lista de Reproducción", bg="black", fg=colorFont)
        self.playlist_label.place(x="4", y="300")

        self.playlist_box = Listbox(panelMenu, selectmode="SINGLE", activestyle="none", width="56", height="10", bg="#041424", fg=colorFont)
        # self.playlist_box = Listbox(panelMenu, selectmode="SINGLE", activestyle="none")
        self.playlist_box.place(x="5.3", y="325")
        # self.playlist_box.pack()

        self.stats_button = Button(panelMenu, text="Generar Estadísticas", command=self.generate_stats)
        self.stats_button.place(x="4", y="100")

        self.played_songs_label = Button(panelImagenArtista, text="Canciones Reproducidas:", bg="#0c131a", fg = "white")
        self.played_songs_label.place(x="10", y="100")

        self.played_songs_display = scrolledtext.ScrolledText(panelImagenArtista, width=83, height=5, bg="#0c131a", fg="white")
        self.played_songs_display.place(x="10", y="10")

    def play_pause_toggle(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button["text"] = "▶️ Play"
        else:
            if not self.current_song:
                self.choose_file()
            else:
                pygame.mixer.music.unpause()
                self.play_button["text"] = "⏸️ Pause"
        self.playing = not self.playing

    def pause(self):
        pygame.mixer.music.pause()
        self.play_button["text"] = "▶️ Play"
        self.pause_button["text"] = "⏸️ Pause"
        self.playing = False

    def stop(self):
        pygame.mixer.music.stop()
        self.play_button["text"] = "▶️ Play"
        self.playing = False
#----------------------------------------------
#----------------------------------------------
#----------------------------------------------
    def play_next(self):
        if not self.playlist:
            return  # No hay canciones en la lista de reproducción

        if not self.played_songs_list.is_empty():
            # Pop the next song from the doubly linked list
            next_song = self.played_songs_list.pop()
        else:
            # If the list is empty, play the next song in the playlist
            if self.current_song:
                current_index = self.playlist.index(self.current_song)
                next_index = (current_index + 1) % len(self.playlist)
            else:
                next_index = 0

            next_song = self.playlist[next_index]

        self.load_song(next_song)

    def play_prev(self):
        if not self.played_songs_list.is_empty():
            # Pop the previous song from the doubly linked list
            prev_song = self.played_songs_list.pop()
            # Add the previous song back to the playlist
            self.playlist.insert(0, prev_song)
            self.playlist_box.insert(0, os.path.basename(prev_song))
            # Load the previous song
            self.load_song(prev_song)

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3;*.wav")])
        if file_path:
            self.playlist.insert(0, file_path)
            self.playlist_box.insert(0, os.path.basename(file_path))
            if not self.current_song:
                self.load_song(file_path)

    def load_song(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.play_button["text"] = "⏸️ Pause"
        self.playing = True

        # Agregar la canción actual a la lista doblemente enlazada de canciones reproducidas
        self.played_songs_list.append(file_path)

        # Actualizar la información de la canción actual
        self.current_song = file_path
        artist = "Artista"
        album = "Álbum"
        song_title = os.path.basename(file_path)
        self.song_info_label["text"] = f"Artista: {artist} - Álbum: {album} - Canción: {song_title}"

        # Cargar y mostrar la imagen de la canción si está disponible
        image_path = "ruta_de_imagen.jpg"  # Reemplaza con la ruta de la imagen de la canción
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.song_image_label.config(image=photo)
            self.song_image_label.image = photo

        # Actualizar la visualización de las canciones reproducidas
        self.update_played_songs_display()

    def update_played_songs_display(self):
        # Mostrar las canciones reproducidas en el widget scrolledtext
        self.played_songs_display.delete("1.0", "end")
        for i, song in enumerate(self.played_songs_list):
            self.played_songs_display.insert("end", f"{i+1}. {os.path.basename(song.file_path)} - {song.nombre}\n")


    def load_playlist_from_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if file_path:
            self.playlist = self.parse_xml_playlist(file_path)
            self.update_playlist_box()

    def parse_xml_playlist(self, file_path):
        playlist = []
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for song_element in root.findall('song'):
                file_path = song_element.find('file_path').text
                playlist.append(file_path)
        except ET.ParseError:
            print("Error al analizar el archivo XML")
        return playlist

    def update_playlist_box(self):
        self.playlist_box.delete(0, "end")
        for song_path in self.playlist:
            self.playlist_box.insert("end", os.path.basename(song_path))

#---------------------------------------------------------------------------------------------------------------
#-----------------------------------------------GENERAR ESTADISTICAS--------------------------------------------
#---------------------------------------------------------------------------------------------------------------
    def generate_stats(self):
        # Generar estadísticas utilizando Graphviz
        dot = Digraph(comment='Reproductor de Música Stats')

        # Agregar nodos para cada canción en la lista de reproducción
        for i, song_path in enumerate(self.playlist):
            dot.node(f'song_{i+1}', os.path.basename(song_path))

        # Agregar conexiones entre las canciones para representar el orden en la lista de reproducción
        for i in range(len(self.playlist) - 1):
            dot.edge(f'song_{i+1}', f'song_{i+2}', constraint='false')

        # Guardar el archivo DOT y generar el gráfico
        dot.render('music_stats', format='png', cleanup=True)
        print("Estadísticas generadas. Verifica el archivo 'music_stats.png'.")

if __name__ == "__main__":
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
