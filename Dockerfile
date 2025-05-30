FROM python:3.13-slim

WORKDIR /app

# Instala herramientas necesarias
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_CREATE=false

# Copia el proyecto
COPY . .

# Instala dependencias sin entorno virtual y sin instalar el paquete raíz
RUN poetry install --no-root --no-interaction --no-ansi

# Expone el puerto del servidor
EXPOSE 8000

# Ejecuta el servidor directamente (porque está instalado en el entorno del sistema)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
