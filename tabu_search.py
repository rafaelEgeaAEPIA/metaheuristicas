
from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from generar_problema_incial import  generar_solucion_inicial, generar_patio_contenedores
from funciones_auxiliares import generar_vecino
from patio_contenedores import PatioContenedores
import numpy as np
import hashlib


def obtener_id_vecino(vecino):

    # Convertir el diccionario a una cadena JSON

    # Calcular el hash SHA-1 (SHA-128)
    hash_obj = hashlib.sha1(str(vecino).encode())
    hash_resultado = hash_obj.hexdigest()

    return hash_resultado




def tabu_search(initial_solucion, datos, patio_contenedores, seed):
    """
    Implementación de Tabu Search.
    """
    mejor_solucion = None
    mejor_costo = np.inf
    solucion_actual = initial_solucion
    tabu_list = []  # Lista tabú
    max_iterations = datos['Max. Iter.']
    tam_tabu = datos['Tam. Tabu']

    for i in range(max_iterations):
        seed = i
        new_neighbor = generar_vecino(solucion_actual, patio_contenedores, seed)
        vecino_costo = evaluar_solucion(new_neighbor, patio_contenedores)
          
        
        # Si el vecino no está en la lista tabú y mejora el costo, actualizamos la solución
        if (vecino_costo < mejor_costo) and (obtener_id_vecino(new_neighbor) not in tabu_list):
            mejor_solucion = new_neighbor
            mejor_costo = vecino_costo

        # Actualizamos la solución actual
        solucion_actual = new_neighbor

        # Añadimos el movimiento a la lista tabú
        tabu_list.append(obtener_id_vecino(new_neighbor))

        # Mantenemos el tamaño de la lista tabú
        if len(tabu_list) > tam_tabu:
            tabu_list.pop(0)



    return mejor_solucion, mejor_costo

# Parámetros

if __name__ == "__main__":
    patio_contenedores = PatioContenedores()

    seed = 1000
    patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(10,10,10, seed)

 
    patio_contenedores.imprimir_patio_contenedores()

    n_gruas = 2
    initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
    
    
    evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)

    iteraciones = 100
    tam_tabu = 10

    # Ejecución del algoritmo
    mejor_solucion, mejor_costo = tabu_search(initial_solucion, iteraciones, patio_contenedores, seed)

    # Resultados
    print("costo primera solucion", evaluacion_solucion)
    print("Costo de la mejor solución:", mejor_costo)


