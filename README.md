# Weather API

REST API para obtener las condiciones climaticas de los proximos siete dias segun una ciudad.

Puedes ver la documentacion de la API en este [Link](
https://linear-fancy-ligoriostest-a42e221d.koyeb.app/docs)

## Requisitos

- Python 3.10+
- Django 4.x
- Docker (opcional, para la ejecución en contenedores)


## Setup

- Para ambos pasos hay que crear un archivo `.env` en la raiz del proyecto con esta estructura

```env
    WEATHER_API_KEY='my api key'
```

### docker

 ```bash
   docker-compose up --build
```
###  virtualenv

1. Crear un entorno virtual

```bash
python3 -m venv env
source env/bin/activate
```
2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Correr Migraciones y runserver

```bash
python manage.py migrate
python manage.py runserver
```

## Test

Para correr los test solo se tiene que ejectura 

```bash
pytest
```





