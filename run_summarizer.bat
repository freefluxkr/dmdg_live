@echo off
chcp 65001 > NUL
echo ===================================================
echo   DMDG - PDF to PPTX Summarizer (Local Build)
echo ===================================================
echo.
echo [INFO] Loading local summary database (ppt_data.json)...
echo [INFO] Running summarizer script. Please wait...
echo.

python summarize_pdfs_to_pptx.py

echo.
echo [SUCCESS] PDF to PPTX conversion completed successfully!
echo [SUCCESS] Please check the '0704보강/ppt' folder.
echo.
pause
