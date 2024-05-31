

class Contenedor:
    def __init__(self, id_contenedor, fecha_salida, fecha_entrada, pila_asignada, hay_que_cargar=False):
        self.id_contenedor = id_contenedor
        self.fecha_salida = fecha_salida
        self.fecha_entrada = fecha_entrada
        self.pila_asignada = pila_asignada
        self.grua_asignada = None
        self.hay_que_cargar = hay_que_cargar


    def to_str(self):
        return "ID:" + str(self.id_contenedor) + " | Pila asignada:" + str(self.pila_asignada.id_pila) + " | Fecha salida:" + str(self.fecha_salida)
    

    def get_localizacion_contenedor(self):
        return (self.pila.localizacion[0], self.pila.localizacion[1])
    
    def copy(self):
        return Contenedor(self.id_contenedor, self.fecha_salida, self.fecha_entrada, self.pila_asignada, self.hay_que_cargar)
    
