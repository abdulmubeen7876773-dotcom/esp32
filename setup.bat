@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo ESP32 Engine setup
echo ==================

where py >nul 2>nul
if errorlevel 1 (
  where python >nul 2>nul
  if errorlevel 1 (
    echo ERROR: Python was not found. Install Python 3, then run setup.bat again.
    exit /b 1
  )
  set "PYTHON_BOOTSTRAP=python"
) else (
  set "PYTHON_BOOTSTRAP=py -3"
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating .venv...
  %PYTHON_BOOTSTRAP% -m venv .venv
  if errorlevel 1 (
    echo ERROR: Failed to create .venv.
    exit /b 1
  )
) else (
  echo Using existing .venv.
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo ERROR: Failed to activate .venv.
  exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
  echo ERROR: pip upgrade failed.
  exit /b 1
)

echo Installing requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: Dependency installation failed.
  exit /b 1
)

echo Verifying required modules...
python -c "import yaml; print('PyYAML OK:', yaml.__version__)"
if errorlevel 1 (
  echo ERROR: Required module verification failed.
  exit /b 1
)

echo.
echo SUCCESS: ESP32 Engine development environment is ready.
exit /b 0
