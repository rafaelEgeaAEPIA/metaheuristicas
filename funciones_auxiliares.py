
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


def elegir_movimiento_aleatoriamente(solucion, seed):
    random.seed(seed)
    indice_movimiento = random.choice(solucion.index)

    return indice_movimiento


def get_grua_id(gruas, id):
    
    for grua in gruas:
        i=0
        for contenedor in gruas[grua]:
            if id == contenedor.id_contenedor:
                return grua, i
            else:
                i+=1
    
    return None

def cambiar_de_orden_movimiento(solucion, gruas, id_movimiento):
    """
        Dentro de los movimientos asignados a una misma grua, intercambiar el orden de procesado de 2 elementos
    """
    
    mask = solucion["grua_asignada"] == solucion.loc[id_movimiento, "grua_asignada"]
    movimientos_de_la_misma_grua = mask

    movimientos_superiores_al_actual = solucion.index.isin(solucion.index[movimientos_de_la_misma_grua]>id_movimiento)
    movimientos_superiores_al_actual = solucion.index.isin(solucion.index[movimientos_superiores_al_actual]>id_movimiento)
    

    if (movimientos_superiores_al_actual & movimientos_de_la_misma_grua).sum() > 0:
        siguiente_movimiento = solucion.index[movimientos_superiores_al_actual][0]
        id_contenedor_actual = solucion.loc[id_movimiento, "id_contenedor"]
        id_contenedor_mover = solucion.loc[siguiente_movimiento, "id_contenedor"]

        id_grua_a_manipular, indice_contenedor = get_grua_id(gruas, id_contenedor_actual)
        id_grua_a_manipular, indice_contenedor_mover = get_grua_id(gruas, id_contenedor_mover)

     
        gruas[id_grua_a_manipular][indice_contenedor_mover], gruas[id_grua_a_manipular][indice_contenedor] = gruas[id_grua_a_manipular][indice_contenedor], gruas[id_grua_a_manipular][indice_contenedor_mover]

       
    return gruas




def generar_vecino(gruas, patio_contenedores, seed):
    random.seed(seed)
    solucion = establecer_configuracion_gruas(gruas, patio_contenedores)

    id_movimiento = elegir_movimiento_aleatoriamente(solucion, seed)

    cambiar_de_orden = random.choice([True, False])
    if cambiar_de_orden:
        gruas = cambiar_de_orden_movimiento(solucion, gruas, id_movimiento)
    else:
        gruas = intercambiar_pila_en_frontera(solucion, gruas, id_movimiento, patio_contenedores, seed)

    return gruas
    

def variar_gruas(solucion, gruas, id_movimiento, pila_a_intercambiar):
    """
        Cambiar responsibilidades de contenedores a grua aledaña a partir de cierto punto
    """
    
    # mask de grua colindante indicada mediante parametro pila_a_intercambiar
    mask = [True if str(pila_a_intercambiar)+"," in posicion_contenedor else False for posicion_contenedor in solucion["contenedor_a_procesar"]]
    if np.sum(mask) > 0:
        grua_mas_responsabilidad = solucion.loc[id_movimiento, "grua_asignada"] 
        grua_menos_responsabilidad = solucion.loc[mask, "grua_asignada"].values[0]


        movimientos_superiores_al_actual = solucion.index.isin(solucion.index[mask]>id_movimiento)

        solucion.loc[movimientos_superiores_al_actual, "grua_asignada"] = grua_mas_responsabilidad

        mask = solucion["grua_asignada"] == grua_mas_responsabilidad
        gruas[grua_mas_responsabilidad] = list(solucion.loc[mask, "contenedor"].values)

        mask = solucion["grua_asignada"] == grua_menos_responsabilidad
        gruas[grua_menos_responsabilidad] = list(solucion.loc[mask, "contenedor"].values)

    return gruas



def intercambiar_pila_en_frontera(solucion, gruas, id_movimiento, patio_contenedores, seed):
    if len(gruas.keys()) > 1:
        patio_contenedores.asignacion_gruas_pilas
        
        grua_aleatoria = solucion.loc[id_movimiento, "grua_asignada"]

        index_grua = 0
        for index in range(len(gruas.keys())):
            if list(gruas.keys())[index_grua] == grua_aleatoria:
                index_grua = index

        
        if index_grua == 0:
            frontera_superior = True 
            frontera_inferior = not frontera_superior
        elif index_grua == len(gruas.keys())-1:
            frontera_inferior = True 
            frontera_superior = not frontera_inferior
        else:
            frontera_superior = random.choice([True, False])

            frontera_inferior = not frontera_superior


        if frontera_inferior:
            grua_anterior = list(gruas.keys())[index_grua-1]
            maximo_anterior = np.max(patio_contenedores.asignacion_gruas_pilas[grua_anterior])
            pila_a_intercambiar = maximo_anterior


        if frontera_superior:
            grua_superior = list(gruas.keys())[index_grua+1]
            minimo_superior = np.min(patio_contenedores.asignacion_gruas_pilas[grua_superior])
            pila_a_intercambiar = minimo_superior


    gruas = variar_gruas(solucion, gruas, id_movimiento, pila_a_intercambiar)

    return gruas
