# -----------------------------
# AGENT BOOT STRAP SCRIPT
# -----------------------------

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

# activate venv
& ".\venv\Scripts\Activate.ps1"

# ensure we are in project root
Set-Location -Path $PSScriptRoot

# run agent
python main.py
