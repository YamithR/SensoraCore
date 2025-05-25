@echo off
echo.
echo ========================================
echo    SensoraCore - Compilador Automático
echo ========================================
echo.
echo Este script compilará SensoraCore en un ejecutable .exe
echo.
pause

cd /d "%~dp0"

if not exist "main.py" (
    echo ERROR: No se encontró main.py
    echo Ejecuta este script desde la carpeta SensoraCoreApp
    pause
    exit /b 1
)

echo Iniciando compilación...
python build_exe.py

echo.
echo ========================================
echo           Compilación Terminada
echo ========================================
echo.
if exist "dist\SensoraCore.exe" (
    echo ✅ Ejecutable creado exitosamente en: dist\SensoraCore.exe
    echo ✅ Tamaño: 
    dir dist\SensoraCore.exe | find "SensoraCore.exe"
    echo.
    echo 📋 Instrucciones:
    echo 1. El ejecutable está en la carpeta 'dist'
    echo 2. Puedes copiarlo a cualquier computadora Windows
    echo 3. No requiere instalación de Python ni dependencias
    echo.
    echo ¿Deseas abrir la carpeta 'dist'? (S/N)
    choice /c SN /n
    if !errorlevel!==1 explorer dist
) else (
    echo ❌ Error: No se pudo crear el ejecutable
    echo Revisa los mensajes de error anteriores
)

echo.
pause
