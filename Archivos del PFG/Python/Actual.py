from Main import obtenerActual
import requests
import time
import argparse


# Se recoge la url a la que enviar los datos como parámetro de programa
parser = argparse.ArgumentParser(description="Datos en tiempo real")
parser.add_argument("--url", type=str, help="URL de OpenHAP")
args = parser.parse_args()
url = str(args.url)





# Cabeceras necesarias en la peticion http
headers = {
    "Content-Type": "text/plain",
    "Accept": "application/json"
}

def enviarDatosOpenHAB(url:str):
    # Se recogen el valor acumulado del día de potencia generada (income) y consumida (power)
    # mediante la función obtenerActual() de la clase main
    day_income, day_power = obtenerActual()
    # Se envía el valor de potencia generada a la API
    # El primer parámetro es la URL general añadiendo el item "day_incomo", puesto que cada item tiene su URL concreta
    # El segundo parámetro es el propio valor convertido a cadena de caracteres
    # El tercer parámetro son las cabeceras definidas previamente
    response = requests.post(url+"day_income", data=str(day_income), headers=headers)
    # Verificar si la petición fue exitosa
    # El código 200 (OK) significa que la petición fue recibida y contestada correctamente
    # El código 202 (Accepted) significa que la petición fue recibida correctamente pero no se ha 
    # terminado de procesar. Ambos son válido puesto que la petición ha llegado correctamente
    if response.status_code == 202 or response.status_code == 200:
        # Se imprime el valor enviado para comprobar que es el mismo que el que se visualiza en OpenHab
        print("Day income =", day_income, "enviado a OpenHAB")
    else:
        # Si la respuesta tiene un código distinto a los dos definidos como válidos, se imprime el mensaje
        # de que ha ocurrido un error y el código de la repsuesta.
        print(f"Error al enviar el valor: {response.status_code}")


    # Se repite el procedimiento anterior, pero esta vez con la potencia consumida (day_power)
    response = requests.post(url+"day_power", data=str(day_power), headers=headers)
    if response.status_code == 202 or response.status_code == 200:
        print("Day power =", day_power, "enviado a OpenHAB")
    else:
        print(f"Error al enviar el valor: {response.status_code}")


enviarDatosOpenHAB(url)

