# Usar una imagen oficial de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación al contenedor
COPY /APP-Emergsys .

# Exponer el puerto en el que Flask servirá la aplicación
EXPOSE 5000

# Configurar las variables de entorno necesarias (opcional)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Definir el comando por defecto para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
