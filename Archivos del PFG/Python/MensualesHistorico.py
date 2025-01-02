from Main import obtenerMensuales
from EscribirBBDD import escribir
import time
import argparse



measurement = 'mensuales'


# Se recoge la url a la que enviar los datos como parámetro de programa
parser = argparse.ArgumentParser(description="")
parser.add_argument("--inicio", type=str, help="Año de instalación")
parser.add_argument("--fin", type=str, help="Año actual")
args = parser.parse_args()
inicio = int(args.inicio)
fin = int(args.fin) 

def rellenar_historico_mensuales():
    # Se utiliza un bucle for para recorrer años haciendo una petición por cada uno desde que se instaló el inversor.
    for year in range (inicio, fin + 1): 
        # Se construye la fecha en formato aaaammdd 
        # El día y el mes es siempre el 1 porque es indiferente cuál se indique, la respuesta contiene los  12 datos
        # del año indicado
        date = str(year)+'0101'
        # Variable booleana utilizada para almacenar si la petición a la API ha sido existosa o no, 
        # y en caso negativo, intentarlo de nuevo
        intento_exitoso = False
        # Se utiliza un bucle mientras que intento_exitoso sea False
        while not intento_exitoso :
            # Se utiliza try ya que la funcion obtenerMensuales() puede lanzar una excepción si se supera
            # el límite de peticiones que se pueden realizar
            try:
                # Se llama a la función para pedir los datos a la API y se almacena el resultado esperado, 
                # que es un dataframe, en la variable df
                df = obtenerMensuales(date).reset_index()
                # Si no se ha obtenido ninguna expeción, la ejecución continúa llamando a la función
                # escribirCompleto() para introducir el df en la tabla 'measurement' de la base de datos
                # y se imprime el resultado para corroborar que ha funcionado correctamente
                print("Datos mensuales. ",escribir(df, measurement), "de la fecha", date)
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


rellenar_historico_mensuales()