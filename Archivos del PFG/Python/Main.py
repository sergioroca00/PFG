from client import Client, PandasClient
import pandas as pd 
import json
import sqlite3

# Credenciales de acceso a la API
user = 'user'
password = 'password'

# Invoca a la función get_kpi_real() de la clase client, y guarda cada uno de los datos que vienen en un 
# diccionario en variables locales, y finalmente devuelve las que son de interés
def obtenerActual():
    data = client.get_kpi_real(station_code)
    total_income = data['data'][0]['dataItemMap']['total_income']
    total_power = data['data'][0]['dataItemMap']['total_power']
    day_income = data['data'][0]['dataItemMap']['day_income']
    day_power = data['data'][0]['dataItemMap']['day_power']
    real_health_state= data['data'][0]['dataItemMap']['real_health_state']
    month_power= data['data'][0]['dataItemMap']['month_power']
    return day_income, day_power

# Devuelve 24 datos, uno por cada hora del día pedido. 
def obtenerHorarios(date:str) -> pd.DataFrame:
    # Se convierte la variable date en un TimeStamp de pandas, que es lo que espera la función get_station_kpi_hour()
    # de la clase client, que es la que finalmente envía la petición a la API.
    pd_date = pd.Timestamp(date, tz='Europe/Brussels')
    # Se recoge el dataframe en la variable df
    df = client.get_kpi_hour(station_code, pd_date)
    return df
# Devuelve los datos de cada día del mes que se haya pedido, desde el último día del mes anterior
# hasta el penúltimo del mes pedido
def obtenerDiarios(date:str) -> pd.DataFrame:
    pd_date = pd.Timestamp(date, tz='Europe/Brussels')
    df = client.get_kpi_day(station_code, pd_date)
    return df

# Devuelve el año, desde diciembre pasado a noviembre de la fecha que le pongas, ambos incluidos.
def obtenerMensuales(date:str) -> pd.DataFrame:
    pd_date = pd.Timestamp(date, tz='Europe/Brussels')
    df = client.get_kpi_month(station_code, pd_date)
    return df

# Devuelve los datos de todos los años desde que se instaló el inversor
def obtenerAnuales(date:str) -> pd.DataFrame:
    pd_date = pd.Timestamp(date, tz='Europe/Brussels')
    df = client.get_kpi_year(station_code, pd_date)
    return df

# Se crea una instancia de PandasClient a la que se le llama client dentro de un bloque with para asegurarse de
# que la conexión (client) se cierre automáticamente cuando se cierre el bloque
with PandasClient(user_name=user, system_code=password) as client: 
    sl = client.get_station_list()
    station_code = sl['data'][0]['stationCode']
    #print("El token de la sesión es:",login_response.cookies.get(name='XSRF-TOKEN'))
