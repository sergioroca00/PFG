import pandas as pd
from influxdb import InfluxDBClient

import socket

def obtener_ip_privada():
    # Crear un socket temporal para conectarse a una dirección sin salir a Internet
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectar a una IP pública (por ejemplo, 8.8.8.8 de Google) sin enviar datos
        s.connect(("8.8.8.8", 80))
        ip_privada = s.getsockname()[0]  # Obtiene la IP privada utilizada para la conexión
    finally:
        s.close()  # Cierra el socket
    return str(ip_privada)

ip = obtener_ip_privada()
# Crea una instancia del cliente de InfluxDB, el parámetro host indica la dirección
# IP del servidor en el que se aloja la base de datos, en nuestro caso la dirección
# de la máquina virtual de la Raspberry Pi; y el segundo parámetro indica el puerto
# mediante el que se a establecer la conexión
client = InfluxDBClient (host=ip, port=8086)
# Se indica el nombre de la base de datos que se va a utilizar
client.switch_database('Inversor')



def escribir(df:pd.DataFrame, measurement:str):
    # Se crea una lista vacía en la que se van a incluir los datos que vienen del 
    # Dataframe en el primer parámetro
    points = []
    # Se utiliza un bucle para recorrer cada una de las filas del dataframe
    # para crear un punto , que es una variable de tipo diccionario, con los datos 
    # obtenidos del dataframe y guardarlo en la "points" que se ha creado antes
    for i, row in df.iterrows():
        point = {
            # Se asigna el nombre d ela tabla donde se va a guardar
            "measurement": measurement,
            # Se asigna la columna collectTime time del datframe con el eje de 
            # tiempos de influxDB
            # Se tiene que llamar time obligatoriamente para que la base de datos lo entienda
            "time": row['collectTime'],
            # Se recogen cada uno de los datos devueltos por la API
            "fields": {
                # Energia que ha generado el inversor en kWh
                "Energía generada": row['inverter_power'],
                # Energia consumida directamente de las placas solares en kWh
                "Autoconsumo": row['selfUsePower'],
                # Ingresos en €
                "Ingresos": row['power_profit'],
                # Ratio entre energia generada/capacidad instalada
                "Ratio": row['perpower_ratio'],
                # Ahorro de CO2 en toneladas
                "Ahorro CO2": row['reduction_total_co2'],
                # Capacidad instalada en kW
                "Capacidad instalada": row['installed_capacity'],
                # Consumo en kWh
                "Consumo total": row['use_power'],
                # Ahorro de carbón en toneladas
                "Ahorro carbon": row['reduction_total_coal'],
                # Potencia introducia en la red en kWh
                "Energía vendida": row['ongrid_power'],
                # Potencia comprada de la red en kWh
                "Energía comprada": row['buyPower']
            }
        }
        # Se añade el diccionario "point" a la lista "points"
        points.append(point)
    # Una vez terminado el bucle se añade la list a"points" a la base de datos
    client.write_points(points)
    # Se devuelve el mensaje de que todo ha funcionado con normalidad
    return("Datos guardados exitosamente en InfluxDB")


# Funciona igual que la función escribir() pero tiene menos datos ya que la respuesta de la API 
# es distinta. Solo aplica a los datos horarios
def escribirHorarios(df:pd.DataFrame, measurement:str):
    points = []
    for i, row in df.iterrows():
        point = {
            "measurement": measurement,
            "time": row['collectTime'], 
            "fields": {
                "Energía generada": row['inverter_power'],
                "Ingresos": row['power_profit'],
                "Energía vendida": row['ongrid_power'],
                "Autoconsumo": row['selfProvide']   
            }
        }
        points.append(point)
    client.write_points(points)
    return("Datos guardados exitosamente en InfluxDB")
