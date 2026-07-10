@echo off
echo ==========================================================
echo   Data Analysis Book PDF Scraper (Local Build)
echo ==========================================================
echo.
echo [INFO] Setting Python IO Encoding to UTF-8...
set PYTHONIOENCODING=utf-8
echo [INFO] Running build_every_data_analysis_pdf.py...
echo.

python build_every_data_analysis_pdf.py

echo.
echo [SUCCESS] PDF generation completed!
echo [SUCCESS] Check the output folder.
echo.
pause
