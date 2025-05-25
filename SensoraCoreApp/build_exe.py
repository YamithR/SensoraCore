# build_exe.py - Script para generar ejecutable de SensoraCore
import os
import sys
import subprocess
import shutil
from datetime import datetime

def check_dependencies():
    print(" Verificando dependencias...")
    required_packages = ['PySide6', 'matplotlib', 'openpyxl', 'pyinstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PySide6':
                __import__('PySide6')
            elif package == 'pyinstaller':
                __import__('PyInstaller')
            else:
                __import__(package.lower())
            print(f" {package}")
        except ImportError:
            missing_packages.append(package)
            print(f" {package}")
    
    if missing_packages:
        print(f"\n  Faltan dependencias: {', '.join(missing_packages)}")
        print("Instalando dependencias faltantes...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
            print(" Dependencias instaladas correctamente")
        except subprocess.CalledProcessError as e:
            print(f" Error al instalar dependencias: {e}")
            return False
    return True

def get_executable_name():
    print("\n Configuración del ejecutable:")
    print("1. Usar nombre por defecto (SensoraCore)")
    print("2. Especificar nombre personalizado")
    
    while True:
        try:
            choice = input("\nSelecciona una opción (1-2): ").strip()
            if choice == "1":
                return "SensoraCore"
            elif choice == "2":
                name = input("Ingresa el nombre del ejecutable (sin extensión .exe): ").strip()
                if name:
                    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
                    if any(char in name for char in invalid_chars):
                        print(" El nombre contiene caracteres no válidos.")
                        continue
                    return name
                else:
                    print(" El nombre no puede estar vacío")
            else:
                print(" Opción no válida. Selecciona 1 o 2.")
        except (KeyboardInterrupt, EOFError):
            return "SensoraCore"

def check_existing_file(exe_name):
    exe_path = f"dist/{exe_name}.exe"
    
    if not os.path.exists(exe_path):
        return exe_name
    
    print(f"\n  El archivo '{exe_name}.exe' ya existe en la carpeta 'dist'")
    print("1. Reemplazar el archivo existente")
    print("2. Crear con nombre automático (agrega timestamp)")
    print("3. Especificar un nuevo nombre")
    
    while True:
        try:
            choice = input("\nSelecciona una opción (1-3): ").strip()
            
            if choice == "1":
                print(f" Se reemplazará '{exe_name}.exe'")
                return exe_name
            elif choice == "2":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{exe_name}_{timestamp}"
                print(f" Nuevo nombre automático: '{new_name}.exe'")
                return new_name
            elif choice == "3":
                new_name = input("Ingresa el nuevo nombre (sin extensión .exe): ").strip()
                if new_name:
                    print(f" Nuevo nombre: '{new_name}.exe'")
                    return new_name
                else:
                    print(" El nombre no puede estar vacío")
            else:
                print(" Opción no válida. Selecciona 1, 2 o 3.")
        except (KeyboardInterrupt, EOFError):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{exe_name}_{timestamp}"

def build_executable(exe_name):
    print(f"\n Generando ejecutable: {exe_name}.exe...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--name={exe_name}",
        "--add-data=ui;ui",
        "--exclude-module=PyQt5",
        "--exclude-module=tkinter",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=matplotlib.backends.backend_qt5agg",
        "--collect-all=matplotlib",
        "main.py"
    ]
    
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon=icon.ico")
        print(" Icono encontrado, agregándolo al ejecutable")
    else:
        print("  Icono no encontrado, continuando sin icono")
    
    try:
        print(" Ejecutando PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f" Ejecutable '{exe_name}.exe' generado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error al generar ejecutable:")
        print(f"Código de error: {e.returncode}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def cleanup(exe_name):
    print("\n Limpiando archivos temporales...")
    
    temp_dirs = ['build', '__pycache__']
    temp_files = [f'{exe_name}.spec']
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"  Eliminado: {temp_dir}")
            except Exception as e:
                print(f"  No se pudo eliminar {temp_dir}: {e}")
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"  Eliminado: {temp_file}")
            except Exception as e:
                print(f"  No se pudo eliminar {temp_file}: {e}")

def main():
    try:
        print(" SensoraCore - Generador de Ejecutable")
        print("=" * 50)
        
        if not os.path.exists("main.py"):
            print(" Error: main.py no encontrado")
            print("   Ejecuta este script desde el directorio SensoraCoreApp")
            input("Presiona Enter para continuar...")
            return
        
        if not check_dependencies():
            print(" Error: No se pudieron instalar todas las dependencias")
            input("Presiona Enter para continuar...")
            return
        
        exe_name = get_executable_name()
        
        if not os.path.exists("dist"):
            os.makedirs("dist")
            print(" Creada carpeta 'dist'")
        
        final_exe_name = check_existing_file(exe_name)
        
        print(f"\n Iniciando compilación de '{final_exe_name}.exe'...")
        
        if build_executable(final_exe_name):
            exe_path = f"dist/{final_exe_name}.exe"
            
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path)
                size_mb = file_size / (1024 * 1024)
                
                print("\n ¡Ejecutable generado exitosamente!")
                print(f" Ubicación: {exe_path}")
                print(f" Tamaño: {size_mb:.2f} MB")
                print(f" Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("\n Instrucciones:")
                print(f"1. Copia {final_exe_name}.exe a cualquier carpeta")
                print("2. Asegúrate que el ESP32 esté configurado y encendido")
                print(f"3. Ejecuta {final_exe_name}.exe")
                
                try:
                    exe_files = [f for f in os.listdir("dist") if f.endswith(".exe")]
                    if len(exe_files) > 1:
                        print(f"\n Otros ejecutables en 'dist': {', '.join(exe_files)}")
                except Exception:
                    pass
                    
            else:
                print("  El archivo se generó pero no se pudo encontrar en 'dist'")
        else:
            print("\n Error al generar el ejecutable")
            print("Revisa los mensajes de error anteriores")
        
        cleanup(final_exe_name)
        print("\n Proceso completado")
        
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        print("El proceso no se completó correctamente")
    
    finally:
        input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    main()
