param(
    [string]$Output = "devops_project_submission.zip",
    [string[]]$Include = @("devops-festival-sena", "festival-devops", "concierto-app", "docs")
)

Write-Host "Generando paquete de entrega: $Output"

$items = @()
foreach ($i in $Include) {
    if (Test-Path $i) { $items += $i } else { Write-Host "Advertencia: no existe $i" }
}

if ($items.Count -eq 0) { Write-Error "No hay archivos para empaquetar. Abortando."; exit 1 }

if (Test-Path $Output) { Remove-Item $Output -Force }

Compress-Archive -Path $items -DestinationPath $Output -Force

Write-Host "Paquete creado: $Output"
Write-Host "Contenido:"; Get-ChildItem -Path $Output | Format-List
