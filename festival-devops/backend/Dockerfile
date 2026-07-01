# ── Imagen base ──────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Metadatos ────────────────────────────────────────────────────────
LABEL maintainer="Festival DevOps Team"
LABEL description="API Backend – Festival DevOps Music Fest 2026"
LABEL version="1.0.0"

# ── Variables de entorno ─────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# ── Directorio de trabajo ────────────────────────────────────────────
WORKDIR /app

# ── Dependencias del sistema ─────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Dependencias Python ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Código fuente ────────────────────────────────────────────────────
COPY . .

# ── Volumen para logs y usuario no root ─────────────────────────────────
RUN mkdir -p /app/logs
VOLUME ["/app/logs"]

# Crear usuario no root y asignar permisos al directorio de la aplicación
RUN groupadd -r devopsgroup && useradd -r -g devopsgroup devopsuser \
    && chown -R devopsuser:devopsgroup /app

# Cambiar al usuario no root
USER devopsuser

# ── Puerto expuesto ───────────────────────────────────────────────────
EXPOSE 5000

# ── Health check ──────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# ── Comando de inicio ─────────────────────────────────────────────────
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
