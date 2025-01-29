# Proyecto Django - Integración con API de Facturación

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2%2B-green)](https://www.djangoproject.com/)

Este proyecto Django permite consumir una API externa de facturación y validar la información de facturas electrónicas. Incluye funcionalidades para crear, validar y gestionar facturas siguiendo los estándares requeridos por la autoridad tributaria local.

## Características Principales

- ✅ Validación de estructura de facturas electrónicas
- 🚀 Consumo de API externa de facturación
- 📦 Creación de facturas
- 📄 Listado y facturas generadas
- 🔒 Manejo seguro de credenciales de API

## Requisitos Previos

- Python 3.8 o superior
- Django 3.2 o superior
- Biblioteca `requests` para consumo de APIs
- Credenciales de acceso a la API de facturación

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/lars505/RFactus.git
cd Rfactus
```
2. Crear y Activar el Entorno Virtual 
``` bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

# Configuracion

1. Crear archivo .env en el directorio principal con las variables de entorno:
```bash
username=
grandtype=
url_api=https:
email=
password=
client_id=
client_secret=
```
2.Configurar las variables en settings.py:

```bash
API_URL = config('url_api')
API_USERNAME = config('username')
API_PASSWORD = config('password')
API_CLIENT_ID = config('client_id')
API_CLIENT_SECRET = config('client_secret')
```

# Uso

1. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```
# Contribución

  1. Haz fork del proyecto

  2. Crea una rama (git checkout -b feature/nueva-funcionalidad)

  3. Realiza tus cambios

  4. Haz commit de los cambios (git commit -am 'Agrega nueva funcionalidad')

  5. Haz push a la rama (git push origin feature/nueva-funcionalidad)

  6. Abre un Pull Request














