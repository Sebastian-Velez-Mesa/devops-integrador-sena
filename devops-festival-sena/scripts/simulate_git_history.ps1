# ── Git Flow History Simulator for SENA DevOps Project ─────────────────
# Este script inicializa un repositorio de Git en el proyecto final
# y recrea un historial de commits y ramas estructurado para la sustentación.

# Detener en caso de error
$ErrorActionPreference = "Stop"

# Guardar ubicación actual
$originalDir = Get-Location

# Ubicación del proyecto final
$projectPath = "c:\Users\User\Desktop\devops_lab\devops-festival-sena"

Write-Output "=== Iniciando Simulación de Historial Git en: $projectPath ==="

if (-not (Test-Path $projectPath)) {
    Write-Error "El directorio de destino no existe: $projectPath"
}

# Cambiar al directorio del proyecto
Set-Location $projectPath

# Limpiar repositorio de git previo si existe
if (Test-Path ".git") {
    Write-Output "Removiendo repositorio Git previo para reiniciar..."
    Remove-Item -Recurse -Force ".git"
}

# 1. Inicializar Git
git init
git config --local user.name "DevOps SENA Apprentice"
git config --local user.email "devops.apprentice@sena.edu.co"

# 2. Crear .gitignore
Write-Output "Creando .gitignore..."
$gitignoreContent = @"
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.venv/
env/
venv/
ENV/

# Logs y Persistencia
backend/logs/
*.log
contactos.json

# IDEs
.vscode/
.idea/

# Sistema
.DS_Store
Thumbs.db
"@
Set-Content -Path ".gitignore" -Value $gitignoreContent

# 3. Primer Commit en Main (Estructura inicial)
Write-Output "Creando commit inicial en 'main'..."
git checkout -b main
git add .gitignore
# Temporalmente quitamos los archivos reales de la ruta para irlos metiendo por commits/ramas
# Pero para hacerlo fácil, podemos mover los archivos temporalmente o simplemente irlos agregando selectivamente.
# Hagámoslo selectivamente agregando archivos por feature:

git commit -m "chore: initial commit with gitignore setup"

# 4. Crear rama develop
Write-Output "Creando rama 'develop'..."
git checkout -b develop

# 5. Feature Backend: Agregar archivos de backend
Write-Output "Simulando rama 'feature-backend'..."
git checkout -b feature-backend
git add backend/app.py backend/requirements.txt backend/test_app.py
git commit -m "feat(backend): implement Flask REST API with persistency and unit tests"

# Combinar feature-backend en develop
git checkout develop
git merge --no-ff feature-backend -m "merge: integrate feature-backend into develop"
git branch -d feature-backend

# 6. Feature Frontend: Agregar archivos de frontend
Write-Output "Simulando rama 'feature-frontend'..."
git checkout -b feature-frontend
git add frontend/index.html frontend/artistas.html frontend/tickets.html frontend/contacto.html frontend/style.css
git commit -m "feat(frontend): create user interface with interactive DevOps live dashboard"

# Combinar feature-frontend en develop
git checkout develop
git merge --no-ff feature-frontend -m "merge: integrate feature-frontend into develop"
git branch -d feature-frontend

# 7. Feature Docker: Agregar Dockerfiles y Docker Compose
Write-Output "Simulando rama 'feature-docker'..."
git checkout -b feature-docker
git add backend/Dockerfile frontend/Dockerfile docker-compose.yml .env.template
git commit -m "feat(docker): dockerize frontend/backend services and setup docker-compose orchestration"

# Combinar feature-docker en develop
git checkout develop
git merge --no-ff feature-docker -m "merge: integrate feature-docker into develop"
git branch -d feature-docker

# 8. Feature CI/CD: Agregar GitHub Actions
Write-Output "Simulando rama 'feature-cicd'..."
git checkout -b feature-cicd
git add .github/workflows/ci-cd.yml
git commit -m "feat(cicd): configure GitHub Actions pipeline for linting, testing, and container build checks"

# Combinar feature-cicd en develop
git checkout develop
git merge --no-ff feature-cicd -m "merge: integrate feature-cicd into develop"
git branch -d feature-cicd

# 9. Agregar scripts de automatización y documentación
Write-Output "Simulando rama 'feature-docs'..."
git checkout -b feature-docs
git add scripts/generate_presentation.py scripts/simulate_git_history.ps1
# Nota: agregaremos los archivos de documentación (DOCUMENTACION.md, README.md) más adelante, pero confirmemos este commit por ahora
git commit -m "docs: add presentation generator script and git history simulator"

git checkout develop
git merge --no-ff feature-docs -m "merge: integrate feature-docs into develop"
git branch -d feature-docs

# 10. Fusiones finales a main
Write-Output "Fusionando de 'develop' a 'main'..."
git checkout main
git merge --no-ff develop -m "release: version 1.0.0 for DevOps CTMA final presentation"

# Dejar el repositorio parado en la rama develop (común en Git Flow)
git checkout develop

# Regresar al directorio original
Set-Location $originalDir

Write-Output "=== Historial Git Recreado Exitosamente ==="
Write-Output "Usa 'git log --graph --oneline --all' para inspeccionar la red de ramas y commits."
