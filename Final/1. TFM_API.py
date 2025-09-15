import os
from dotenv import load_dotenv

import pandas as pd
from datetime import datetime, timedelta

import base64
import requests

# Este codigo se deberá ejecutar para cada par API-key secret, debido al cambio en las variables de entorno.
# Además se deberá cambiar también el número de las páginas
#------------------------------------------------------------------------------------------------------------
# Pedir a la API que me devuelva un token
def idealista_token(api_key, secret):
    """ Obtiene un token de acceso desde la API de Idealista usando OAuth2

    Parameters
    ----------
    api_key(str): Api key
    secret(str): secreto

    Returns
    -------
    access_token, fecha caducidad
    """
    real_credentials = api_key+":"+secret
    base64_bytes = base64.b64encode(real_credentials.encode("ascii"))
    credentials = base64_bytes.decode("ascii")


    req = requests.post(
        "https://api.idealista.com/oauth/token",
        "grant_type=client_credentials&scope=read",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    ).json()
    return req["access_token"], datetime.now() + timedelta(seconds=req["expires_in"])

#--------------------------------------------------------------------------------------------------------------
# Realiza una consulta a la API de idealista
def query(token, request):
    """Realiza una consulta a la API de idealista
    Parameter
    ---------
    token: token recibido por la API de outhenticator
    request: diccionario con los datos de la solicitud

    Returns
    -------
    Devuelve la respuesta de la API
    """

    response = requests.post(
            "https://api.idealista.com/3.5/es/search",
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "curl/8.3.0"
            },
            data=request,
        )
    return response.json()


# Accedemos a las varibles de entorno y las guardamos en variables locales
load_dotenv()
api_key = os.getenv("api_key")
secret = os.getenv("secret")


# Hacemos un bucle para acceder en cada token a una página distinta
# Aquí se deberán elegir las páginas que deseamos ver.
for num_page in range(201,301):
    # Filtro con los anuncios que queremos recopilar
    filter_request = {
        "country": "es",
        "operation": "sale",
        "propertyType": "homes",
        "locationId": "0-EU-ES-28",
        "maxItems": 50,
        "numPage": num_page
    }
    token, expires = idealista_token(api_key, secret)
    print(token)
    response = query(token, filter_request)

    # Lista de viviendas dentro del JSON
    viviendas = response["elementList"]

    # Usamos json_normalize con sep='.' para que las claves anidadas se aplanen con ese separador
    df = pd.json_normalize(viviendas, sep='.')

    df.to_csv(f"data2/datos_separados/datos_sec_pag_{num_page}.csv", index=False)