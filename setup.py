import sys
from cx_Freeze import setup, Executable

print(">>> Empaquetando todo el contenido de la carpeta 'src'...")

build_exe_options = {
    "packages": ["streamlit", "pandas", "numpy", "altair"],
    
    # COPIAMOS LA CARPETA SRC COMPLETA
    # Origen: "src" (la carpeta real en tu disco)
    # Destino: "dashboard/src" (la carpeta dentro del exe)
    "include_files": [
        ("src", "src")
    ]
}

setup(
    name = "PrototipoStreamlit",
    version = "1.0",
    description = "App con estructura estandar",
    options = {"build_exe": build_exe_options},
    executables = [Executable("ControlConfigurationApp.py", base=None,icon="favicon.ico")]
)