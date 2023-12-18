import PySimpleGUI as sg
import os

# Definir el diseño de la ventana con un cuadro y una imagen
layout = [
    [sg.Text('Ejemplo de ventana con cuadro y imagen')],
    [sg.Frame(layout=[
        [sg.Image(key='-IMAGE-')],
        [sg.Button('Cargar Imagen')]
    ], title='Cuadro con Imagen')],
    [sg.Button('Salir')]
]

# Crear la ventana
window = sg.Window('Ejemplo de Ventana con Imagen', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Salir':
        break
    elif event == 'Cargar Imagen':
        # Seleccionar la imagen mediante un cuadro de diálogo
        image_path = sg.popup_get_file('Selecciona una imagen', file_types=(('Archivos de imagen', '*.png;*.jpg'),))
        if image_path:
            try:
                # Verificar si la ruta de la imagen es válida
                if os.path.exists(image_path):
                    window['-IMAGE-'].update(filename=image_path)
                else:
                    sg.popup_error('Error: La ruta de la imagen no es válida.')
            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')

# Cerrar la ventana al finalizar
window.close()
