@echo off
echo ========================================
echo Building AEGIS AI .exe...
echo ========================================
echo.

pyinstaller --clean aegis.spec

echo.
echo ========================================
echo Build complete!
echo Check the 'dist' folder for AEGIS_AI.exe
echo ========================================
pause
