@echo off
chcp 65001 > NUL
echo ==========================================================
echo   FastAPI Book PDF Scraper & Modernizer (Local Build)
echo ==========================================================
echo.
echo [INFO] Setting Python IO Encoding to UTF-8...
set PYTHONIOENCODING=utf-8
echo [INFO] Running build_fastapi_pdf.py...
echo.

python build_fastapi_pdf.py

echo.
echo [SUCCESS] FastAPI PDF generation completed!
echo [SUCCESS] Check the 'FastAPI' folder.
echo.
pause
