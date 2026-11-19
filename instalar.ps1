# KREAVANCE · instala las skills y comandos de krea-skills para TODOS los proyectos de Claude Code en este ordenador.
# Uso (PowerShell, dentro de la carpeta krea-skills):   powershell -ExecutionPolicy Bypass -File .\instalar.ps1
# Para actualizar: git pull y volver a ejecutarlo.
$origen = Join-Path $PSScriptRoot ".claude"
$destino = Join-Path $env:USERPROFILE ".claude"
New-Item -ItemType Directory -Force -Path (Join-Path $destino "skills"), (Join-Path $destino "commands") | Out-Null
Copy-Item -Recurse -Force (Join-Path $origen "skills\*") (Join-Path $destino "skills")
Copy-Item -Force (Join-Path $origen "commands\*") (Join-Path $destino "commands")
Write-Host "Listo: skills y comandos de KREA en $destino. Abre Claude Code en cualquier proyecto y prueba /seguridad."
