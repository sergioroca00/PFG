from EscribirBBDD import escribir
from Main import obtenerDiarios
from datetime import datetime
import time
import argparse

# NOTAS:
# formato  de la fecha: aaaammdd



# Measurement son las diferentes tablas que se tienen en la base de datos.
measurement = 'diarios'

# Se recoge la url a la que enviar los datos como parámetro de programa
parser = argparse.ArgumentParser(description="")
parser.add_argument("--inicio", type=str, help="Año de instalación")
parser.add_argument("--fin", type=str, help="Año actual")
args = parser.parse_args()
inicio = int(args.inicio)
fin  = int(args.fin) 

def rellenar_historico_diario():
    # Se utiliza un doble bucle for para recorrer años y meses haciendo una petición por cada mes desde
    # que se instaló el inversor.
    for year in range (inicio, fin + 1):
        for month in range (1,13):
            # Se construye la fecha en formato aaaammdd 
            # La función zfill() sirve para rellenar una cadena de caracteres con 0 a la izquierda hasta 
            # cumplir con el parámetro que se le pasa, en este caso 2. Un ejemplo es que si el mes es 10 
            # se deja como está, pero si es 9, se le añade un cero para convertirlo en 09
            # El día es siempre el 1 porque es indiferente cuál se indique, la respuesta contiene los datos
            # de todos los días del mes 
            date = str(year)+str(month).zfill(2)+'01'
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
                    df = obtenerDiarios(date).reset_index()
                    # Si no se ha obtenido ninguna expeción, la ejecución continúa llamando a la función
                    # escribirCompleto() para introducir el df en la tabla 'measurement' de la base de datos
                    # y se imprime el resultado para corroborar que ha funcionado correctamente
                    print("Datos diarios.",escribir(df, measurement), "de la fecha", date)
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



rellenar_historico_diario()
