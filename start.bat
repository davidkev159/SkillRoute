@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   SkillRoute launcher
echo ============================================
echo.

if not exist "backend\.env" (
    echo [!] backend\.env not found.
    echo.
    echo     Copy backend\.env.example to backend\.env and fill in your
    echo     CognoDB connection details first:
    echo         NEO4J_URI      = bolt+s://your-instance-id.databases.cognodb.cloud
    echo         NEO4J_USERNAME = cognodb
    echo         NEO4J_PASSWORD = the password shown once when you created the instance
    echo.
    pause
    exit /b 1
)

if not exist "backend\.venv" (
    echo [*] First run: creating backend virtual environment and installing dependencies...
    python -m venv backend\.venv
    call backend\.venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    call backend\.venv\Scripts\deactivate.bat
    echo.
)

if not exist "frontend\node_modules" (
    echo [*] First run: installing frontend dependencies...
    pushd frontend
    call npm install
    popd
    echo.
)

echo [*] Starting the API on http://localhost:8000 ...
start "SkillRoute API" cmd /k "cd /d "%~dp0backend" && call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

echo [*] Starting the frontend on http://localhost:5173 ...
start "SkillRoute Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo [*] Waiting for everything to boot...
timeout /t 6 /nobreak >nul

start "" "http://localhost:5173"

echo.
echo SkillRoute is running in two separate windows (API + Frontend).
echo Close those windows (or Ctrl+C inside them) to stop the servers.
echo.
echo If this is your very first run, remember to load the seed data once:
echo     cd backend ^&^& .venv\Scripts\activate ^&^& python -m seed.seed
echo.
pause
endlocal
