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
            __import__(package.lower() if package != 'PySide6' else 'PySide6')
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Faltan dependencias: {', '.join(missing_packages)}")
        print("Instalando dependencias faltantes...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
    
    return len(missing_packages) == 0

def build_executable():
    """Genera el ejecutable usando PyInstaller"""
    print("\n🔨 Generando ejecutable...")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name=SensoraCore",           # Nombre del ejecutable
        "--icon=icon.ico",              # Icono (si existe)
        "--add-data=ui;ui",             # Incluir carpeta ui
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=matplotlib.backends.backend_qt5agg",
        "main.py"
    ]
    
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
