# Country Profile Application

A professional dashboard for viewing country economic profiles, built with FastAPI, React, and Ollama.

## Features
- **Macroeconomics**: Real-time stats from World Bank.
- **Investment Climate**: AI-curated insights using Ollama.
- **FDI Overview**: Inbound and Outbound FDI data processed with `jq`.
- **Political Landscape**: Wikipedia-sourced summaries and leadership info.

## Tech Stack
- **Backend**: Python (FastAPI), `uv`, `jq`, Ollama (llama3).
- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons.

## Setup & Run

### 1. Prerequisites
- [Ollama](https://ollama.com/) must be installed and running.
- Pull the model: `ollama pull llama3`

### 2. Backend
```bash
cd backend
# uv will handle venv and deps
python -m uv run main.py

```
#Run scheduled tasks:
powershell.exe -File .\daily_sync.ps1

python -m uv run sync_data.py --mode daily --ai

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Data Sources
- **World Bank**: GDP, Inflation, Unemployment, FDI.
## API:
BASE_URL = "https://api.worldbank.org/v2"
    
    INDICATORS = {
        "gdp": "NY.GDP.MKTP.CD",
        "gdp_growth": "NY.GDP.MKTP.KD.ZG",
        "inflation": "FP.CPI.TOTL.ZG",
        "unemployment": "SL.UEM.TOTL.ZS",
        "debt_gdp": "GC.DOD.TOTL.GD.ZS"
    }

- **UNCTAD**: FDI trends (simulated via World Bank with `jq` processing).

## API:
    INWARD_FDI = "BX.KLT.DINV.CD.WD"
    OUTWARD_FDI = "BM.KLT.DINV.CD.WD"

- **Wikipedia**: Country summaries and political structure.

## Data Management

The application uses a local storage system to ensure high performance and availability.

### Local Storage
- Path: `backend/storage_data/`
- Format: JSON (per country code)

### Synchronizing Data
To update country data and generate AI insights:

**Via Batch Files (Recommended on Windows):**
- Double-click `run_daily.bat` to sync popular countries.
- Double-click `run_weekly.bat` to perform a full sync.

**Via PowerShell Scripts:**
- `./daily_sync.ps1`: Syncs popular countries (may require `-ExecutionPolicy Bypass`).
- `./weekly_sync.ps1`: Performs a full sync (may require `-ExecutionPolicy Bypass`).

**Via CLI:**
```powershell
cd backend
python -m uv run sync_data.py --mode [daily|weekly|single] [--country CODE]
```

python -m uv run sync_ai.py --country IND

python -m uv run sync_data.py --mode single --country GBR
python backend/sync_data.py --mode single --country GBR