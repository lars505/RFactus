import requests
import time
from django.conf import settings


class FactusAPI:
    _access_token = None  
    _token_expires_at = 0  

    def __init__(self):
        self.base_url = settings.API_URL
        self.username = settings.API_USERNAME
        self.password = settings.API_PASSWORD
        self.client_id = settings.API_CLIENT_ID
        self.client_secret = settings.API_CLIENT_SECRET

    def _generate_token(self):
        """
        Genera un nuevo access_token y almacena su tiempo de expiración.
        """
        url = f"{self.base_url}/oauth/token"
        payload = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(url, data=payload)
        response.raise_for_status()  

        tokens = response.json()

        FactusAPI._access_token = tokens.get("access_token")

        expires_in = tokens.get("expires_in", 3600)  # Por defecto, 1 hora

        FactusAPI._token_expires_at = time.time() + expires_in

    def get_access_token(self):
        """
            Devuelve un token válido (lo genera si ha expirado o no existe).
        """
        if not FactusAPI._access_token or FactusAPI._token_expires_at <= time.time():
            self._generate_token()
        return FactusAPI._access_token

    def request(self, method, endpoint, params=None, data=None):
        """
        Realiza una solicitud genérica a la API.

        Args:
            method (str): Método HTTP (GET, POST, etc.).
            endpoint (str): Endpoint de la API (ej. '/v1/bills').
            params (dict): Query parameters.
            data (dict): Datos para el cuerpo de la solicitud.

        Returns:
            dict: Respuesta JSON de la API.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.request(method, url, headers=headers, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud a {url}: {e}")
            raise e
