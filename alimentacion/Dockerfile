# Usar una imagen oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /alimentacion

# Copiar los archivos del proyecto a la imagen de Docker
COPY . /alimentacion

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
