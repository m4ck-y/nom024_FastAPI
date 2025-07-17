FROM python:3.13.5-bookworm

# Instala herramientas necesarias para compilar paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    rustc \
    cargo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear el directorio de trabajo
WORKDIR /code

# Copiar e instalar dependencias
COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt

    # Copiar el código fuente
COPY ./app /code/app

# Puerto donde se ejecutará FastAPI
EXPOSE 8000

# Comando para ejecutar Uvicorn con auto-reload (solo en desarrollo)
# En producción, quita `--reload` y usa más workers (--workers N)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]