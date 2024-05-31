
from evaluacion import evaluar_solucion
from generar_problema_incial import  generar_solucion_inicial, generar_patio_contenedores
from enfriamiento_simulado import simulated_annealing
from vns import vns
from patio_contenedores import PatioContenedores
import json
import time 
from tabu_search import tabu_search
from grasp import grasp

combinaciones_pc = {
    1: {'n_rows': 5, 'n_cols': 5, 'max_cont': 10, 'n_gruas': 2},
    2: {'n_rows': 6, 'n_cols': 4, 'max_cont': 12, 'n_gruas': 3},
    3: {'n_rows': 7, 'n_cols': 6, 'max_cont': 15, 'n_gruas': 2},
    4: {'n_rows': 8, 'n_cols': 5, 'max_cont': 8, 'n_gruas': 4},
    5: {'n_rows': 9, 'n_cols': 7, 'max_cont': 11, 'n_gruas': 3},
    6: {'n_rows': 6, 'n_cols': 6, 'max_cont': 14, 'n_gruas': 2},
    7: {'n_rows': 4, 'n_cols': 8, 'max_cont': 9, 'n_gruas': 3},
    8: {'n_rows': 7, 'n_cols': 8, 'max_cont': 13, 'n_gruas': 4},
    9: {'n_rows': 5, 'n_cols': 9, 'max_cont': 16, 'n_gruas': 2},
    10: {'n_rows': 8, 'n_cols': 6, 'max_cont': 12, 'n_gruas': 3},
    11: {'n_rows': 6, 'n_cols': 7, 'max_cont': 11, 'n_gruas': 5},
    12: {'n_rows': 9, 'n_cols': 9, 'max_cont': 14, 'n_gruas': 3},
    13: {'n_rows': 7, 'n_cols': 5, 'max_cont': 13, 'n_gruas': 2},
    14: {'n_rows': 5, 'n_cols': 6, 'max_cont': 15, 'n_gruas': 4},
    15: {'n_rows': 4, 'n_cols': 7, 'max_cont': 9, 'n_gruas': 3}
}

datos_recocido_simulado = {
    1: {'TI': 100.0, 'CR': 0.1, 'SS': 0.1, 'Max. Iter.': 50},
    2: {'TI': 200.0, 'CR': 0.1, 'SS': 0.1, 'Max. Iter.': 100},
    3: {'TI': 300.0, 'CR': 0.1, 'SS': 0.1, 'Max. Iter.': 150},
    4: {'TI': 100.0, 'CR': 0.3, 'SS': 0.1, 'Max. Iter.': 50},
    5: {'TI': 200.0, 'CR': 0.3, 'SS': 0.1, 'Max. Iter.': 100},
    6: {'TI': 300.0, 'CR': 0.3, 'SS': 0.1, 'Max. Iter.': 150},
    7: {'TI': 100.0, 'CR': 0.6, 'SS': 0.1, 'Max. Iter.': 50},
    8: {'TI': 200.0, 'CR': 0.6, 'SS': 0.1, 'Max. Iter.': 100},
    9: {'TI': 300.0, 'CR': 0.6, 'SS': 0.2, 'Max. Iter.': 150},
    10: {'TI': 100.0, 'CR': 0.9, 'SS': 0.2, 'Max. Iter.': 50},
    11: {'TI': 200.0, 'CR': 0.9, 'SS': 0.2, 'Max. Iter.': 100},
    12: {'TI': 300.0, 'CR': 0.9, 'SS': 0.05, 'Max. Iter.': 150},
}

datos_VNS = {
    1: {'Max. Iter.': 50, 'Max. Iter. BL': 10, 'K': 100},
    2: {'Max. Iter.': 50, 'Max. Iter. BL': 50, 'K': 100},
    3: {'Max. Iter.': 50, 'Max. Iter. BL': 100, 'K': 100},
    4: {'Max. Iter.': 100, 'Max. Iter. BL': 10, 'K': 60},
    5: {'Max. Iter.': 100, 'Max. Iter. BL': 50, 'K': 60},
    6: {'Max. Iter.': 100, 'Max. Iter. BL': 100, 'K': 60},
    7: {'Max. Iter.': 150, 'Max. Iter. BL': 10, 'K': 50},
    8: {'Max. Iter.': 150, 'Max. Iter. BL': 50, 'K': 50},
    9: {'Max. Iter.': 150, 'Max. Iter. BL': 100, 'K': 50},
    10: {'Max. Iter.': 200, 'Max. Iter. BL': 10, 'K': 20},
    11: {'Max. Iter.': 200, 'Max. Iter. BL': 50, 'K': 20},
    12: {'Max. Iter.': 200, 'Max. Iter. BL': 100, 'K': 20},
}

datos_Grasp = {
    1: {'Max. Iter.': 5, 'Max. Iter. BL': 10},
    2: {'Max. Iter.': 10, 'Max. Iter. BL': 25},
    3: {'Max. Iter.': 20, 'Max. Iter. BL': 50},
    4: {'Max. Iter.': 30, 'Max. Iter. BL': 10},
    5: {'Max. Iter.': 40, 'Max. Iter. BL': 25},
    6: {'Max. Iter.': 50, 'Max. Iter. BL': 50},
    7: {'Max. Iter.': 60, 'Max. Iter. BL': 10},
    8: {'Max. Iter.': 70, 'Max. Iter. BL': 25},
    9: {'Max. Iter.': 80, 'Max. Iter. BL': 50},
    10: {'Max. Iter.': 90, 'Max. Iter. BL': 10},
    11: {'Max. Iter.': 100, 'Max. Iter. BL': 25},
    12: {'Max. Iter.': 110, 'Max. Iter. BL': 50},
}

datos_busqueda_tabu = {
    1: {'Max. Iter.': 50, 'Tam. Tabu': 10},
    2: {'Max. Iter.': 50, 'Tam. Tabu': 20},
    3: {'Max. Iter.': 50, 'Tam. Tabu': 30},
    4: {'Max. Iter.': 100, 'Tam. Tabu': 10},
    5: {'Max. Iter.': 100, 'Tam. Tabu': 20},
    6: {'Max. Iter.': 100, 'Tam. Tabu': 30},
    7: {'Max. Iter.': 150, 'Tam. Tabu': 10},
    8: {'Max. Iter.': 150, 'Tam. Tabu': 20},
    9: {'Max. Iter.': 150, 'Tam. Tabu': 30},
    10: {'Max. Iter.': 200, 'Tam. Tabu': 10},
    11: {'Max. Iter.': 200, 'Tam. Tabu': 20},
    12: {'Max. Iter.': 200, 'Tam. Tabu': 30},
}


if __name__ == "__main__":
    patio_contenedores = PatioContenedores()

    resultados = {}
    for prueba in combinaciones_pc.keys():
        print(prueba)
        n_rows = combinaciones_pc[prueba]["n_rows"]
        n_cols = combinaciones_pc[prueba]["n_cols"]
        max_cont = combinaciones_pc[prueba]["max_cont"]
        n_gruas = combinaciones_pc[prueba]["n_gruas"]
        resultados[prueba] = {}
        datos = datos_Grasp

        for combinaciones in datos.keys():
            print(combinaciones)
            resultados[prueba][combinaciones] = {}
            for seed in [1]:
            
                patio_contenedores.pilas, patio_contenedores.shape, patio_contenedores.contenedores_en_espera = generar_patio_contenedores(n_rows,n_cols,max_cont, seed)

                inicio = time.time()
                initial_solucion, patio_contenedores = generar_solucion_inicial(patio_contenedores, n_gruas=n_gruas, seed=seed)
                evaluacion_solucion = evaluar_solucion(initial_solucion, patio_contenedores)
                fin = time.time()
                print(evaluacion_solucion)
                resultados[prueba][combinaciones]["solucion_inicial"] = evaluacion_solucion
                resultados[prueba][combinaciones]["tinicial"] = str(fin-inicio)

                inicio = time.time()
                #best_solution, best_cost = vns(initial_solucion, datos[combinaciones], patio_contenedores, seed)
                # best_solution, best_cost = tabu_search(initial_solucion, datos[combinaciones], patio_contenedores, seed)
                best_solution, best_cost = grasp(initial_solucion, datos[combinaciones], patio_contenedores, n_gruas, seed)

                #best_solution, best_cost = simulated_annealing(initial_solucion, datos_recocido_simulado[combinaciones], patio_contenedores, seed)
                print(best_cost)
                fin = time.time()

                resultados[prueba][combinaciones]["solucion_final"] = best_cost
                resultados[prueba][combinaciones]["tfinal"] = str(fin-inicio)


    json_string = json.dumps(resultados, indent=4)

    # Guardar en un archivo
    nombre_archivo = "datosGrasp.json"
    with open(nombre_archivo, "w") as archivo:
        archivo.write(json_string)
