import os
import shutil

from cx_Freeze import Executable, setup

# --- BLOQUE DE LIMPIEZA ---
if os.path.exists("build"):
    print("🧹 Eliminando carpeta 'build' antigua...")
    try:
        shutil.rmtree("build")
        print("✅ Carpeta 'build' eliminada.")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar la carpeta 'build': {e}")
# --------------------------

print(">>> Empaquetando todo el contenido de la carpeta 'src'...")

build_exe_options = {
    "packages": ["streamlit", "pandas", "numpy", "altair"],
    # COPIAMOS LA CARPETA SRC COMPLETA
    # Origen: "src" (la carpeta real en tu disco)
    # Destino: "dashboard/src" (la carpeta dentro del exe)
    "include_files": [("src", "src")],
}

setup(
    name="ControlConfigurationApp",
    version="0.1",
    description="App con estructura estandar",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("ControlConfigurationApp.py", base=None, icon="favicon.ico")
    ],
)
