from Cancion import Cancion

class NodoDoble:
    def __init__(self, cancion):
        self.cancion = cancion
        self.siguiente = None
        self.anterior = None

class ListaDoble:
    def __init__(self):
        self.head = None
        self.tail = None

    def agregar_cancion(self, cancion):
        nuevo_nodo = NodoDoble(cancion)
        if not self.head:
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.tail
            self.tail.siguiente = nuevo_nodo
            self.tail = nuevo_nodo

    def recorrer_lista(self):
        actual = self.head
        while actual:
            print(f"Nombre: {actual.cancion.nombre}, Artista: {actual.cancion.artista}")
            actual = actual.siguiente

    def obtener_nodo_por_nombre(self, nombre):
        actual = self.head
        while actual:
            if actual.cancion.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None