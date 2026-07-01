# Demo script para la presentación - PowerShell
Write-Host "Iniciando demo del proyecto DevOps Festival"

Write-Host "1) Construir y levantar servicios (detached)..."
docker compose up --build -d

Write-Host "\n2) Esperar 3 segundos y listar contenedores"
Start-Sleep -Seconds 3
docker ps --format "table {{.Names}}	{{.Image}}	{{.Status}}"

Write-Host "\n3) Inspeccionar imágenes"
docker images --format "table {{.Repository}}	{{.Tag}}	{{.Size}}"

Write-Host "\n4) Chequear endpoints de health"
try {
    $b = curl http://localhost:5000/health -UseBasicParsing
    Write-Host "Backend health:`n" $b.Content
} catch {
    Write-Host "No se pudo contactar el backend en http://localhost:5000/health"
}

try {
    $f = curl http://localhost:8080/ -UseBasicParsing
    Write-Host "Frontend OK (index) — tamaño: " ($f.Content.Length) " bytes"
} catch {
    Write-Host "No se pudo contactar el frontend en http://localhost:8080/"
}

Write-Host "\n5) Mostrar redes y volúmenes"
docker network ls
docker volume ls

Write-Host "\n6) Mostrar últimos commits"
git --no-pager log --oneline -n 10

Write-Host "\nDemo finalizada. Para detener y eliminar contenedores: `docker compose down -v`"
