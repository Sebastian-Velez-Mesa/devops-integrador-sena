# Documento Técnico: Decisiones de Diseño e Infraestructura DevOps

## 1. Introducción y Propósito
Este documento técnico recopila y justifica las decisiones de diseño de software, arquitectura de contenedores e integración continua (CI/CD) adoptadas para el desarrollo del portal **SENA DevOps & Cloud Fest 2026** (directorio de entrega: `devops-festival-sena`). 

El objetivo principal es sustentar ante el comité evaluador de la tecnología cómo el proyecto incorpora las mejores prácticas de la cultura DevOps moderno: automatización, aislamiento, reproducibilidad, seguridad, persistencia de datos y chequeo proactivo de fallos.

---

## 2. Arquitectura de la Solución y Flujo de Información
El proyecto implementa una arquitectura desacoplada basada en microservicios contenerizados y orquestados por Docker Compose:

```
                  Peticiones HTTP (Puerto 8080)
      [Usuario] ─────────────────────────────────> [devops-frontend]
                                                        │ (Servidor Nginx Alpine)
                                                        │
                                                        │ Peticiones AJAX / API REST (Puerto 5000)
                                                        ▼ (Usando DNS Interno en Red Bridge)
                                                   [devops-backend]
                                                        │ (Flask API / Gunicorn WSGI)
                                                        │
                                    Escritura Logs      │ Persistencia Contactos
                                    y Métricas          ▼ (Volumen con Nombre)
                                              [devops-backend-logs]
                                               (contactos.json & festival.log)
```

### Flujo de Información
1. **Acceso de Usuario (Frontend):** El usuario ingresa a `http://localhost:8080`. El servidor **Nginx Alpine** despacha los recursos estáticos (HTML, CSS y JS).
2. **Dashboard DevOps en Vivo:** El Javascript del navegador realiza peticiones AJAX periódicas (cada 3 segundos) hacia la API REST del backend (`http://localhost:5000/api/stats` y `/health`). Los datos se procesan y pintan dinámicamente en el "Live Monitor" y en el log de consola emulado en la interfaz.
3. **Registro de Reservas / Contactos:** Cuando el usuario adquiere un ticket o envía un mensaje en la página de contacto, el frontend envía un `POST /api/contacto` con formato JSON. El backend procesa el envío, valida que los campos estén completos, y añade el registro al archivo persistente `/app/logs/contactos.json` en el volumen de Docker.

---

## 3. Decisiones Técnicas de Dockerización y Seguridad

### Backend Dockerfile (`backend/Dockerfile`)
Se diseñó un Dockerfile optimizado enfocado en la ligereza, reproducibilidad y seguridad:
1. **Imagen Base:** Se seleccionó `python:3.11-slim` en lugar de una imagen completa de Python. Esto reduce el peso de la imagen de unos ~900MB a menos de ~150MB, acortando tiempos de build y bajando la superficie de ataque al no incluir dependencias de sistema innecesarias.
2. **Caché Multi-Capa (Multi-layer Caching):** Se copian primero los archivos de dependencias (`requirements.txt`) antes de transferir el código fuente. Esto permite que Docker cachee la capa de instalación de paquetes de Python (`pip install`) y acelere enormemente compilaciones posteriores si no han variado las dependencias.
3. **Seguridad (Contexto sin Privilegios):** Por defecto, los contenedores Docker corren como root. Para seguir las pautas de seguridad industrial, se creó un usuario y grupo de sistema limitados (`devopsuser` / `devopsgroup`) y se le otorgó propiedad sobre el directorio `/app`. El contenedor se ejecuta bajo el contexto seguro `USER devopsuser`.
4. **Healthcheck Nativo:** Se instaló `curl` de forma limpia y se configuró un `HEALTHCHECK` que ejecuta `curl -f http://localhost:5000/health || exit 1` cada 20 segundos. Esto expone el estado real del backend a Docker y Compose.

### Frontend Dockerfile (`frontend/Dockerfile`)
1. **Imagen Base:** Se utiliza `nginx:alpine` para actuar como servidor HTTP estático, garantizando un rendimiento óptimo de consumo de recursos y un peso de imagen mínimo (~23MB).

---

## 4. Orquestación y Redes (`docker-compose.yml`)

### Redes Bridge Aisladas
Se define una red bridge personalizada denominada `devops-network`.
* **Aislamiento:** Los contenedores frontend y backend se comunican dentro de esta red virtual.
* **Descubrimiento DNS Interno:** Los contenedores pueden llamarse entre sí usando su nombre de servicio (por ejemplo, el frontend puede apuntar al backend usando `http://backend:5000` internamente).

### Persistencia con Volúmenes
Se configuró el volumen con nombre `devops-backend-logs` mapeado en el backend bajo `/app/logs`.
* **Demostración de Persistencia:** Las reservas del formulario se guardan en `/app/logs/contactos.json` y el log de depuración en `/app/logs/festival.log`.
* **Persistencia del Estado:** Si ejecutamos `docker compose down` (destruyendo los contenedores) y luego `docker compose up -d` (creándolos nuevamente), los registros se leen del volumen persistente de Nodos y el Dashboard recuperará las reservas realizadas con anterioridad.

### Control de Dependencia de Salud
El servicio del `frontend` utiliza la sintaxis extendida `depends_on`:
```yaml
depends_on:
  backend:
    condition: service_healthy
```
Esto asegura que el servidor web Nginx no comience a despachar archivos del frontend hasta que el contenedor del Backend esté activo, responda saludablemente y pase la validación del `HEALTHCHECK`.

---

## 5. Control de Versiones con Git Flow
El proyecto fue construido bajo la metodología **Git Flow** para simular un ambiente colaborativo profesional:
1. **Rama `main`:** Código de producción estable (Versionado oficial).
2. **Rama `develop`:** Integración de nuevas funcionalidades estables para entrega técnica.
3. **Ramas `feature`:** Ramas de trabajo aisladas de desarrollo creadas desde `develop` y fusionadas sin Fast-Forward (`--no-ff`) para mantener la trazabilidad de la red gráfica:
   * `feature-backend`: Desarrollo de la API REST de Flask y testing.
   * `feature-frontend`: Implementación de maquetación HTML, estilos CSS y llamadas dinámicas JavaScript.
   * `feature-docker`: Creación de Dockerfiles y docker-compose.yml.
   * `feature-cicd`: Automatización con GitHub Actions.
   * `feature-docs`: Creación de manuales y presentador PowerPoint.

*Nota:* Un script automatizado (`scripts/simulate_git_history.ps1`) reconstruye este flujo de ramas de manera exacta en el entorno local del aprendiz para facilitar la demostración de la rama y commits en vivo.

---

## 6. Automatización de Integración Continua (GitHub Actions)
La automatización del ciclo de vida se encuentra en `.github/workflows/ci-cd.yml` y valida dos flujos críticos ante eventos `push` o `pull_request` en `main` y `develop`:

1. **Trabajo de Calidad y Tests (`lint-and-test`):**
   * Configura Python 3.11 en el runner de GitHub.
   * Ejecuta `flake8` para auditar la calidad del código, deteniendo la compilación si encuentra fallos críticos de sintaxis o variables sin definir.
   * Lanza `pytest` para verificar que la API responda con códigos de estado HTTP correctos para las rutas `/`, `/health`, `/api/artistas` y `/api/contacto`.
2. **Trabajo de Construcción (`docker-build`):**
   * Configura Docker Buildx.
   * Realiza un build de prueba (Dry Run) de las imágenes de Docker de frontend y backend (`push: false`) para garantizar que las dependencias de compilación resuelvan sin problemas.

---

## 7. Conclusiones de la Actividad

### Dificultades Encontradas y Soluciones
* **Dificultad:** Error de "CORS" (Cross-Origin Resource Sharing) en el navegador al intentar consultar el backend desde el cliente.
* **Solución:** Se integró la extensión `flask-cors` en la aplicación Flask, habilitando `CORS(app)` para autorizar llamadas asíncronas HTTP desde el dominio del frontend de manera segura.
* **Dificultad:** Mantener la persistencia del archivo JSON de contactos al destruir contenedores.
* **Solución:** Inicializar correctamente el directorio `/app/logs` en el Dockerfile y otorgar los permisos de escritura correspondientes al usuario no privilegido `devopsuser`, montando el volumen con nombre en la definición de Compose.

### Aprendizajes Clave
* El diseño de Dockerfiles robustos utilizando imágenes `slim` y entornos sin privilegios (`non-root`) mitiga brechas de seguridad informáticas en la nube.
* La cultura DevOps minimiza el esfuerzo manual; el uso de pipelines CI/CD previene errores humanos e inconsistencias de código antes de la entrega técnica.
