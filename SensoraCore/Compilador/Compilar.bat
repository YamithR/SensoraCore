@echo off
REM Compilar.bat - Delegado al script PowerShell con opciones interactivas
setlocal EnableExtensions

set SCRIPT_DIR=%~dp0
set PS1=%SCRIPT_DIR%Build-Release.ps1

if not exist "%PS1%" (
	echo [ERR ] No se encontró Build-Release.ps1 en %SCRIPT_DIR%
	exit /b 1
)

REM Ejecuta PowerShell con política de ejecución relajada solo para este proceso
powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
set EXITCODE=%ERRORLEVEL%
if not "%EXITCODE%"=="0" (
	echo [ERR ] Fallo en la compilacion. Codigo %EXITCODE%
	exit /b %EXITCODE%
)

echo [ OK ] Compilacion finalizada.
exit /b 0
