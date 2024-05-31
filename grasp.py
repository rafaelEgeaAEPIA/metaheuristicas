
from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from generar_problema_incial import  generar_solucion_inicial, generar_patio_contenedores
from funciones_auxiliares import generar_vecino
from patio_contenedores import PatioContenedores
import numpy as np
from vns import busqueda_local



def grasp(solucion_inicial, datos, patio_contenedores,n_gruas, seed):
    mejor_solucion = solucion_inicial
    mejor_costo = np.inf

    num_iteraciones = datos['Max. Iter.']
    num_iteraciones_bl = datos['Max. Iter. BL']

    for i in range(num_iteraciones):

        solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=i)
    
        solucion, costo=busqueda_local(solucion, patio_contenedores, num_iteraciones_bl)            
        if costo < mejor_costo:
            mejor_solucion = solucion
            mejor_costo = costo
    return mejor_solucion, mejor_costo

# Ejemplo de uso
if __name__ == "__main__":
    
    """
    num_iteraciones = 100
    n_gruas=2
    patio_contenedores = PatioContenedores()
    seed = 1000
    patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(10,10,10, seed)

    initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
    evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)
    
    patio_contenedores = PatioContenedores()

    seed = 100
    patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(10,10,10, seed)

 
    patio_contenedores.imprimir_patio_contenedores()

    n_gruas = 2
    initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
    
    
    evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)
    print(evaluacion_solucion)
    num_iteraciones = 5

    mejor_solucion, mejor_costo = grasp(initial_solucion,num_iteraciones, n_gruas,  patio_contenedores, seed)
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

    print(evaluacion_solucion)

    num_iteraciones = 10
    k_max = 30
    mejor_solucion, mejor_costo = grasp(initial_solucion,num_iteraciones, n_gruas,  patio_contenedores, seed)
    print("costo primera solucion", evaluacion_solucion)
    print("Costo de la mejor solución:", mejor_costo)