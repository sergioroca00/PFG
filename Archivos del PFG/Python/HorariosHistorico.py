from EscribirBBDD import escribirHorarios
import pandas as pd
from Main import obtenerHorarios
from datetime import datetime
import calendar
import time
import argparse

# Measurement son las diferentes tablas que se tienen en la base de datos. 
measurement = 'horarios'

# Se recoge la url a la que enviar los datos como parámetro de programa
parser = argparse.ArgumentParser(description="")
parser.add_argument("--inicio", type=str, help="Año de instalación")
parser.add_argument("--fin", type=str, help="Año actual")
args = parser.parse_args()
inicio = int(args.inicio)
fin = int(args.fin)

def rellenar_historico_horario():
    # Se utiliza un triple bucle for para recorrer años, meses y días haciendo una petición por cada día desde
    # que se instaló el inversor.
    
    for year in range(inicio, fin +1):
        for month in range(1, 13):
            # Obtener el número de días en el mes que se está iterando
            days_in_month = calendar.monthrange(year, month)[1]  
            for day in range(1, days_in_month + 1):
                # Se construye la fecha en formato aaaammdd 
                # La función zfill() sirve para rellenar una cadena de caracteres con 0 a la izquierda hasta 
                # cumplir con el parámetro que se le pasa, en este caso 2. Un ejemplo es que si el día es 10 
                # se deja como está, pero si es 9, se le añade un cero para convertirlo en 09
                date = str(year) + str(month).zfill(2) + str(day).zfill(2)
                # Variable booleana utilizada para almacenar si la petición a la API ha sido existosa o no, 
                # y en caso negativo, intentarlo de nuevo
                intento_exitoso = False
                # Se utiliza un bucle mientras que intento_exitoso sea False
                while not intento_exitoso :
                    # Se utiliza try ya que la funcion obtenerHorarios() puede lanzar una excepción si se supera
                    # el límite de peticiones que se pueden realizar
                    try:
                        # Se llama a la función para pedir los datos a la API y se almacena el resultado esperado, 
                        # que es un dataframe, en la variable df
                        df = obtenerHorarios(date).reset_index()
                        # Si no se ha obtenido ninguna expeción, la ejecución continúa llamando a la función
                        # escribirHorarios() para introducir el df en la tabla 'measurement' de la base de datos
                        # y se imprime el resultado para corroborar que ha funcionado correctamente
                        print("Datos horarios.",escribirHorarios(df, measurement), "de la fecha", date)
                        # Si la ejecución llega a este punto es porque no se ha producido ninguna excepción, por 
                        # lo que el intento ha sido exitoso y se pone la variable a True, no hace falta repetir la petición
                        intento_exitoso = True
                        # Espera dos minutos y medio a seguir, ejecutando el programa con la siguiente llamada ya que la 
                        # API solo permite 5 llamadas cada 10 minutos.
                        time.sleep(150)
                    except Exception as e:
                        # Si se captura una excepción, se imprime el mensaje de error recibido y se informa de que el programa
                        # va a esperar 10 minutos y a reintentarlo de nuevo
                        print(f"Error al procesar {date}: {e}. Reintentando en 10 minutos...")
                        time.sleep(600)
                


rellenar_historico_horario()