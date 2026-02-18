Write-Host "Starting Daily Country Data Sync..." -ForegroundColor Cyan
Set-Location -Path "$PSScriptRoot/backend"
python -m uv run sync_data.py --mode daily --ai
Write-Host "Daily Sync Complete." -ForegroundColor Green
