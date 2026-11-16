# Mini Travel Planner

A Flask dashboard for saving trip destinations, travel dates, and estimated budgets. Trip data is stored locally in `data/trips.json`.

## Requirements

- Python 3.9 or newer
- Packages listed in `requirements.txt`

## Setup

From the project directory, create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run --debug
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app app run --debug
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

The app generates a temporary random session key when `FLASK_SECRET_KEY` is not set, which is suitable for local development. For a persistent key, set `FLASK_SECRET_KEY` in your environment before starting the app. For example, in PowerShell:

```powershell
$env:FLASK_SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
```

## Features

- Add trips with a destination, start and end dates, and a positive estimated budget.
- Search saved trips by destination and view the filtered trip count.
- View the combined budget for all saved trips.
- Delete trips you no longer need.
- Persist trip data locally in `data/trips.json`; this file is excluded from Git to keep personal trip information private.

The dashboard loads Tailwind CSS from a public CDN, so styling requires an internet connection.
