"""
import PySimpleGUI as sg
sg.theme('DarkPurple1')
# Definimos los elementos graficos: Texto, inputs, botones
layout = [[sg.Text("Cual es tu nombre: ")],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Salir')]]

# Creamos la ventana con el layout definido anteriormente
window = sg.Window('Facialix', layout)

# Iniciamos la ejecucion de la ventana con ciclo While
while True:
    # Podemos leer eventos y valores de nuestra ventana
    event, values = window.read()
    # El evento por defecto para cerrar la ventana es Salir
    if event == sg.WINDOW_CLOSED or event == 'Salir':
        break
    # Es posible actualizar valores de los elementos graficos en tiempo de ejecucion.
    window['-OUTPUT-'].update('Hola ' * values['-INPUT-'])
    
    # NO olvides cerra la ventana al terminar
    window.close()
"""

import PySimpleGUI as sg

sg.theme('DarkPurple1')

# Definimos los elementos gráficos: Texto, inputs, botones
layout = [
    [sg.Text("¿Cuál es tu nombre?")],
    [sg.InputText(key='-INPUT-')],
    [sg.Text(size=(40, 1), key='-OUTPUT-')],
    [sg.Button('Ok'), sg.Button('Salir')]
]

# Creamos la ventana con el layout definido anteriormente
window = sg.Window('Facialix', layout)

# Iniciamos la ejecución de la ventana con un ciclo While
while True:
    # Podemos leer eventos y valores de nuestra ventana
    event, values = window.read()

    # El evento por defecto para cerrar la ventana es Salir
    if event == sg.WINDOW_CLOSED or event == 'Salir':
        break

    # Es posible actualizar valores de los elementos gráficos en tiempo de ejecución.
    window['-OUTPUT-'].update(f'Hola {values["-INPUT-"]}')

# NO olvides cerrar la ventana al terminar (mover la línea fuera del bucle)
window.close()
