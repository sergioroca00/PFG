from EscribirBBDD import escribir
import pandas as pd
from Main import obtenerAnuales
from datetime import datetime
import time



# NOTAS:
# formato  de la fecha: aaaammdd


# Measurement son las diferentes tablas que se tienen en la base de datos.
measurement = 'anuales'


def anuales():
    # Se obtiene la fecha actual en formato aaaammdd
    date = datetime.now().strftime("%Y%m%d")
    # Variable booleana utilizada para almacenar si la petición a la API ha sido existosa o no, 
    # y en caso negativo, intentarlo de nuevo
    intento_exitoso = False
    # Se utiliza un bucle mientras que intento_exitoso sea False
    while not intento_exitoso:
        # Se utiliza try ya que la funcion obtenerAnuales() puede lanzar una excepción si se supera
        # el límite de peticiones que se pueden realizar
        try:
            # Se llama a la función para pedir los datos a la API y se almacena el resultado esperado, 
            # que es un dataframe, en la variable df
            df = obtenerAnuales(date).reset_index()
            # Si no se ha obtenido ninguna expeción, la ejecución continúa llamando a la función
            # escribirCompleto() para introducir el df en la tabla 'measurement' de la base de datos
            # y se imprime el resultado para corroborar que ha funcionado correctamente
            print("Datos anuales.",escribir(df, measurement), "de la fecha", date)
            # Si la ejecución llega a este punto es porque no se ha producido ninguna excepción, por 
            # lo que el intento ha sido exitoso y se pone la variable a True, no hace falta repetir la petición
            intento_exitoso = True
        except Exception as e:
            # Si se captura una excepción, se imprime el mensaje de error recibido y se informa de que el programa
            # va a esperar 10 minutos y a reintentarlo de nuevo
            print(f"Error al procesar {date}: {e}. Reintentando en 10 minutos...")
            time.sleep(600)


anuales()