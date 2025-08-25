# Build-Release.ps1
# Crea un .exe de la app PySide6 con PyInstaller.
# - Permite elegir nombre del .exe y el icono .ico
# - Dos modos: performance (inicio rápido, onedir) y portable (un solo .exe, onefile)
# - Incluye los archivos .ui y datos necesarios
# - Optimiza tamaño/tiempo con --strip, limpieza y runtime hook para rutas

Param(
    [string]$Version,
    [string]$ExeName,
    [string]$IconPath,
    [ValidateSet('performance','portable')]
    [string]$Mode = 'portable',
    [switch]$Clean,
    [string]$UPXDir
)

$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -ge 7) { $PSStyle.OutputRendering = 'Host' }

function Write-Info($msg){ Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg){ Write-Host "[ OK ] $msg" -ForegroundColor Green }
function Write-Warn($msg){ Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg){ Write-Host "[ERR ] $msg" -ForegroundColor Red }

# Rutas base
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Split-Path -Parent $scriptDir   # .../SensoraCore

# Entrypoint
$entryPoint = Join-Path $repoRoot "SC_DesktopApp\Main\main.py"
if (-not (Test-Path $entryPoint)) { Write-Err "No se encontró entrypoint: $entryPoint"; exit 1 }

# Defaults interactivos
if (-not $ExeName -or $ExeName.Trim() -eq '') { $ExeName = Read-Host "Nombre del .exe (ej: SensoraCore)" }
if (-not $ExeName -or $ExeName.Trim() -eq '') { $ExeName = 'SensoraCore_Beta1.0' }

if (-not $Version -or $Version.Trim() -eq '') {
    $Version = Read-Host "Versión a generar (ej: 1.0.0 o auto)"
}
if ($Version -eq '' -or $Version -eq 'auto') {
    $Version = (Get-Date).ToString('yyyy.MM.dd.HHmm')
}

$defaultIcon = Join-Path $repoRoot 'Docs\Media\SensoraCore.ico'
if (-not $IconPath -or $IconPath.Trim() -eq '') { $IconPath = $defaultIcon }
if (-not (Test-Path $IconPath)) { Write-Warn "Icono no encontrado en '$IconPath'. Se compilará sin icono."; $IconPath = $null }

# Carpetas de salida
$distDir = Join-Path $scriptDir "Versiones\${ExeName}_$Version"
$buildWorkDir = Join-Path $scriptDir 'build'
$specDir = Join-Path $scriptDir 'spec'
New-Item -ItemType Directory -Force -Path $distDir, $buildWorkDir, $specDir | Out-Null

# Resolver intérprete de Python a usar
$pythonExe = $null
# 1) Usar venv activo si existe
if ($env:VIRTUAL_ENV) {
    $candidate = Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe'
    if (Test-Path $candidate) { $pythonExe = $candidate }
}
# 2) Usar .venv del repo si existe
if (-not $pythonExe) {
    $repoVenv = Join-Path $repoRoot '.venv\Scripts\python.exe'
    if (Test-Path $repoVenv) { $pythonExe = $repoVenv }
}
# 3) En su defecto, crear venv local del compilador
$createdLocalVenv = $false
if (-not $pythonExe) {
    $venvPath = Join-Path $scriptDir '.venv'
    $venvPython = Join-Path $venvPath 'Scripts\python.exe'
    if (-not (Test-Path $venvPython)) {
        Write-Info 'Creando entorno virtual local para compilación...'
        & py -3 -m venv $venvPath
        $createdLocalVenv = $true
    }
    if (Test-Path $venvPython) { $pythonExe = $venvPython }
}
if (-not $pythonExe) { Write-Err 'No se encontró Python. Asegúrate de tener py -3 o un .venv válido.'; exit 1 }

# Instalar dependencias para build
$reqFile = Join-Path $repoRoot 'Docs\requirements.txt'
& $pythonExe -m pip install --upgrade pip wheel setuptools | Out-Null
# Siempre asegurar PyInstaller en el intérprete seleccionado
& $pythonExe -m pip install --upgrade pyinstaller pyinstaller-hooks-contrib | Out-Null
# Solo instalar requirements si usamos un venv local recién creado (para no pisar el venv del proyecto)
if ($createdLocalVenv -and (Test-Path $reqFile)) {
    Write-Info 'Instalando dependencias del proyecto en el entorno local de compilación...'
    & $pythonExe -m pip install -r $reqFile | Out-Null
}

# Verificar e instalar módulos de runtime mínimos si faltan (p.ej. PySide6)
# Nota: pandas y pillow son necesarios para las exportaciones a Excel con gráficos
$requiredMods = @('PySide6','matplotlib','numpy','openpyxl','pandas','pillow') | Where-Object { $_ -and $_.Trim() -ne '' } | Select-Object -Unique
# Crear script temporal para evitar problemas de quoting con -c
$checkScript = @(
    'import importlib, sys',
    'name = sys.argv[1] if len(sys.argv) > 1 else ""',
    'sys.exit(0) if (name and importlib.util.find_spec(name)) else sys.exit(1)'
) -join "`n"
$checkPath = Join-Path $buildWorkDir 'check_import.py'
Set-Content -Path $checkPath -Value $checkScript -Encoding UTF8

$missingMods = @()
foreach ($m in $requiredMods) {
    $proc = Start-Process -FilePath $pythonExe -ArgumentList $checkPath, $m -NoNewWindow -PassThru -Wait -ErrorAction SilentlyContinue
    if (-not $proc -or $proc.ExitCode -ne 0) { $missingMods += $m }
}
if ($missingMods.Count -gt 0) {
    Write-Info ("Instalando módulos faltantes: {0}" -f ($missingMods -join ', '))
    & $pythonExe -m pip install @missingMods | Out-Null
}
Write-Info ("Usando Python: {0}" -f $pythonExe)

# Hook en runtime para fijar CWD cuando es onefile
$runtimeHook = Join-Path $specDir 'hook_set_cwd.py'
if (-not (Test-Path $runtimeHook)) {
$hookContent = @'
import os, sys
# Si fue empaquetado como onefile, PyInstaller expone sys._MEIPASS con la ruta de extracción temporal.
if hasattr(sys, "_MEIPASS") and sys._MEIPASS:
    try:
        os.chdir(sys._MEIPASS)
    except Exception:
        pass
'@
    Set-Content -Path $runtimeHook -Value $hookContent -Encoding UTF8
}

# Flags de optimización y modo
$commonArgs = @()
$commonArgs += '--noconfirm'
$commonArgs += '--clean'
$commonArgs += '--windowed'
$commonArgs += ('--name', $ExeName)
$commonArgs += ('--distpath', $distDir)
$commonArgs += ('--workpath', $buildWorkDir)
$commonArgs += ('--specpath', $specDir)
$commonArgs += ('--runtime-hook', $runtimeHook)
$commonArgs += ('--paths', (Join-Path $repoRoot 'SC_DesktopApp'))
$commonArgs += '--hidden-import' ; $commonArgs += 'PySide6.QtUiTools'
$commonArgs += '--hidden-import' ; $commonArgs += 'matplotlib.backends.backend_qtagg'
$commonArgs += '--hidden-import' ; $commonArgs += 'pandas'
$commonArgs += '--hidden-import' ; $commonArgs += 'openpyxl'
$commonArgs += '--collect-data'  ; $commonArgs += 'matplotlib'
$commonArgs += '--collect-all'   ; $commonArgs += 'pandas'
$commonArgs += '--collect-all'   ; $commonArgs += 'openpyxl'
$commonArgs += '--collect-all'   ; $commonArgs += 'PySide6'
$commonArgs += '--collect-all'   ; $commonArgs += 'shiboken6'
$commonArgs += '--collect-all'   ; $commonArgs += 'numpy'

# UPX: comprimir binarios si upx.exe está disponible
try {
    $resolvedUpxDir = $null
    if ($UPXDir -and (Test-Path $UPXDir)) {
        $resolvedUpxDir = $UPXDir
    } else {
        $upxCmd = Get-Command upx.exe -ErrorAction SilentlyContinue
        if ($upxCmd) { $resolvedUpxDir = Split-Path -Parent $upxCmd.Path }
    }
    if ($resolvedUpxDir) {
        Write-Info ("Usando UPX en: {0}" -f $resolvedUpxDir)
        $commonArgs += ('--upx-dir', $resolvedUpxDir)
        # Excluir runtimes de MSVC por estabilidad
        $commonArgs += '--upx-exclude' ; $commonArgs += 'vcruntime*.dll'
        $commonArgs += '--upx-exclude' ; $commonArgs += 'msvcp*.dll'
    } else {
        Write-Warn 'UPX no encontrado en PATH. Si deseas usarlo, instala UPX o proporciona -UPXDir.'
    }
} catch { Write-Warn ("No se pudo configurar UPX: {0}" -f $_.Exception.Message) }

# Asegurar inclusion de modulos de sensores (Modules.<sensor>.*_logic)
$modulesRoot = Join-Path $repoRoot 'SC_DesktopApp\Modules'
if (Test-Path $modulesRoot) {
    Get-ChildItem -Directory -Path $modulesRoot | ForEach-Object {
        $sensorDir = $_.Name
        Get-ChildItem -Path $_.FullName -Filter '*_logic.py' -File -ErrorAction SilentlyContinue | ForEach-Object {
            $modBase = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
            $hidden = "Modules.$sensorDir.$modBase"
            $commonArgs += '--hidden-import'; $commonArgs += $hidden
        }
    }
}

# Incluir archivos .ui y datos necesarios preservando estructura 'SensoraCore/...'
function Add-DataArg($src, $dst){
    # Nota: En Windows, PyInstaller usa ';' para separar origen;destino
    # Importante: usar el scope del script para mutar el arreglo compartido
    $script:commonArgs += '--add-data'
    $script:commonArgs += ("$src;$dst")
}

# Paquetes de UI
# Main UI
$uiMainSrc = Join-Path $repoRoot 'SC_DesktopApp\Main\mainWindow.ui'
if (Test-Path $uiMainSrc) { Add-DataArg $uiMainSrc 'SensoraCore\SC_DesktopApp\Main' }
# Todos los .ui de módulos
Get-ChildItem -Recurse -Path (Join-Path $repoRoot 'SC_DesktopApp\Modules') -Filter '*.ui' | ForEach-Object {
    $rel = $_.FullName.Substring($repoRoot.Length).TrimStart('\\')
    $destDir = 'SensoraCore\' + (Split-Path $rel -Parent)
    Add-DataArg $_.FullName $destDir
}
# Media (iconos/imagenes)
Get-ChildItem -Path (Join-Path $repoRoot 'Docs\Media') -File -ErrorAction SilentlyContinue | ForEach-Object {
    Add-DataArg $_.FullName 'SensoraCore\Docs\Media'
}

# Exclusiones para aligerar y mejorar arranque
$excludeArgs = @()
# Siempre excluir paquetes de pruebas pesados
$excludeArgs += '--exclude-module'; $excludeArgs += 'pandas.tests'
$excludeArgs += '--exclude-module'; $excludeArgs += 'numpy.tests'
$excludeArgs += '--exclude-module'; $excludeArgs += 'matplotlib.tests'
if ($Mode -eq 'performance') {
    $excludeArgs += '--exclude-module'; $excludeArgs += 'tkinter'
    $excludeArgs += '--exclude-module'; $excludeArgs += 'pytest'
    $excludeArgs += '--exclude-module'; $excludeArgs += 'scipy'
    $excludeArgs += '--exclude-module'; $excludeArgs += 'sklearn'  # No usada en UI principal
}

# Modo de empaquetado
$modeArgs = @()
if ($Mode -eq 'performance') {
    # onedir -> inicio más rápido; sin UPX para evitar sobrecarga de descompresión
    $modeArgs += '--onedir'
} else {
    # portable -> un solo .exe
    $modeArgs += '--onefile'
}

# Icono
$iconArgs = @()
if ($IconPath) { $iconArgs += ('--icon', $IconPath) }

# Opción de limpieza total
if ($Clean.IsPresent) {
    Write-Info 'Limpiando artefactos previos...'
    Get-ChildItem -Path $distDir -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $buildWorkDir -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# Ejecutar PyInstaller
$env:PYTHONOPTIMIZE = '2'   # quita asserts/docstrings stdlib
Write-Info "Compilando $ExeName ($Mode) versión $Version..."
$pyinstallerArgs = @()
$pyinstallerArgs += $commonArgs
$pyinstallerArgs += $excludeArgs
$pyinstallerArgs += $modeArgs
$pyinstallerArgs += $iconArgs
$pyinstallerArgs += $entryPoint

# Log de depuración
Write-Host "pyinstaller " ($pyinstallerArgs -join ' ') -ForegroundColor DarkGray

& $pythonExe -m PyInstaller @pyinstallerArgs
if ($LASTEXITCODE -ne 0) { Write-Err 'PyInstaller falló'; exit 1 }

Write-Ok "Build completado. Salida en: $distDir"

# Copiar el icono al directorio final por conveniencia
if ($IconPath -and (Test-Path $IconPath)) {
    Copy-Item -Force $IconPath -Destination $distDir -ErrorAction SilentlyContinue
}

 # Sin ZIP: se deja sólo el ejecutable en la carpeta de versiones

Write-Host "`nCómo ejecutar:" -ForegroundColor Cyan
if ($Mode -eq 'portable') {
    Write-Host "  $distDir\$ExeName.exe" -ForegroundColor White
} else {
    Write-Host "  $distDir\$ExeName\$ExeName.exe" -ForegroundColor White
}
