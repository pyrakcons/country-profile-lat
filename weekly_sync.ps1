Write-Host "Starting Weekly Full Country Data Sync..." -ForegroundColor Cyan
Set-Location -Path "$PSScriptRoot/backend"
python -m uv run sync_data.py --mode weekly --ai
Write-Host "Weekly Sync Complete." -ForegroundColor Green
