from EscribirBBDD import escribir
import pandas as pd
from Main import obtenerDiarios
from datetime import datetime
import time

# NOTAS:
# formato  de la fecha: aaaammdd



# Measurement son las diferentes tablas que se tienen en la base de datos.
measurement = 'diarios'


def diarios():
    # Se obtiene la fecha actual en formato aaaammdd
    date = datetime.now().strftime("%Y%m%d")
    # Se invoca a la función obtenerDiarios() de la clase main, como parámetro se pasa la fecha actual
    # Esta función a su vez invocará a otras para lanzar la petición a la API, obtener los datos y devolverlos 
    # en forma de DataFrame de Pandas, que se guarda en la variable df
    df = obtenerDiarios(date).reset_index()
    # Se invoca a la función escribirCompleto() de la clase EscribirBBDD, como parámetro se pasa el dataframe 
    # obtenido y almacenado en la variable df y la variable measurement que indica la tabla de la base de datos
    # en la que se quiere almacenar dicho dataframe
    res = escribir(df, measurement)
    # Se imprime el resultado de la escritura de la base de datos para comprobar si ha funcionado correctamente
    print ("Datos diarios.", res, "de la fecha", date)
        


diarios()




