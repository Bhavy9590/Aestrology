@echo off
cd /d "%~dp0"
where python >nul 2>nul || (echo Python not found. Install Python 3.12 or 3.13 and try again.&pause&exit /b 1)
where npm >nul 2>nul || (echo Node.js/npm not found. Install Node.js 18+ and try again.&pause&exit /b 1)
if not exist backend\.venv (
    python -m venv backend\.venv
)
call backend\.venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r backend\requirements.txt
cd frontend
npm install
cd ..
python backend\manage.py migrate
echo.
echo Installation complete. Run start.bat next time.
pause
