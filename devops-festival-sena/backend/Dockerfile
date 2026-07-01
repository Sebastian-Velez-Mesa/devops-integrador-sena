# ── Imagen Base Lenta pero Optimizada ────────────────────────────────
FROM python:3.11-slim

# ── Metadatos del Contenedor ──────────────────────────────────────────
LABEL maintainer="SENA DevOps Team <emorenov@sena.edu.co>"
LABEL description="API REST Flask para la sustentación del proyecto integrador DevOps."
LABEL version="1.0.0"

# ── Variables de Entorno de Producción ────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    LOGS_DIR=/app/logs \
    PORT=5000

# ── Directorio de Trabajo ─────────────────────────────────────────────
WORKDIR /app

# ── Dependencias del Sistema (Instalar curl para Healthcheck) ────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Dependencias de Python (Caché de capas) ──────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Copiar el Código Fuente ───────────────────────────────────────────
COPY . .

# Crear el directorio para logs y almacenamiento persistente de volúmenes
RUN mkdir -p /app/logs

# ── Seguridad: Crear usuario no root ─────────────────────────────────
RUN groupadd -r devopsgroup && useradd -r -g devopsgroup devopsuser \
    && chown -R devopsuser:devopsgroup /app

# Cambiar al contexto de usuario seguro
USER devopsuser

# ── Puerto del Contenedor ─────────────────────────────────────────────
EXPOSE 5000

# ── Chequeo de Salud del Contenedor ──────────────────────────────────
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# ── Comando de Entrada (Correr con Gunicorn en producción) ───────────
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
