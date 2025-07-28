import requests
import base64
from datetime import datetime, timedelta




#------------------------------------------------------------------------------------------------------------
# Pedir a la API que me devuelva un token 
def idealista_token(api_key, secret):
    """ Request a token from OAuth authentification

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




filter_request = {
    "country": "es",
    "operation": "sale",
    "propertyType": "homes",
    
}
