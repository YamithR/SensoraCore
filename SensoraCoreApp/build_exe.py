# build_exe.py - Script para generar ejecutable de SensoraCore
"""
Script para compilar SensoraCore en un ejecutable .exe usando PyInstaller
"""

import os
import sys
import subprocess
import shutil

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = ['PySide6', 'matplotlib', 'openpyxl', 'pyinstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            # Handle special import cases
            if package == 'PySide6':
                __import__('PySide6')
            elif package == 'pyinstaller':
                __import__('PyInstaller')
            else:
                __import__(package.lower())
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Faltan dependencias: {', '.join(missing_packages)}")
        print("Instalando dependencias faltantes...")
        result = subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        
        # Verificar nuevamente después de la instalación
        print("\n🔍 Verificando dependencias nuevamente...")
        still_missing = []
        for package in missing_packages:
            try:
                if package == 'PySide6':
                    __import__('PySide6')
                elif package == 'pyinstaller':
                    __import__('PyInstaller')
                else:
                    __import__(package.lower())
                print(f"✅ {package} (instalado)")
            except ImportError:
                still_missing.append(package)
                print(f"❌ {package} (aún falta)")
        
        return len(still_missing) == 0
    
    return True

def build_executable():
    """Genera el ejecutable usando PyInstaller"""
    print("\n🔨 Generando ejecutable...")
    
    # Comando PyInstaller base
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name=SensoraCore",           # Nombre del ejecutable
        "--add-data=ui;ui",             # Incluir carpeta ui
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=matplotlib.backends.backend_qt5agg",
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--collect-all=matplotlib",
        "main.py"
    ]
    
    # Agregar icono si existe
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon=icon.ico")
        print("🎨 Icono encontrado, agregándolo al ejecutable")
    else:
        print("⚠️  Icono no encontrado, continuando sin icono")
    
    # Ejecutar PyInstaller
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Ejecutable generado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar ejecutable: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def cleanup():
    """Limpia archivos temporales"""
    print("\n🧹 Limpiando archivos temporales...")
    
    temp_dirs = ['build', '__pycache__']
    temp_files = ['SensoraCore.spec']
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️  Eliminado: {temp_dir}")
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"🗑️  Eliminado: {temp_file}")

def main():
    """Función principal"""
    print("🚀 SensoraCore - Generador de Ejecutable")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: main.py no encontrado")
        print("   Ejecuta este script desde el directorio SensoraCoreApp")
        return
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ Error: No se pudieron instalar todas las dependencias")
        return
    
    # Generar ejecutable
    if build_executable():
        print("\n🎉 ¡Ejecutable generado exitosamente!")
        print("📁 Ubicación: dist/SensoraCore.exe")
        print("\n📋 Instrucciones:")
        print("1. Copia SensoraCore.exe a cualquier carpeta")
        print("2. Asegúrate que el ESP32 esté configurado y encendido")
        print("3. Ejecuta SensoraCore.exe")
    else:
        print("\n❌ Error al generar el ejecutable")
    
    # Limpiar archivos temporales
    cleanup()
    
    print("\n✨ Proceso completado")

if __name__ == "__main__":
    main()
