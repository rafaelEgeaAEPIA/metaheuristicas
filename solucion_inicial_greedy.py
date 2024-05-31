import random
import copy
import numpy as np
from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from grua import Grua


def set_gruas(n_gruas, patio_contenedores, itinerarios):
    grua_fila_patio_equitativa=patio_contenedores.asignacion_gruas_pilas
    if n_gruas > patio_contenedores.shape[0]:
        return "Error en la configuracion"
    
    
    shape_patio = patio_contenedores.shape

    new_gruas = {}
    for n_grua in range(n_gruas):

        posicion_inicial = (np.nan, np.nan)
        if len(itinerarios[n_grua]) > 0:
            posicion_inicial = itinerarios[n_grua][0].pila_asignada.posicion

        fronteras =  (grua_fila_patio_equitativa[n_grua][0], grua_fila_patio_equitativa[n_grua][-1])
        grua = Grua(n_grua, (posicion_inicial[0], posicion_inicial[1]), itinerarios[n_grua], fronteras)

        new_gruas[n_grua] = grua

    return new_gruas



def buscar_grua_a_asignar(grua_fila_patio_equitativa, fila):
    grua_asignar = list(grua_fila_patio_equitativa.keys())[0]
    for grua in grua_fila_patio_equitativa:
        if fila in grua_fila_patio_equitativa[grua]:
            grua_asignar = grua
    return grua_asignar
    


def asignar_contenedores_a_gruas_gredy(patio_contenedores, gruas, seed, n_gruas):
    """Asigna contenedores a las gruas aleatoriamente."""

    random.seed(seed)
    pilas_patio = copy.deepcopy(patio_contenedores.pilas)
    contenedores_en_patio = np.sum([len(pila) for pila in pilas_patio])
    contenedores_en_espera = patio_contenedores.contenedores_en_espera.copy()
    

    # Mientas haya  contenedores en el patio y contenedores a la espera de ser cargados
    while contenedores_en_patio > 0 and len(contenedores_en_espera) > 0:
        # Elegir aleatoriamente si cargar un nuevo contenedor o descargar uno
        cargar_nuevo_contenedor = random.randint(0,1)
        descargar_contenedor = not cargar_nuevo_contenedor

        if descargar_contenedor:
            # Si elegimos descargar uno
            filas = []
            for fila in range(len(pilas_patio)):
                for pila in pilas_patio[fila]:
                    if len(pila.pila) > 0:
                        filas.append(fila)

            fila = random.choice(filas)


            pilas = [i for i in range(len(pilas_patio[fila])) if len(pilas_patio[fila][i].pila) > 0]
            tam = 5 if len(pilas) > 5 else len(pilas)

            pilas = random.sample(pilas, tam)

            grua_greedy = copy.copy(gruas)
            pila_contenedores_mejor = pilas_patio[fila][pilas[0]]
            contenedor = pila_contenedores_mejor.pila[0]

            grua_asignar=buscar_grua_a_asignar(patio_contenedores.asignacion_gruas_pilas, fila)
            contenedor.grua_asignada = grua_asignar

            grua_greedy[grua_asignar].append(contenedor)
            patio_contenedores.gruas = set_gruas(n_gruas, patio_contenedores, gruas)

            mejor_coste = evaluar_solucion(grua_greedy, patio_contenedores)


            for pila in pilas[1:]:
                grua_greedy = copy.copy(gruas)
                pila_contenedores = pilas_patio[fila][pila]
                contenedor = pila_contenedores.pila[0]
                grua_asignar=buscar_grua_a_asignar(patio_contenedores.asignacion_gruas_pilas, fila)
                contenedor.grua_asignada = grua_asignar

                patio_contenedores.gruas = set_gruas(n_gruas, patio_contenedores, gruas)

                grua_greedy[grua_asignar].append(contenedor)
                coste = evaluar_solucion(grua_greedy, patio_contenedores)

                if coste < mejor_coste:
                    pila_contenedores_mejor = pila_contenedores
                    mejor_coste = coste 

            contenedor = pila_contenedores_mejor.pila.pop(0)
            contenedores_en_patio -= 1
            
            grua_asignar=buscar_grua_a_asignar(patio_contenedores.asignacion_gruas_pilas, fila)
            contenedor.grua_asignada = grua_asignar
            gruas[grua_asignar].append(contenedor)


        if cargar_nuevo_contenedor:
            # Elegimos un contenedor aleatorio de entre todos los existentes
            contenedor = random.choice(contenedores_en_espera)
            contenedores_en_espera.remove(contenedor)

            # Extraemos la pila asignada y la fila a la que debería ir
            pila_asignada = contenedor.pila_asignada
            fila, columna = pila_asignada.posicion[0], pila_asignada.posicion[1]

            # Buscamos la grua asignada a esa fila 
            grua_asignar=buscar_grua_a_asignar(patio_contenedores.asignacion_gruas_pilas, fila)



            new_contenedor = contenedor.copy()
            new_contenedor.hay_que_cargar = False

            if len(pilas_patio[fila][columna].pila) == 0:
                contenedor.grua_asignada = grua_asignar
                pilas_patio[fila][columna].pila.append(new_contenedor)
                gruas[grua_asignar].append(contenedor)
                contenedores_en_patio += 1

            # Comprobamos que la fecha de salida del contenedor es mayor o igual a la del tope
            elif contenedor.fecha_salida >= pilas_patio[fila][columna].pila[0].fecha_salida:

                contenedor.grua_asignada = grua_asignar
              
                gruas[grua_asignar].append(contenedor)
                # Añadimos el contenedor a descargar nuevo en la pila del patio de contenedores copia
                pilas_patio[fila][columna].pila.append(new_contenedor)
                contenedores_en_patio += 1


    return gruas

