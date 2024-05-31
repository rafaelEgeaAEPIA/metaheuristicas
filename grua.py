class Grua:
    tiempo_entre_filas = 10*60000
    tiempo_entre_columnas = 5*60000

    def __init__(self, id_grua, posicion, itinerario, frontera):
        self.id_grua = id_grua
        self.posicion_inicial = posicion
        self.itinerario = itinerario
        self._posicion = posicion 
        self._frontera = frontera

    @property
    def posicion(self):
        return self._posicion 
    
    @posicion.setter
    def posicion(self, value):
        self._posicion=value


    @property
    def frontera(self):
        return self._frontera 
    
    @frontera.setter
    def frontera(self, value):
        self._frontera=value
        
        