$ErrorActionPreference = "Stop"
Write-Host "Checking Python..." -ForegroundColor Cyan
py --version
Write-Host "Checking Node..." -ForegroundColor Cyan
node --version
npm --version
Write-Host "Environment checks complete." -ForegroundColor Green
