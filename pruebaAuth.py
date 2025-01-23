import requests
import os

# Variables de entorno (puedes cargarlas desde un .env si prefieres)
username = "sandbox@factus.com.co"
password = "sandbox2024%"
client_id = "9dfc4732-efa6-4784-8efd-6bdf1eb5ab1d"
client_secret = "74W9Cw0uwaR9Pg8Zw97koo5ZLOvoyu7jtvTkA59I"
url_api = "https://api-sandbox.factus.com.co"
grant_type = "password"

# Endpoint para autenticar
auth_url = f"{url_api}/oauth/token"

# Data para enviar en la petición
payload = {
    "grant_type": grant_type,
    "username": username,
    "password": password,
    "client_id": client_id,
    "client_secret": client_secret
}

try:
    # Solicitud POST para obtener los tokens
    response = requests.post(auth_url, data=payload)
    response.raise_for_status()  # Lanza un error si la respuesta no es 2xx

    # Parseamos la respuesta JSON
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

except requests.exceptions.RequestException as e:
    print("Error al autenticar:", e)
