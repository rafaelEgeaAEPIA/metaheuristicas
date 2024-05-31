from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from generar_problema_incial import  generar_solucion_inicial, generar_patio_contenedores
from funciones_auxiliares import generar_vecino
from patio_contenedores import PatioContenedores
import numpy as np
import random

def generar_vecindario(solucion):
    # Esta función genera una lista de soluciones vecinas a partir de la solución actual
    vecindario = []
    for i in range(len(solucion)):
        for j in range(i+1, len(solucion)):
            vecino = generar_vecino(solucion, patio_contenedores, i+j)
            vecindario.append(vecino)

    return vecindario


def busqueda_local(solucion, patio_contenedores, iters):

    mejor_solucion = solucion
    mejor_costo = evaluar_solucion(mejor_solucion, patio_contenedores)
    for i in range(iters):
        vecino = generar_vecino(solucion, patio_contenedores, i)
        if evaluar_solucion(vecino, patio_contenedores) < mejor_costo:
            mejor_solucion = vecino
            mejor_costo = evaluar_solucion(vecino, patio_contenedores)

    return mejor_solucion, mejor_costo


def vns(initial_solucion, datos, patio_contenedores, seed):
    iteraciones = datos['Max. Iter.']
    mejor_solucion = initial_solucion
    mejor_costo =  evaluar_solucion(mejor_solucion, patio_contenedores)
    k = 1
    i=0
    while k <= datos["K"] and i<iteraciones:
        vecino = generar_vecino(mejor_solucion, patio_contenedores, i+k) 

        mejor_vecino, costo_vecino = busqueda_local(vecino, patio_contenedores, datos[ 'Max. Iter. BL'])

        if costo_vecino < mejor_costo:
            mejor_solucion = mejor_vecino
            mejor_costo = costo_vecino
            k = 1 
        else:
            k += 1

        i+=1
    return mejor_solucion, mejor_costo



if __name__ == "__main__":
    """
    patio_contenedores = PatioContenedores()

    seed = 100
    patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(10,10,10, seed)

 
    patio_contenedores.imprimir_patio_contenedores()

    n_gruas = 2
    initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
    
    
    evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)

    iteraciones = 10000
    k_max = 30
    mejor_solucion, mejor_costo = vns(initial_solucion, iteraciones, patio_contenedores, k_max)
    print("costo primera solucion", evaluacion_solucion)
    print("Costo de la mejor solución:", mejor_costo)
    """
    patio_contenedores = PatioContenedores()

    seed = 100
    patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(10,10,10, seed)

 
    patio_contenedores.imprimir_patio_contenedores()

    n_gruas = 2
    initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
    
    
    evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)



    iteraciones = 10000
    k_max = 30
    mejor_solucion, mejor_costo = vns(initial_solucion, iteraciones, patio_contenedores, k_max)
    print("costo primera solucion", evaluacion_solucion)
    print("Costo de la mejor solución:", mejor_costo)