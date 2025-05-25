@echo off
setlocal enabledelayedexpansion
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
if exist "dist\*.exe" (
    echo ✅ Ejecutable(s) encontrado(s) en la carpeta 'dist':
    echo.
    for %%f in (dist\*.exe) do (
        echo 📁 %%~nxf
        echo    Tamaño: 
        dir "%%f" | find ".exe" | for /f "tokens=3" %%s in ('findstr /r /c:"[0-9]"') do echo    %%s bytes
        echo    Fecha: 
        dir "%%f" | find ".exe" | for /f "tokens=1,2" %%d in ('findstr /r /c:"[0-9]"') do echo    %%d %%e
        echo.
    )
    echo 📋 Instrucciones:
    echo 1. El/Los ejecutable(s) están en la carpeta 'dist'
    echo 2. Puedes copiarlo(s) a cualquier computadora Windows
    echo 3. No requiere instalación de Python ni dependencias
    echo 4. Los archivos anteriores se mantienen (no se borran)
    echo.
    echo ¿Deseas abrir la carpeta 'dist'? (S/N)
    choice /c SN /n
    if !errorlevel!==1 explorer dist
) else (
    echo ❌ Error: No se encontraron ejecutables en la carpeta 'dist'
    echo Revisa los mensajes de error anteriores
    echo.
    echo Posibles causas:
    echo - Faltan dependencias de Python
    echo - Error en el código fuente
    echo - Problemas de permisos
    echo.
)

echo.
pause
