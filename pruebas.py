

from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from generar_problema_incial import  generar_solucion_inicial, generar_patio_contenedores
from funciones_auxiliares import generar_vecino
from patio_contenedores import PatioContenedores
from tabu_search import tabu_search
from vns import vns
from grasp import grasp
from enfriamiento_simulado import simulated_annealing



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
mejor_solucion, mejor_costo = grasp(initial_solucion, iteraciones, patio_contenedores, seed)

# Resultados
print("costo primera solucion", evaluacion_solucion)
print("Costo de la mejor solución:", mejor_costo)