from EscribirBBDD import escribirHorarios
import pandas as pd
from Main import obtenerHorarios
from datetime import datetime

import time


# NOTAS:
# formato  de la fecha: aaaammdd
# Estan guaradados los datos de la primera semana de enero de 2024 y de la primera semana de agosto de 2024
# Dos modos de ejecucion:
# 1. Ejecución función horarios(). Genera la fecha de hoy en el formato comentado y llama a la funcion obtenerHorarios 
#     de main para obtener los 24 datos horarios de hoy
# 2. Ejecución función rellenar_historico_horario(). Recorre todos los días desde el 1 de enero del 2019 hasta el 31 de 
#     diciembre del 2024 pidiendo en cada día los 24 datos para rellenar la base de datos.
# Para cambiar entre un modo de ejecución y otro, comentar la invocacion a la funcion que se quiera


# Measurement son las diferentes tablas que se tienen en la base de datos. 
measurement = 'horarios'


def horarios():
    # Se obtiene la fecha actual en formato aaaammdd
    date = datetime.now().strftime("%Y%m%d")
    # Se invoca a la función obtenerHorarios() de la clase main, como parámetro se pasa la fecha actual
    # Esta función a su vez invocará a otras para lanzar la petición a la API, obtener los datos y devolverlos 
    # en forma de DataFrame de Pandas, que se guarda en la variable df
    df = obtenerHorarios(date).reset_index()
    # Se invoca a la función escribirHorarios() de la clase EscribirBBDD, como parámetro se pasa el dataframe 
    # obtenido y almacenado en la variable df y la variable measurement que indica la tabla de la base de datos
    # en la que se quiere almacenar dicho dataframe
    res = escribirHorarios(df, measurement)
    # Se imprime el resultado de la escritura de la base de datos para comprobar si ha funcionado correctamente
    print ("Datos horarios.",res, "de la fecha", date)



horarios()


