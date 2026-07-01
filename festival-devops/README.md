# 🎵 Festival DevOps Music Fest 2026

> El festival donde la tecnología y la música se fusionan — 3 días · 20+ artistas · Medellín, Colombia

![Estado](https://img.shields.io/badge/estado-activo-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Flask](https://img.shields.io/badge/backend-Flask%203.0-orange)
![GitHub](https://img.shields.io/badge/versionado-Git%20Flow-purple)

---

## 📋 Tabla de Contenidos
- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Docker y Docker Compose](#docker-y-docker-compose)
- [API REST – Endpoints](#api-rest--endpoints)
- [Git y Git Flow](#git-y-git-flow)
- [GitHub – Repositorio Remoto](#github--repositorio-remoto)
- [Cómo ejecutar el proyecto](#cómo-ejecutar-el-proyecto)

---

## 📖 Descripción

**Festival DevOps Music Fest 2026** es una aplicación web full-stack que simula el portal oficial de un festival de música con temática DevOps. Incluye una landing page con cuenta regresiva, catálogo de artistas con filtros, sistema de tickets con modal de compra y formulario de contacto con FAQ interactivo.

Este proyecto fue desarrollado como práctica de **Git Flow**, **Docker**, **Docker Compose** y **GitHub**.

---

## 🛠️ Tecnologías

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Frontend** | HTML5 + CSS3 (Vanilla) | — |
| **Backend** | Python + Flask | 3.11 / 3.0.3 |
| **Servidor WSGI** | Gunicorn | 22.0.0 |
| **Contenedores** | Docker | 25+ |
| **Orquestación** | Docker Compose | v3.8 |
| **Red Docker** | Bridge (`festival-net`) | — |
| **Volúmenes** | Named volume (`festival-backend-logs`) | — |
| **Control de versiones** | Git + Git Flow básico | 2.x |
| **Repositorio remoto** | GitHub | — |

---

## 📁 Estructura del Proyecto

```
festival-devops/
├── frontend/
│   ├── index.html        ← Landing page principal con countdown
│   ├── style.css         ← Hoja de estilos global (dark mode + animaciones)
│   ├── artistas.html     ← Lineup con filtros por escenario
│   ├── tickets.html      ← Compra de entradas con modal
│   └── contacto.html     ← Formulario de contacto + FAQ
├── backend/
│   ├── app.py            ← API REST Flask con 5 endpoints
│   ├── requirements.txt  ← Dependencias Python
│   └── Dockerfile        ← Imagen Docker del backend
├── docker-compose.yml    ← Orquestación de servicios
└── README.md             ← Este archivo
```

---

## 🐳 Docker y Docker Compose

### Dockerfile del Backend

El archivo `backend/Dockerfile` construye una imagen basada en `python:3.11-slim`:

- **Multi-layer caching**: copia `requirements.txt` antes del código fuente
- **Gunicorn**: servidor WSGI de producción con 2 workers
- **Healthcheck**: verifica `/health` cada 30 segundos
- **Volumen**: persiste logs en `/app/logs`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Docker Compose

El archivo `docker-compose.yml` define **2 servicios**:

| Servicio | Imagen | Puerto | Descripción |
|---------|--------|--------|-------------|
| `festival-frontend` | `nginx:alpine` | `8080:80` | Sirve los archivos estáticos del frontend |
| `festival-backend` | Build local | `5000:5000` | API REST Flask |

**Red**: Ambos servicios comparten la red `festival-net` (bridge)  
**Volumen**: `festival-backend-logs` persiste los logs del backend

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

---

## 🔌 API REST – Endpoints

Base URL: `http://localhost:5000`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Info general de la API |
| `GET` | `/health` | Health check del servicio |
| `GET` | `/api/festival` | Información del festival |
| `GET` | `/api/artistas` | Lista todos los artistas |
| `GET` | `/api/artistas?escenario=Principal` | Filtra artistas por escenario |
| `GET` | `/api/artistas/:id` | Detalle de un artista |
| `GET` | `/api/tickets` | Tipos de tickets disponibles |
| `POST` | `/api/contacto` | Enviar mensaje de contacto |

**Ejemplo POST `/api/contacto`:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "mensaje": "¿Hay descuentos para grupos?"
}
```

---

## 🌿 Git y Git Flow

Este proyecto siguió el flujo **Git Flow básico**:

```
main
 │
 ├── feature-landing    → index.html + style.css
 ├── feature-backend    → app.py + requirements.txt + Dockerfile
 ├── feature-artistas   → artistas.html  (Reto Avanzado)
 ├── feature-tickets    → tickets.html   (Reto Avanzado)
 └── feature-contacto   → contacto.html  (Reto Avanzado)
```

### Comandos utilizados

```bash
# Inicializar repositorio
git init
git config user.name "Festival DevOps"
git config user.email "devops@festival.com"

# Primer commit
git add .
git commit -m "Estructura inicial del proyecto"

# Crear y usar ramas feature
git checkout -b feature-landing
git add .
git commit -m "Se agrega landing page del festival"

git checkout -b feature-backend
git add .
git commit -m "Se agrega API Flask"

# Merge a main
git checkout main
git merge feature-landing
git merge feature-backend

# Reto Avanzado
git checkout -b feature-artistas
git commit -m "Se agrega pagina de artistas"
git checkout main && git merge feature-artistas

git checkout -b feature-tickets
git commit -m "Se agrega pagina de tickets"
git checkout main && git merge feature-tickets

git checkout -b feature-contacto
git commit -m "Se agrega pagina de contacto"
git checkout main && git merge feature-contacto
```

### Historial de commits

```
c3fae6f  Se agrega pagina de contacto
2937257  Se agrega pagina de tickets
2a0dfb4  Se agrega pagina de artistas
ef16472  Se agrega API Flask
92e2691  Se agrega landing page del festival
f19b831  Estructura inicial del proyecto
```

---

## 🐙 GitHub – Repositorio Remoto

```bash
# Vincular con repositorio remoto
git remote add origin https://github.com/Sebastian-Velez-Mesa/nose.git

# Publicar rama main
git push -u origin main
```

**Repositorio:** [github.com/Sebastian-Velez-Mesa/nose](https://github.com/Sebastian-Velez-Mesa/nose)

---

## 🚀 Cómo ejecutar el proyecto

### Opción 1 – Con Docker Compose (recomendado)

```bash
git clone https://github.com/Sebastian-Velez-Mesa/nose.git festival-devops
cd festival-devops
docker-compose up -d
```

- Frontend: [http://localhost:8080](http://localhost:8080)
- Backend API: [http://localhost:5000](http://localhost:5000)

### Opción 2 – Backend local (sin Docker)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Opción 3 – Frontend estático

Abrir directamente `frontend/index.html` en el navegador.

---

## 👥 Equipo

Desarrollado por el equipo **Festival DevOps** como práctica del laboratorio de Git Flow y Docker.

---

*© 2026 Festival DevOps Music Fest · Hecho con ❤️, Flask y Docker*
