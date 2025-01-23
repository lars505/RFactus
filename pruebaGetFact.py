import requests

# Variables de entorno (usa las mismas del paso anterior)
url_api = "https://api-sandbox.factus.com.co"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZGZjNDczMi1lZmE2LTQ3ODQtOGVmZC02YmRmMWViNWFiMWQiLCJqdGkiOiJiYjU2YTY0N2Y0ODk0MTMzNDBmMmRlY2QzMjE1YmI5MWUyZGQ4YTQzOTkyYjQ2N2RkZjEzOTA2ZjRkMDEzYTY1ODg1MGRjNzE3NDEzNmRkMyIsImlhdCI6MTczNzYxMjkyNC41NzIzNDMsIm5iZiI6MTczNzYxMjkyNC41NzIzNDUsImV4cCI6MTczNzYxNjUyNC41NjM2MDIsInN1YiI6IjMiLCJzY29wZXMiOltdfQ.RPuiGg0HFOWMxMht-7x-_aNlXvTfPcS7oaKITX_Ti2XUD5GDAcXOMIsaqLtSMA3N_re11u2adNcPK9bfiUc7C6e0GJF_SPHn3ZaITkNdLKdbcO3BKtsQ7qMjPZ8JOeAIfhYxDfmD2zFH7k0rKm69UtCS3lDqZbOkGk2asy1AjFt78ATXQ9lmCfBode3VtngY7ejOkAaRVpmre5dZXbB58Pr37oy4eMUOO7SsiRL39O1u7o8cnpq3xPP6J3X93xHqSSUCJc-Q_N87ad0DOUC3XE0zgO4uk9lEfcDB_nZHwo-KO86J3oHz6DJqtsCqR5zgCP_EyxSUVLmf49oDmqpQ5GG7DJFMSpxvy4CXtpj8SXTZyrACaBfZozrvByvr4XcI8OuApylmiDrBgUn37lQ84bg2lyKbZDlAXM3fs-5LvbDkNXYOMf1HK9NM5ZTyoYd5EZsiOR3M1HTT42OP0Zg-q6Y04BNImS1aPxeKKrf2roTPkWb6k_2O_Z6BzokIETiZ8UGlCKfRalgb3rdfv4aKxf5hAeqmipo0i_b--qEya2hI9YCqWEfcqZVKaHDel--opBzPIEet5HXFFWV6JBZYgyhKiTeC9J4cGQkbWe4fJsGccpYJBHdfxuuw9VQNpDmPdRfkPtFZ0FOQ3Wa-O5Y1ReTT34uLG5w0MyLhk_6DvfA"  # Reemplaza esto con el token obtenido anteriormente

# Endpoint para consultar las facturas
bills_url = f"{url_api}/v1/bills"

# Opcional: Parámetros de filtro
params = {
    "filter[identification]": "",  # Agrega el valor correspondiente o déjalo vacío
    "filter[names]": "",
    "filter[number]": "",
    "filter[prefix]": "",
    "filter[reference_code]": "",
    "filter[status]": ""
}

# Headers para la autenticación
headers = {
    "Authorization": f"Bearer {access_token}"
}

try:
    # Solicitud GET para obtener las facturas
    response = requests.get(bills_url, headers=headers, params=params)
    response.raise_for_status()  # Lanza un error si la respuesta no es 2xx

    # Parseamos la respuesta JSON
    bills = response.json()
    print("Facturas obtenidas:", bills.get("data"))

except requests.exceptions.RequestException as e:
    print("Error al obtener las facturas:", e)
