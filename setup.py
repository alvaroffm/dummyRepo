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
# 1. DEFINIMOS LA VERSIÓN AQUÍ
VERSION = "0.1"
nombre_carpeta_salida = f"build/v{VERSION}_ControlConfigurationApp"
print(f"Configurando build para v{VERSION}...")
# 2. OPCIONES DE CONSTRUCCIÓN
build_exe_options = {
    "packages": ["streamlit", "pandas", "numpy", "altair"],
    # COPIAMOS LA CARPETA SRC COMPLETA
    # Origen: "src" (la carpeta real en tu disco)
    # Destino: "dashboard/src" (la carpeta dentro del exe)
    "include_files": [("src", "src")],
    "build_exe": nombre_carpeta_salida,
}
# 3. CONFIGURACIÓN FINAL
setup(
    name="ControlConfigurationApp",
    version=VERSION,
    description="App con estructura estandar",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("ControlConfigurationApp.py", base=None, icon="favicon.ico")
    ],
)
