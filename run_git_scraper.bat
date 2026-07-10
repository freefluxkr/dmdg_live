@echo off
chcp 65001 > NUL
echo ==========================================================
echo   Git Book PDF Scraper & Modernizer (Local Build)
echo ==========================================================
echo.
echo [INFO] Setting Python IO Encoding to UTF-8...
set PYTHONIOENCODING=utf-8
echo [INFO] Running build_git_pdf.py...
echo.

python build_git_pdf.py

echo.
echo [SUCCESS] Git PDF generation completed!
echo [SUCCESS] Check the 'Git' folder.
echo.
pause
