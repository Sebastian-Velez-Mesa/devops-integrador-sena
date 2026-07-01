# ── Imagen Base Ultra Ligera ─────────────────────────────────────────
FROM nginx:alpine

# ── Metadatos del Servidor Web ───────────────────────────────────────
LABEL maintainer="SENA DevOps Team <emorenov@sena.edu.co>"
LABEL description="Servidor Nginx para distribuir los recursos estáticos del Frontend."
LABEL version="1.0.0"

# ── Copiar Archivos Estáticos ─────────────────────────────────────────
# La compilación se hace desde el contexto de la carpeta /frontend
COPY . /usr/share/nginx/html

# Ajustar permisos para el usuario `nginx` y añadir healthcheck
RUN chown -R nginx:nginx /usr/share/nginx/html || true

# ── Puertos Expuestos ─────────────────────────────────────────────────
EXPOSE 80

# ── Healthcheck simple ───────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
	CMD wget -qO- --timeout=2 http://localhost:80/ >/dev/null || exit 1

# ── Comando de Ejecución ──────────────────────────────────────────────
CMD ["nginx", "-g", "daemon off;"]
