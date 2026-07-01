# DevOps Festival - Demo y pasos de presentación

Este repositorio contiene la aplicación del proyecto integrador DevOps (Backend Flask + Frontend Nginx) y los artefactos necesarios para la demostración.

Requisitos previos
- Docker y Docker Compose instalados
- PowerShell (Windows) o Bash (Linux/macOS)

Arranque rápido (local)

1. Construir y levantar los servicios:

```powershell
docker compose up --build -d
```

2. Comprobar contenedores e imágenes:

```powershell
docker ps --format "table {{.Names}}	{{.Image}}	{{.Status}}"
docker images --format "table {{.Repository}}	{{.Tag}}	{{.Size}}"
```

3. Chequear health endpoints:

```powershell
curl http://localhost:5000/health
curl http://localhost:8080/  # frontend
```

Evidencias a capturar para la sustentación
- Lista de contenedores (`docker ps`)
- Imágenes (`docker images`)
- Redes Docker (`docker network ls`)
- Volúmenes Docker (`docker volume ls`)
- Logs del backend (`docker logs <backend-container>`)
- Historial de commits (`git log --oneline --graph --all`)
- Branches (`git branch -a`)
- Resultado del pipeline (GitHub Actions) — ver `.github/workflows/ci-cd.yml`

Pruebas locales

```powershell
pytest backend/test_app.py
```

Archivos importantes
- `backend/` – API Flask
- `frontend/` – HTML + recursos servidos por Nginx
- `.github/workflows/ci-cd.yml` – pipeline CI/CD de ejemplo
- `docker-compose.yml` – orquestación multicontenedor

Preparar entrega
- Generar un archivo ZIP del repositorio o proporcionar el enlace al repositorio en GitHub.
- Enviar por correo a `emorenov@sena.edu.co` el ZIP o enlace, presentación (PPTX/PDF) y documento técnico.

Guía rápida de la demo (30 minutos)
- 0–5 min: Introducción y objetivo del proyecto
- 5–15 min: Arquitectura y decisiones técnicas
- 15–25 min: Demostración en vivo (arranque, comprobaciones, logs)
- 25–30 min: Conclusiones y mejoras futuras

---
Generado automáticamente como soporte para la sustentación.
# 🎵 SENA DevOps & Cloud Fest 2026

> Proyecto Integrador de Aprendizaje: Sustentación Técnica de DevOps, Contenedores Docker, Redes, Volúmenes y CI/CD con GitHub Actions.

Este repositorio contiene la entrega completa del proyecto DevOps consolidado de manera independiente en el directorio `devops-festival-sena`, cumpliendo con todos los criterios de evaluación del Centro de Tecnología y Manufactura Avanzada (SENA).

---

## 📋 Tabla de Contenidos
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instrucciones de Despliegue Rápido](#-instrucciones-de-despliegue-rápido)
- [Fases de la Demostración en Vivo](#-fases-de-la-demostración-en-vivo)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Verificación de Persistencia y Logs](#-verificación-de-persistencia-y-logs)
- [Contacto para la Entrega](#-contacto-para-la-entrega)

---

## 📁 Estructura del Proyecto

```
devops-festival-sena/
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # Integración Continua (Linter + Tests + Build)
├── backend/
│   ├── app.py                    # REST API Flask con persistencia local
│   ├── requirements.txt          # Dependencias de Python
│   ├── test_app.py               # Suite de Pruebas Unitarias (pytest)
│   └── Dockerfile                # Imagen Backend optimizada (non-root + healthcheck)
├── frontend/
│   ├── index.html                # Landing Page + Dashboard DevOps en tiempo real
│   ├── artistas.html             # Listado de artistas dinámico con filtros
│   ├── tickets.html              # Venta de tickets con checkout interactivo
│   ├── contacto.html             # Formulario de contacto y acordeón FAQ
│   ├── style.css                 # Diseño moderno con glassmorphism
│   └── Dockerfile                # Servidor web Nginx Alpine
├── scripts/
│   ├── generate_presentation.py  # Generador automático de PowerPoint (PPTX)
│   └── simulate_git_history.ps1  # Inicializador de Git con historial de Git Flow
├── docker-compose.yml            # Orquestación multicontenedor de la red y volúmenes
├── .env.template                 # Plantilla de variables de entorno
├── DOCUMENTACION.md              # Documento técnico detallado de decisiones de diseño
└── README.md                     # Guía de inicio rápido (Este archivo)
```

---

## 🛠️ Requisitos Previos

Para ejecutar y probar la solución completa, debes tener instalado:
* **Docker Desktop** (con Docker Compose v2+)
* **Python 3.11** (o superior)
* **PowerShell** (para ejecutar scripts en Windows) o Git Bash

---

## 🚀 Instrucciones de Despliegue Rápido

Sigue estos sencillos pasos para preparar y arrancar todo el proyecto desde la terminal:

### Paso 1: Generar la Presentación PowerPoint oficial
Genera automáticamente las diapositivas para la exposición ejecutando el script python:
```bash
python scripts/generate_presentation.py
```
*Esto instalará automáticamente `python-pptx` si no está presente en tu sistema y creará el archivo `Sustentacion_DevOps.pptx` en la raíz del proyecto.*

### Paso 2: Recrear el Historial de Git (Git Flow)
Si deseas recrear el árbol gráfico de ramas y commits de manera limpia en tu entorno local para la sustentación, abre PowerShell como Administrador en Windows y ejecuta:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\simulate_git_history.ps1
```
*Este comando inicializa Git localmente, crea el archivo `.gitignore` y recrea la red de ramas (`develop`, `feature-backend`, `feature-frontend`, etc.) con sus respectivos fusiones (`merges`) sin Fast-Forward.*

### Paso 3: Lanzar los Contenedores con Docker Compose
Para compilar y levantar los microservicios en segundo plano, corre:
```bash
docker compose up --build -d
```
*Este comando construirá las imágenes del frontend (Nginx) y backend (Flask), creará la red privada `devops-network` y levantará el volumen `devops-backend-logs`.*

---

## 🖥️ Fases de la Demostración en Vivo

Una vez desplegada la aplicación, podrás sustentarla en base a las siguientes direcciones:

1. **Frontend del Festival & Dashboard DevOps:**
   * Abre en tu navegador: `http://localhost:8080`
   * En la página de inicio, desplázate hasta la sección **DevOps Live Monitor**. Verás métricas del backend en vivo (OS, peticiones totales, uptime del contenedor) y un visor de logs emulado que actualiza en tiempo real cada 3 segundos.
2. **Lineup de Artistas (API REST):**
   * Navega a `http://localhost:8080/artistas.html`
   * Los artistas se cargan mediante peticiones asíncronas desde `http://localhost:5000/api/artistas`. Puedes filtrarlos dinámicamente por escenario. Si apagas el contenedor backend, verás que el frontend activa el modo *Offline Fallback*.
3. **Reserva e Inserción de Datos en el Volumen:**
   * Navega a `http://localhost:8080/tickets.html` u `http://localhost:8080/contacto.html` y envía datos mediante los formularios.
   * Verás alertas que confirman el almacenamiento exitoso en el volumen de Docker. Al instante, el Live Monitor de la página de inicio mostrará que el contador de registros subió.

---

## 🔌 Endpoints de la API

La API Backend expone los siguientes endpoints públicos en `http://localhost:5000`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Información del servicio |
| `GET` | `/health` | Chequeo de salud del contenedor (usado por Docker Healthcheck) |
| `GET` | `/api/festival` | Información general del festival |
| `GET` | `/api/artistas` | Lista todos los artistas (filtrable por `?escenario=devops stage`) |
| `GET` | `/api/tickets` | Tipos de tickets y pases de acceso |
| `POST` | `/api/contacto` | Registro de reservas y contactos (Escribe en el volumen persistente) |
| `GET` | `/api/stats` | Estadísticas DevOps internas en formato JSON para el frontend |

---

## 💾 Verificación de Persistencia y Logs

Para demostrar la persistencia de datos al comité evaluador:

1. Realiza algunas reservas en la sección de Tickets.
2. Comprueba la persistencia apagando el contenedor:
   ```bash
   docker compose down
   ```
3. Levántalo de nuevo:
   ```bash
   docker compose up -d
   ```
4. Recarga la página y verifica que el contador de registros en el Dashboard y los datos anteriores sigan intactos, ya que están almacenados en el volumen persistente `devops-backend-logs`.
5. Revisa los logs internos del backend en tiempo real con:
   ```bash
   docker compose logs -f backend
   ```

---

## 📧 Contacto para la Entrega

El proyecto consolidado listo para calificar debe enviarse por correo electrónico según las pautas de SENA:
* **Destinatario:** emorenov@sena.edu.co
* **Asunto:** Entrega Proyecto Final DevOps - Grupo [Nombre de tu Equipo]
* **Contenido:** Repositorio GitHub remoto, Documento Técnico (`DOCUMENTACION.md`), Presentación generada (`Sustentacion_DevOps.pptx`) y evidencias de ejecución.

---
*Hecho colaborativamente bajo la filosofía DevOps - SENA CTMA 2026.*
