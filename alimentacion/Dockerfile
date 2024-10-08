# Usar una imagen oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /alimentacion

# Actualizar e instalar dependencias del sistema necesarias para algunas bibliotecas como pandas
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos del proyecto a la imagen de Docker
COPY . /alimentacion

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que utilizará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

