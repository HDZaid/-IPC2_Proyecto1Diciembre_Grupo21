
from graphviz import Digraph    
    
def generar_grafo(canciones, nombre_archivo_dot):
    dot = Digraph(comment='Grafo de canciones en la lista')

    actual = canciones.head
    while actual:
        canciones = actual.canciones
        dot.node(canciones.nombre, f"{canciones.nombre}")
        actual = actual.tail

    # Conectar nodos en función de la lista enlazada
    actual = canciones.head
    while actual and actual.tail:
        dot.edge(actual.canciones.nombre, actual.tail.canciones.nombre)
        actual = actual.tail

    # Guardar el archivo DOT
    dot.save(nombre_archivo_dot)