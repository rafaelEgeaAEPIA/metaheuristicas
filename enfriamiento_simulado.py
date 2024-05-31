
from evaluacion import evaluar_solucion, establecer_configuracion_gruas
from generar_problema_incial import  generar_solucion_inicial, generar_patio_contenedores
from funciones_auxiliares import generar_vecino
import copy
import math 
import random
from patio_contenedores import PatioContenedores


def simulated_annealing(initial_solution, datos_recocido_simulado, patio_contenedores, seed):

    initial_temperature = datos_recocido_simulado["TI"]
    cooling_rate =datos_recocido_simulado["CR"]
    max_iterations =datos_recocido_simulado["Max. Iter."]

    current_solution = copy.deepcopy(initial_solution)
    current_temperature = initial_temperature
    best_solution = current_solution.copy()
    best_cost = evaluar_solucion(best_solution, patio_contenedores)


    for i in range(max_iterations):
        seed = i
        new_neighbor = generar_vecino(current_solution, patio_contenedores, seed)

        new_cost = evaluar_solucion(new_neighbor, patio_contenedores)
        if new_cost < best_cost:
            best_solution = new_neighbor
            best_cost = new_cost

        if new_cost < evaluar_solucion(current_solution, patio_contenedores):
            current_solution = new_neighbor
        else:
            probability = math.exp(-(new_cost - evaluar_solucion(current_solution, patio_contenedores)) / current_temperature)
            if random.random() < probability:
                current_solution = new_neighbor

        current_temperature *= cooling_rate

    return best_solution, best_cost





if __name__ == "__main__":
    patio_contenedores = PatioContenedores()

    seed = 100
    patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(10,10,10, seed)

 
    patio_contenedores.imprimir_patio_contenedores()

    n_gruas = 2
    initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
    
    
    evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)

    # Parámetros del algoritmo
    initial_temperature = 100.0
    cooling_rate = 0.6
    step_size = 0.1
    max_iterations = 100

    # Ejecución del algoritmo
    best_solution, best_cost = simulated_annealing(initial_solucion, initial_temperature, cooling_rate, step_size, max_iterations, patio_contenedores, seed)
    print(evaluacion_solucion)
    print(best_cost)