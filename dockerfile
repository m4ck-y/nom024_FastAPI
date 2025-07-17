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

CMD ["python", "-m", "app.main"]