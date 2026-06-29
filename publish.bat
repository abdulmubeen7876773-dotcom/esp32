@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "COMMIT_MESSAGE=%*"
if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Publish ESP32 Engine updates"

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv not found. Run setup.bat first.
  exit /b 1
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo ERROR: Failed to activate .venv.
  exit /b 1
)

call validate.bat
if errorlevel 1 (
  echo ERROR: Publish stopped because validation failed.
  exit /b 1
)

call build.bat
if errorlevel 1 (
  echo ERROR: Publish stopped because build failed.
  exit /b 1
)

echo.
echo Publishing to origin/main...
git add .
if errorlevel 1 goto :gitfail

git diff --cached --quiet
if not errorlevel 1 (
  echo No staged changes to commit.
) else (
  git commit -m "%COMMIT_MESSAGE%"
  if errorlevel 1 goto :gitfail
)

git pull --rebase origin main
if errorlevel 1 goto :gitfail

git push origin main
if errorlevel 1 goto :gitfail

echo.
echo SUCCESS: Published to origin/main.
exit /b 0

:gitfail
echo.
echo ERROR: Publish failed during Git operation.
exit /b 1
