@echo off
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
%PY% -c "import pynput" 2>nul || (
    echo Installation de pynput...
    %PY% -m pip install -r requirements.txt
)
%PY% zones.py
pause
