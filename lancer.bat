@echo off
cd /d "%~dp0"
python -c "import pynput" 2>nul || (
    echo Installation de pynput...
    pip install -r requirements.txt
)
python zones.py
pause
