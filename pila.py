


class PilaContenedores:
    def __init__(self, id_pila, posicion, posicion_descarga):
        self.id = id_pila
        self.pila = [] 
        self.posicion = posicion
        self.posicion_descarga = posicion_descarga

    def add_contenedor(self, contenedor):
        self.pila.append(contenedor)