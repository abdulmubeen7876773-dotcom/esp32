@echo off
setlocal EnableExtensions

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv not found. Run setup.bat first.
  exit /b 1
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo ERROR: Failed to activate .venv.
  exit /b 1
)

echo Running ESP32 Engine build...
python tools\build_all.py
if errorlevel 1 (
  echo.
  echo ERROR: Build failed.
  exit /b 1
)

echo.
echo SUCCESS: Build completed.
exit /b 0
