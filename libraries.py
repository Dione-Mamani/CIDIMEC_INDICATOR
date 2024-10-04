import subprocess
import sys

# Lista de librerías necesarias
required_libraries = [
    "os",
    "datetime",
    "re",
    "roboflow",
    "openpyxl",
    "cv2",
    "time",
    "tkinter",
    "PIL",  # Pillow (Python Imaging Library)
    "pandas"
]

# Librerías que se pueden instalar con pip
pip_libraries = [
    "roboflow",
    "openpyxl",
    "opencv-python",
    "pillow",  # Se instala como 'pillow', pero se importa como 'PIL'
    "pandas"
]

# Función para instalar librerías usando pip


def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Verifica e instala las librerías necesarias
for lib in pip_libraries:
    try:
        __import__(lib)
        print(f"{lib} ya está instalada.")
    except ImportError:
        print(f"{lib} no está instalada. Instalando...")
        install_package(lib)
        print(f"{lib} se ha instalado correctamente.")

# Verifica si las librerías no pip están disponibles
for lib in required_libraries:
    try:
        __import__(lib)
        print(f"{lib} ya está instalada.")
    except ImportError:
        print(f"{lib} no se puede instalar automáticamente con pip.")
