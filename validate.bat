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

echo Running ESP32 Engine validation...

echo.
echo === validate_content.py ===
python tools\validate_content.py
if errorlevel 1 goto :fail

echo.
echo === validate_component_quality.py ===
python tools\validate_component_quality.py
if errorlevel 1 goto :fail

echo.
echo === validate_guide_quality.py ===
python tools\validate_guide_quality.py
if errorlevel 1 goto :fail

echo.
echo === validate_project_quality.py ===
python tools\validate_project_quality.py
if errorlevel 1 goto :fail

echo.
echo === validate_project_metadata_sync.py ===
python tools\validate_project_metadata_sync.py
if errorlevel 1 goto :fail

echo.
echo === validate_phase_b_homepage.py ===
python tools\validate_phase_b_homepage.py
if errorlevel 1 goto :fail

echo.
echo === validate_phase_c_cleanup.py ===
python tools\validate_phase_c_cleanup.py
if errorlevel 1 goto :fail

echo.
echo === validate_faq_quality.py ===
python tools\validate_faq_quality.py
if errorlevel 1 goto :fail

echo.
echo === validate_phase_d_acceptance.py ===
python tools\validate_phase_d_acceptance.py
if errorlevel 1 goto :fail

echo.
echo === validate_visual_assets.py ===
python tools\validate_visual_assets.py
if errorlevel 1 goto :fail

echo.
echo === validate_seo.py ===
python tools\validate_seo.py
if errorlevel 1 goto :fail

echo.
echo === release_validation.py ===
python -c "import sys; sys.path.insert(0, 'tools'); import release_validation; report = release_validation.generate_release_report({'status': 'VALIDATION'}); raise SystemExit(1 if report.get('status') == 'FAIL' else 0)"
if errorlevel 1 goto :fail

echo.
echo SUCCESS: Validation completed.
exit /b 0

:fail
echo.
echo ERROR: Validation failed. Fix the issue above before building or publishing.
exit /b 1
