# New project

This workspace matches the original Explorer layout:

- `Cartograph-QA/` — the Robot Framework / Selenium capstone (this is what you run)
- `app.py`, `snn_pipeline.py`, `train_pipeline.py`, `models/` — leftover files from the original zip; they are **not** part of the automation assignment

## Why Cartograph-QA failed on this PC

The copy from your friend’s desktop shipped a virtual environment bound to **his** machine:

- Home Python: `C:\Program Files\Python313\python.exe`
- Venv path: `C:\Users\uttar\OneDrive\Documents\New project\Cartograph-QA\.venv`

That folder still exists here as `Cartograph-QA\.venv`, but it cannot run on this computer. Do not activate it.

This machine uses a new environment:

- Python 3.11.9 at `C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe`
- Venv: `C:\Users\User\Downloads\New project\Cartograph-QA\.venv-local`

Open **this** folder (`C:\Users\User\Downloads\New project`) in VS Code / Cursor, then run tests from `Cartograph-QA` with `.venv-local` — not from `Cartograph-QA` as a standalone project that still points at `.venv`.

## Run the automation

PowerShell from this workspace:

```powershell
.\run_cartograph.ps1
```

Smoke tests only:

```powershell
.\run_cartograph.ps1 -IncludeTag smoke
```

Headed Chrome (visible browser):

```powershell
.\run_cartograph.ps1 -Headless false
```

Or, from `Cartograph-QA` itself:

```powershell
Set-Location "C:\Users\User\Downloads\New project\Cartograph-QA"
.\.venv-local\Scripts\Activate.ps1
.\.venv-local\Scripts\robot.exe -d results tests
```

Reports land in `Cartograph-QA\results\`. Full framework notes are in `Cartograph-QA\README.md`.
