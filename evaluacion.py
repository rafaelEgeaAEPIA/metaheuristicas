import numpy as np
from grua import Grua 
from datetime import  timedelta
import pandas as pd 




def establecer_configuracion_gruas(gruas, patio_contenedores):
    posicion_fecha = {}

    # Iterar sobre las grúas y sus contenedores asociados
    for grua, contenedores in gruas.items():
        if len(contenedores) >0:

            # Calcular la fecha de finalización del movimiento previo
            previa_posicion_grua = patio_contenedores.gruas[grua].posicion_inicial
            fecha_fin_movimiento_previo = contenedores[0].fecha_salida - timedelta(minutes=(abs(contenedores[0].pila_asignada.posicion[0] - previa_posicion_grua[0]) * Grua.tiempo_entre_filas + abs(contenedores[0].pila_asignada.posicion[1] - previa_posicion_grua[1]) * Grua.tiempo_entre_columnas + abs(contenedores[0].pila_asignada.posicion[1] - patio_contenedores.shape[1]) * Grua.tiempo_entre_columnas) / 6e4)
            
            # Iterar sobre los contenedores de la grúa
            for contenedor_a_procesar in contenedores:
                posicion_procesar = contenedor_a_procesar.pila_asignada.posicion_descarga if contenedor_a_procesar.hay_que_cargar else contenedor_a_procesar.pila_asignada.posicion
                fecha_operacion = contenedor_a_procesar.fecha_entrada if contenedor_a_procesar.hay_que_cargar else contenedor_a_procesar.fecha_salida
                tiempo_viaje_al_contenedor = abs(posicion_procesar[0] - previa_posicion_grua[0]) * Grua.tiempo_entre_filas + abs(posicion_procesar[1] - previa_posicion_grua[1]) * Grua.tiempo_entre_columnas
                tiempo_de_carga_o_descarga_del_contenedor = abs(contenedor_a_procesar.pila_asignada.posicion[1] - patio_contenedores.shape[1]) * Grua.tiempo_entre_columnas
                tiempo_operacion = (tiempo_viaje_al_contenedor + tiempo_de_carga_o_descarga_del_contenedor) / 6e4
                tiempo_inicio_optimo = fecha_operacion - timedelta(minutes=tiempo_operacion)
                inicio_movimiento = tiempo_inicio_optimo if fecha_fin_movimiento_previo < tiempo_inicio_optimo else fecha_fin_movimiento_previo
                fin_movimiento = inicio_movimiento + timedelta(minutes=tiempo_operacion)
                
                # Almacenar los datos en el diccionario posicion_fecha
                posicion_fecha.setdefault(grua, {}).setdefault(contenedor_a_procesar.id_contenedor, {
                    "posicion_previa_grua": previa_posicion_grua,
                    "contenedor_a_procesar": posicion_procesar,
                    "fecha_operacion_contenedor": fecha_operacion,
                    "grua_asignada": contenedor_a_procesar.grua_asignada,
                    "tiempo_operacion": tiempo_operacion,
                    "tiempo_inicio_optimo": tiempo_inicio_optimo,
                    "inicio_movimiento": inicio_movimiento,
                    "fin_movimiento": fin_movimiento,
                    "cargar_contenedor": contenedor_a_procesar.hay_que_cargar,
                    "id_contenedor": contenedor_a_procesar.id_contenedor,
                    "contenedor":contenedor_a_procesar
                })
                previa_posicion_grua = contenedor_a_procesar.pila_asignada.posicion_descarga
                fecha_fin_movimiento_previo = fin_movimiento

    # Convertir el diccionario a DataFrame
    solucion = pd.DataFrame(posicion_fecha[grua][id_contenedor] for grua in posicion_fecha for id_contenedor in posicion_fecha[grua])
    # Ordenar la solución por el tiempo de inicio de movimiento
    solucion = solucion.sort_values("inicio_movimiento")
    solucion.index = range(solucion.shape[0])
    return solucion


def objective_function(solucion, patio_contenedores, margen_seguridad=1):
    # Calcular el tiempo de penalización para cada contenedor en minutos
    solucion["penalizacion"] = (solucion["fin_movimiento"] - solucion["fecha_operacion_contenedor"]).dt.total_seconds() / 60


    # Iterar sobre cada contenedor procesado
    for id_contenedor_siendo_procesado, row in solucion.iterrows():
        grua_asignada = row["grua_asignada"]
        posicion_descarga = row["contenedor_a_procesar"]
        patio_contenedores.gruas[grua_asignada].posicion = posicion_descarga
        posicion_previa_grua = row["posicion_previa_grua"]

        # Comprobar si hay colisión entre grúas
        for grua, grua_info in patio_contenedores.gruas.items():
            if grua != grua_asignada:
                min_fila = min(posicion_descarga[0], posicion_previa_grua[0])
                max_fila = max(posicion_descarga[0], posicion_previa_grua[0])

                # Crear un rango de movimientos para cada grúa
                rango_movimientos = range(min_fila, max_fila + 1)

                # Verificar si las grúas están en el mismo rango de movimiento
                if grua_info.posicion[0] in rango_movimientos:
                    print("Gruas van a chocar")
                    return np.inf  # Devolver infinito si las grúas chocan

                # Verificar si se cumple el margen de seguridad
                if np.min([abs(grua_info.posicion[0] - movimiento) for movimiento in rango_movimientos]) < margen_seguridad:
                    print("Se incumple margen seguridad")
                    return np.inf  # Devolver infinito si se incumple el margen de seguridad

    # Devolver la suma de penalizaciones si no hay colisión ni incumplimiento de margen de seguridad
    return solucion["penalizacion"].sum()


def evaluar_solucion(asignacion_contenedor_gruas, patio_contenedores):
    """
        Funcion que obtiene el fitness  de una solución y la devuelve.
        
        Parámetros: 
            - asignacion_contenedor_gruas: Diccionario con clave el identificador de cada grua
            y valor la lista con los contenedores a visitar por orden
            - patio_contenedores: Instancia de la calse PatioContenedores, con los datos específicos del problema
            generado.
            
        Devuelve:
            - El tiempo de espera  total para todos los contenedores en minutos.
    """
    # Se configura  el grafo con las distancias entre los nodos (Gruas, Contenedores), los tiempos en los que visitar y el orden de visita 
    # de cada contenedor
    configuracion_solucion = establecer_configuracion_gruas(asignacion_contenedor_gruas, patio_contenedores)
    # Calculo del fitness de la solucion
    # Se suman los tiempos de espera de  todos los contenedores
    fitness = objective_function(configuracion_solucion, patio_contenedores)

    return fitness