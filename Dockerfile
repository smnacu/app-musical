# Base con Python
FROM python:3.11-slim

# Ajustes básicos de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ffmpeg para exportar con pydub/librosa
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src ./src
COPY main.py ./

# Nota: Ejecutar GUI en contenedor requiere configuración adicional (X11/WSLg). Por defecto sólo ejecuta CLI de prueba.
CMD ["python", "main.py", "--no-gui"]
