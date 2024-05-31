import numpy as np
from pila import PilaContenedores
import random
from contenedor import Contenedor
from patio_contenedores import PatioContenedores
from grua import Grua 
from datetime import datetime, timedelta
import pandas as pd 
import math
import copy
from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from solucion_inicial_greedy import asignar_contenedores_a_gruas_gredy
def generar_fechas_aleatorias(seed):
    random.seed(seed)
    fecha_inicio = datetime.now()
    horas_aleatorias_salida = random.randint(0, 23)
    minutos_aleatorios_salida  = random.randint(0, 59)
    segundos_aleatorios_salida  = random.randint(0, 59)
    # Crear una fecha aleatoria dentro del mismo día
    fecha_salida = fecha_inicio.replace(hour=horas_aleatorias_salida, 
                                        minute=minutos_aleatorios_salida, 
                                        second=segundos_aleatorios_salida)
    

    diferencia_horas = timedelta(minutes=random.randint(50,500))

    fecha_entrada = fecha_salida - diferencia_horas
  

    return fecha_salida, fecha_entrada

def generar_patio_contenedores(n_rows, n_cols, max_contenedores_bay, seed):
    """
        Esta función genera un patio de contenedores 
        de n_rows, y n_cols columnas.
        Para cada columna se asignaran un número aleatorio de contenedores por bay
    """
    random.seed(seed)
    patio_contenedores = []

    i = 0
    j=0
    for row in range(n_rows):
        patio_contenedores.append([])        
        for col in range(n_cols):
            pila = PilaContenedores(i, (row, col), (row, n_cols))
            n_contenedores_bay = random.randint(1, max_contenedores_bay)
            for new_cont in range(n_contenedores_bay):
                fecha_salida, fecha_entrada  = generar_fechas_aleatorias(seed)
                new_contenedor = Contenedor(j, fecha_salida, fecha_entrada, pila)
                j+=1
                pila.add_contenedor(new_contenedor)
            
            pila.pila.sort(key=lambda contenedor: contenedor.fecha_salida)


            patio_contenedores[row].append(pila)

            i+=1

    n_contenedores_en_espera = random.randint(0, n_rows*n_cols*max_contenedores_bay)

    contenedores_en_espera = []
    for cont in range(n_contenedores_en_espera):
        fecha_salida, fecha_entrada  = generar_fechas_aleatorias(seed)
        pila_to_add =  random.choice(random.choice(patio_contenedores))
        new_contenedor = Contenedor(j, fecha_salida, fecha_entrada, pila_to_add, hay_que_cargar=True)
        contenedores_en_espera.append(new_contenedor)
        j+=1

    return patio_contenedores, (n_rows, n_cols), contenedores_en_espera




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








def generar_solucion_inicial(patio_contenedores, n_gruas, seed):

    # Dividir las pilas entre las grúas de manera equitativa
    grua_fila_patio_equitativa = dividir_filas_entre_gruas(patio_contenedores, n_gruas)
    patio_contenedores.asignacion_gruas_pilas = grua_fila_patio_equitativa
    # Inicializar diccionario de grúas
    gruas = inicializar_gruas(n_gruas)

    # Asignar contenedores a las grúas aleatoriamente
    #gruas = asignar_contenedores_a_gruas(patio_contenedores, gruas, seed)
    gruas = asignar_contenedores_a_gruas_gredy(copy.deepcopy(patio_contenedores), gruas, seed, n_gruas)

    # Establecer las grúas en el patio
    patio_contenedores.gruas = set_gruas(n_gruas, patio_contenedores, gruas)


    return gruas, patio_contenedores


def dividir_filas_entre_gruas(patio_contenedores, n_gruas):
    """Divide las filas del patio entre las gruas de manera equitativa."""
    elementos_por_grua = patio_contenedores.shape[0] // n_gruas
    residuo = patio_contenedores.shape[0] % n_gruas
    grua_fila_patio_equitativa = {}

    for i in range(n_gruas):
        grua_fila_patio_equitativa[i] = list(range(i * elementos_por_grua + min(i, residuo), (i + 1) * elementos_por_grua + min(i + 1, residuo)))
        
    return grua_fila_patio_equitativa

def inicializar_gruas(n_gruas):
    """Inicializa el diccionario de grúas."""
    gruas = {}
    for grua in range(n_gruas):
        gruas[grua] = []
        
    return gruas



    
def buscar_grua_a_asignar(grua_fila_patio_equitativa, fila):
    grua_asignar = list(grua_fila_patio_equitativa.keys())[0]
    for grua in grua_fila_patio_equitativa:
        if fila in grua_fila_patio_equitativa[grua]:
            grua_asignar = grua
    return grua_asignar
    

def asignar_contenedores_a_gruas_a(patio_contenedores, gruas, seed):
    """Asigna contenedores a las gruas aleatoriamente."""

    random.seed(seed)
    pilas_patio = copy.deepcopy(patio_contenedores.pilas)
    contenedores_en_patio = np.sum([len(pila) for pila in pilas_patio])

    while contenedores_en_patio > 0:
        filas = []
        for fila in range(len(pilas_patio)):
            for pila in pilas_patio[fila]:
                if len(pila.pila) > 0:
                    filas.append(fila)

        fila = random.choice(filas)


        pilas = [i for i in range(len(pilas_patio[fila])) if len(pilas_patio[fila][i].pila) > 0]
        pila = random.choice(pilas)
        pila_contenedores = pilas_patio[fila][pila]
        
  
        contenedor = pila_contenedores.pila.pop(0)
        contenedores_en_patio -= 1
        
        grua_asignar=buscar_grua_a_asignar(patio_contenedores.asignacion_gruas_pilas, fila)
        contenedor.grua_asignada = grua_asignar
        gruas[grua_asignar].append(contenedor)
    
    return gruas




def asignar_contenedores_a_gruas(patio_contenedores, gruas, seed):
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
            pila = random.choice(pilas)
            pila_contenedores = pilas_patio[fila][pila]
            
      
            contenedor = pila_contenedores.pila.pop(0)
            contenedores_en_patio -= 1
            
            grua_asignar=buscar_grua_a_asignar(patio_contenedores.asignacion_gruas_pilas, fila)
            contenedor.grua_asignada = grua_asignar
            gruas[grua_asignar].append(contenedor)


        if cargar_nuevo_contenedor:
            # Elegimos un contenedor aleatorio de entre todos los existentes
            contenedor = random.choice(contenedores_en_espera)

            # Extraemos la pila asignada y la fila a la que debería ir
            pila_asignada = contenedor.pila_asignada
            fila, columna = pila_asignada.posicion[0], pila_asignada.posicion[1]

            # Buscamos la grua asignada a esa fila 
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

