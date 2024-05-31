class PatioContenedores:

    def __init__(self):
        self.pilas = []
        self.gruas = {}
        self._shape = (1,)
        self.contenedores_en_espera = []
        self._asignacion_gruas_pilas = None

    def set_pilas(self, pilas):
        self.pilas = pilas

    @property
    def shape(self):
        return self._shape
    
    @shape.setter
    def shape(self, value):
        self._shape = value



    @property
    def asignacion_gruas_pilas(self):
        return self._asignacion_gruas_pilas
    
    @asignacion_gruas_pilas.setter
    def asignacion_gruas_pilas(self, value):
        self._asignacion_gruas_pilas = value


    def add_grua(self, grua):
        self.gruas[grua.id_grua] = grua

    def imprimir_patio_contenedores(self):
        """
            Funcion que imprime las columnas del patio de contenedores
        """
        print(self.pilas, self.shape)

        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                for g in self.gruas:
                    if (self.gruas[g].posicion_inicial[0] == row) and (self.gruas[g].posicion_inicial[1] == col):
                        print("Grua", self.gruas[g].id_grua, self.gruas[g].posicion_inicial, end=" ")

                print(self.pilas[row][col].id, end=":")
                print([c.id_contenedor for c in self.pilas[row][col].pila], end="\t\t")
            print()

        print("Contenedores en espera")
        print([c.id_contenedor for c in self.contenedores_en_espera])