import logging
from functools import wraps
from time import sleep
from typing import Dict
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests
import datetime


class HTTPError(Exception):
    pass


class HTTPError407(HTTPError):
    pass

class HTTPError305(HTTPError):
    pass

class HTTPError306(HTTPError):
    pass

class HTTPError307(HTTPError):
    pass

class HTTPError401(HTTPError):
    pass

def authenticated(func):
    """
    Decorator to check if token has expired.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.token_expiration_time <= pd.Timestamp.utcnow().timestamp():
            self.login()
        return func(*args, **kwargs)

    return wrapper


def throttle_retry(func):
    """
    Decorator to retry when throttleError is received.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except HTTPError407 as e:
            for i in range(1, self.max_retry + 1):
                delay = i * 3
                logging.debug(f'Sleeping {delay} seconds')
                sleep(delay)
                try:
                    return func(*args, **kwargs)
                except HTTPError407:
                    pass
            else:
                raise e
        except (HTTPError305, HTTPError306, HTTPError307) as e:
            # Token as expired or we aren't logged in.. Refresh it.
            logging.debug("Got login error. Logging back in and retrying")
            self.login()
            return func(*args, **kwargs)

    return wrapper

 
class Client:
    def __init__(
            self,
            user_name: str,
            system_code: str,
            max_retry: int = 10,
            base_url: str = "https://intl.fusionsolar.huawei.com/thirdData"
    ):
        self.user_name = user_name
        self.system_code = system_code
        self.max_retry = max_retry
        self.base_url = base_url

        self.session = requests.session()
        self.session.headers.update(
            {'Connection': 'keep-alive', 'Content-Type': 'application/json'})

        self.token_expiration_time = 0

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def login(self):
        url = f'{self.base_url}/login'
        body = {
            'userName': self.user_name,
            'systemCode': self.system_code
        }
        self.session.cookies.clear()
        r = self.session.post(url=url, json=body)
        self._validate_response(response=r)
        self.session.headers.update(
            {'XSRF-TOKEN': r.cookies.get(name='XSRF-TOKEN')})
        self.token_expiration_time = pd.Timestamp.utcnow().timestamp() + 1200
        return r

    @staticmethod
    def _validate_response(response: requests.Response) -> bool:
        response.raise_for_status()
        body = response.json()
        success = body.get('success', False)
        if not success:
            if body.get('failCode') == 407:
                logging.debug('Error 407')
                raise HTTPError407(body)
            elif body.get('failCode') == 305:
                logging.debug('Error 305')
                raise HTTPError306(body)
            elif body.get('failCode') == 306:
                logging.debug('Error 306')
                raise HTTPError306(body)
            elif body.get('failCode') == 307:
                logging.debug('Error 307')
                raise HTTPError306(body)
            elif body.get('failCode') == 401:
                logging.debug('Error 401')
                raise HTTPError401
            else:
                raise HTTPError(body)
        else:
            return True

    @throttle_retry
    @authenticated
    def _request(self, function: str, data=None) -> Dict:
        if data is None:
            data = {}
        url = f'{self.base_url}/{function}'
        r = self.session.post(url=url, json=data)
        self._validate_response(r)
        return r.json()

    def get_station_list(self) -> Dict:
        res = self._request("getStationList")
        return res

    def get_station_kpi_real(self, station_code: str) -> Dict:
        return self._request("getStationRealKpi",
                             {'stationCodes': station_code})

    def get_station_kpi_hour(self, station_code: str,
                             date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getKpiStationHour", {'stationCodes': station_code,
                                                   'collectTime': time})

    def get_station_kpi_day(self, station_code: str,
                            date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getKpiStationDay", {'stationCodes': station_code,
                                                  'collectTime': time})

    def get_station_kpi_month(self, station_code: str,
                              date: pd.Timestamp) -> Dict:
        time = int(date.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
        return self._request("getKpiStationMonth",
                             {'stationCodes': station_code,
                              'collectTime': time})

    def get_station_kpi_year(self, station_code: str,
                             date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getKpiStationYear", {'stationCodes': station_code,
                                                   'collectTime': time})

    def get_dev_list(self, station_code) -> Dict:
        return self._request("getDevList", {'stationCodes': station_code})

    def get_dev_kpi_real(self, dev_id: str, dev_type_id: int) -> Dict:
        return self._request("getDevRealKpi",
                             {'devIds': dev_id, 'devTypeId': dev_type_id})

    def get_dev_kpi_fivemin(self, dev_id: str, dev_type_id: int,
                            date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getDevFiveMinutes",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'collectTime': time})

    def get_dev_kpi_hour(self, dev_id: str, dev_type_id: int,
                         date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getDevKpiHour",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'collectTime': time})

    def get_dev_kpi_day(self, dev_id: str, dev_type_id: int,
                        date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getDevKpiDay",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'collectTime': time})

    def get_dev_kpi_month(self, dev_id: str, dev_type_id: int,
                          date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getDevKpiMonth",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'collectTime': time})

    def get_dev_kpi_year(self, dev_id: str, dev_type_id: int,
                         date: pd.Timestamp) -> Dict:
        time = int(date.timestamp()) * 1000
        return self._request("getDevKpiYear",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'collectTime': time})

    def dev_on_off(self, dev_id: str, dev_type_id: int,
                   control_type: int) -> Dict:
        # control_type
        # 1: power-on
        # 2: power-off
        return self._request("devOnOff",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'controlType': control_type})

    def dev_upgrade(self, dev_id: str, dev_type_id: int) -> Dict:
        return self._request("devUpgrade",
                             {'devIds': dev_id, 'devTypeId': dev_type_id})

    def get_dev_upgradeinfo(self, dev_id: str, dev_type_id: int) -> Dict:
        return self._request("getDevUpgradeInfo",
                             {'devIds': dev_id, 'devTypeId': dev_type_id})


class PandasClient(Client):

    # Transforma el JSON "j" de parámetro a un diccionario para simplificar el manejo
    # de los datos. Este diccionario se contruye dinámicamente durante el bucle con la 
    # sentencia yield y se devuelve completo al finalizar la función
    def flatten_data(self, j): 
            for point in j['data']:
                line = {'collectTime': point['collectTime']}
                line.update(point['dataItemMap'])
                yield line



    # Función auxiliar que llama a la función get_station_kpi_hour() y convierte su salida 
    # en un diccionario mediante la función flatten_data para convertirlo en un DataFrame de Pandas
    # Posteriormente se modifica el DataFrame para que la columna collectData sea tratada igual que las demás
    # y no se le de un tratamiento distinto al ser un eje temporal. Se hace esto para simplificar el manejo 
    # posterior de los datos
    def get_kpi_hour(self, station_code: str,
                    date: pd.Timestamp) -> pd.DataFrame:
        data = super(PandasClient, self).get_station_kpi_hour(
            station_code=station_code, date=date)
        if len(data['data']) == 0:
            return pd.DataFrame()
        df = pd.DataFrame(self.flatten_data(data))
        df['collectTime'] = pd.to_datetime(df['collectTime'], unit='ms',
                                           utc=True)
        df.set_index('collectTime', inplace=True)
        df = df.astype(float)
        return df
    

    # Función auxiliar que llama a la función get_station_kpi_day() y convierte su salida 
    # en un diccionario mediante la función flatten_data para convertirlo en un DataFrame de Pandas
    # Posteriormente se modifica el DataFrame para que la columna collectData sea tratada igual que las demás
    # y no se le de un tratamiento distinto al ser un eje temporal. Se hace esto para simplificar el manejo 
    # posterior de los datos
    def get_kpi_day(self, station_code: str,
                    date: pd.Timestamp) -> pd.DataFrame:
        data = super(PandasClient, self).get_station_kpi_day(
            station_code=station_code, date=date)
        if len(data['data']) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(self.flatten_data(data))
        df['collectTime'] = pd.to_datetime(df['collectTime'], unit='ms',
                                           utc=True)
        df['collectTime'] = df['collectTime'].apply(lambda x: x + relativedelta(days=1))
        df.set_index('collectTime', inplace=True)
        df = df.astype(float)
        return df
    



    # Función auxiliar que llama a la función get_station_kpi_month() y convierte su salida 
    # en un diccionario mediante la función flatten_data para convertirlo en un DataFrame de Pandas
    # Posteriormente se modifica el DataFrame para que la columna collectData sea tratada igual que las demás
    # y no se le de un tratamiento distinto al ser un eje temporal. Se hace esto para simplificar el manejo 
    # posterior de los datos
    def get_kpi_month(self, station_code: str,
                    date: pd.Timestamp) -> pd.DataFrame:
        
        data = super(PandasClient, self).get_station_kpi_month(
            station_code=station_code, date=date)
        
        for item in data["data"]:
            collect_time = item["collectTime"]

        if len(data['data']) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(self.flatten_data(data))
        df['collectTime'] = pd.to_datetime(df['collectTime'], unit='ms',
                                           utc=True)
        # Se necesita añadir un mes a la fecha puesto que la API lo devuelve un mes antes de la fecha real
        df['collectTime'] = df['collectTime'].apply(lambda x: x + relativedelta(months=1))
        df.set_index('collectTime', inplace=True)
        df = df.astype(float)
        return df
    


    # Función auxiliar que llama a la función get_station_kpi_year() y convierte su salida 
    # en un diccionario mediante la función flatten_data para convertirlo en un DataFrame de Pandas
    # Posteriormente se modifica el DataFrame para que la columna collectData sea tratada igual que las demás
    # y no se le de un tratamiento distinto al ser un eje temporal. Se hace esto para simplificar el manejo 
    # posterior de los datos
    def get_kpi_year(self, station_code: str,
                    date: pd.Timestamp) -> pd.DataFrame:
        data = super(PandasClient, self).get_station_kpi_year(
            station_code=station_code, date=date)
        if len(data['data']) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(self.flatten_data(data))
        df['collectTime'] = pd.to_datetime(df['collectTime'], unit='ms',
                                           utc=True)
        # Se necesita añadir un año a la fecha puesto que la API lo devuelve un año antes de la fecha real
        df['collectTime'] = df['collectTime'].apply(lambda x: x + relativedelta(years=1))
        df.set_index('collectTime', inplace=True)
        df = df.astype(float)
        return df
    

    # Simplemente llama a la función get_station_kpi_real() y devuelve su resultado. 
    # Se ha codificado de esta manera para seguir la metodlogía que se ha utilizado con 
    # el resto de los datos, pero en este caso no hace falta ninguna modificación de estos
    def get_kpi_real(self, station_code: str):
        return super(PandasClient, self).get_station_kpi_real(station_code=station_code)
