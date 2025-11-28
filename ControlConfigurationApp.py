import datetime
import os
import shutil
import sys
from pathlib import Path

from streamlit.web import cli as stcli


# --- CLASE PARA REDIRIGIR LA SALIDA ---
class DualLogger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        # Usamos 'a' (append) para añadir al final del archivo
        self.log = open(filename, "a", encoding="utf-8", buffering=1)

    def write(self, message):
        try:
            self.terminal.write(message)
        except Exception:
            pass
        try:
            self.log.write(message)
        except Exception:
            pass

    def flush(self):
        try:
            self.terminal.flush()
            self.log.flush()
        except Exception:
            pass


def configurar_logs(base_path):
    """Activa la grabación de logs"""
    log_path = os.path.join(base_path, "application.log")

    # Redirigimos stdout (prints normales) y stderr (errores rojos)
    sys.stdout = DualLogger(log_path)
    sys.stderr = sys.stdout

    # Mensaje de inicio con fecha
    print(f"\n{'=' * 50}")
    print(f"INICIO DE SESIÓN: {datetime.datetime.now()}")
    print(f"{'=' * 50}\n")


def configurar_entorno_usuario():
    print(">>> Preparando entorno de Streamlit...")

    # 1. Definir Ruta de DESTINO (Usuario)
    home_dir = Path.home()
    dest_dir = home_dir / ".streamlit"

    # Según setup.py, la carpeta 'src' se copia a la raíz del build como 'src/'
    # Buscamos la carpeta de configuración de Streamlit dentro de src
    src_dir = os.path.join(application_path, "src", ".streamlit")

    print(f"   -> Buscando configuración en: {src_dir}")

    # 3. Comprobación de seguridad
    if not os.path.exists(src_dir):
        print(f"⚠️ ADVERTENCIA: No se encontró la carpeta en {src_dir}")
        print("   (Asegúrate de haber compilado con 'python setup.py build')")
        return

    # 4. Proceso de Copia
    try:
        # Crear carpeta destino si no existe
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)

        archivos = ["config.toml", "credentials.toml"]

        for archivo in archivos:
            origen = os.path.join(src_dir, archivo)
            destino = dest_dir / archivo

            if os.path.exists(origen):
                shutil.copy2(origen, destino)
                print(f"✅ Configuración inyectada: {archivo}")
            else:
                print(f"⚠️ No se encontró: {archivo}")

    except Exception as e:
        print(f"❌ Error configurando entorno: {e}")


if __name__ == "__main__":
    # 1. Determinar dónde estamos ejecutando (exe compilado o script directo)
    if getattr(sys, "frozen", False):
        # Si es un .exe compilado con cx_Freeze
        application_path = os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como script de Python
        application_path = os.path.dirname(os.path.abspath(__file__))

    # 2. Configurar logs antes de lanzar la app
    configurar_logs(application_path)

    # 3. Inyectar configuración de Streamlit (.streamlit/config.toml, etc.)
    configurar_entorno_usuario()

    # 4. Determinar ruta del script principal (app.py)
    # Este script es el punto de entrada que Streamlit ejecutará
    script_path = os.path.join("src", "dashboards", "dummy1", "app.py")

    # 5. Ejecutar Streamlit con el script especificado
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]

    sys.exit(stcli.main())
