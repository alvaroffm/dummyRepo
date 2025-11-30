import os
import shutil

from cx_Freeze import Executable, setup


VERSION = "0.2"
nombre_carpeta_salida = f"build/v{VERSION}_ControlConfigurationApp"

if os.path.exists(nombre_carpeta_salida):
    print("🧹 Eliminando carpeta 'build' antigua...")
    try:
        shutil.rmtree(nombre_carpeta_salida)
        print("✅ Carpeta 'build' eliminada.")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar la carpeta 'build': {e}")

print(f"Configurando build para v{VERSION}...")
build_exe_options = {
    "packages": ["streamlit", "pandas", "numpy", "altair"],
    "include_files": [("src", "src")],
    "build_exe": nombre_carpeta_salida,
}

setup(
    name="ControlConfigurationApp",
    version=VERSION,
    description="App con estructura estandar",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("ControlConfigurationApp.py", base=None, icon="favicon.ico")
    ],
)
