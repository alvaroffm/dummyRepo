import datetime
import logging  # <--- IMPORTANTE: Necesario para capturar mensajes de Streamlit
import os
import shutil
import sys
from pathlib import Path

from streamlit.web import cli as stcli


# --- CLASE LOGGER MEJORADA (MIMIC TERMINAL) ---
class DualLogger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        # buffering=1 asegura que se escriba línea a línea
        self.log = open(filename, "a", encoding="utf-8", buffering=1)

    def write(self, message):
        # 1. Escribir en la terminal real (si existe)
        try:
            if self.terminal:
                self.terminal.write(message)
                self.terminal.flush()  # Forzamos que salga al momento
        except Exception:
            pass

        # 2. Escribir en el archivo de log
        try:
            self.log.write(message)
            self.log.flush()
        except Exception:
            pass

    def flush(self):
        # Necesario para cumplir con la interfaz de archivo de Python
        try:
            if self.terminal:
                self.terminal.flush()
            self.log.flush()
        except Exception:
            pass


def configurar_logs(base_path):
    nombre_log = "info.log"
    log_path = os.path.join(base_path, nombre_log)

    # --- LIMPIEZA AUTOMÁTICA (10 EJECUCIONES) ---
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                contenido = f.read()

            ejecuciones = contenido.count("INICIO DE SESIÓN")

            if ejecuciones >= 10:
                os.remove(log_path)
        except Exception:
            pass

    # --- ACTIVACIÓN DEL LOGGER ---
    # Creamos la instancia
    logger = DualLogger(log_path)

    # Reemplazamos stdout y stderr
    sys.stdout = logger
    sys.stderr = logger

    # --- PARCHE CRÍTICO PARA STREAMLIT ---
    # Forzamos a la librería logging a usar nuestro sys.stdout modificado.

    # 1. Obtenemos el logger raíz
    root_logger = logging.getLogger()

    # 2. Limpiamos handlers viejos
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # 3. Reconfiguramos para que todo vaya a nuestro DualLogger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,  # <--- Aquí ocurre la magia
        force=True,
    )

    print(f"\n{'=' * 50}")
    print(f"INICIO DE SESIÓN: {datetime.datetime.now()}")
    print(f"{'=' * 50}\n")


def configurar_entorno_usuario(application_path):
    print(">>> Preparando entorno de Streamlit...")

    # 1. Definir Ruta de DESTINO (Usuario)
    home_dir = Path.home()
    dest_dir = home_dir / ".streamlit"

    # Definimos la ruta de origen según tu estructura
    # Prioridad: dashboard/src/.streamlit (Ruta típica en cx_Freeze)
    src_dir = os.path.join(application_path, "dashboard", "src", "config")

    # Si no existe, probamos ruta directa
    if not os.path.exists(src_dir):
        src_dir = os.path.join(application_path, "src", "config")

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

    # 3. Inyectar configuración de Streamlit
    configurar_entorno_usuario(application_path)

    # 4. Determinar ruta del script principal (app.py)
    # Ruta estándar para cx_Freeze con copia de carpeta entera
    script_path = os.path.join(
        application_path, "dashboard", "src", "dashboards", "dummy1", "app.py"
    )

    # Fallback si moviste el archivo
    if not os.path.exists(script_path):
        script_path = os.path.join(
            application_path, "src", "dashboards", "dummy1", "app.py"
        )

    print(f"🚀 Lanzando script principal: {script_path}")

    # 5. Ejecutar Streamlit con el script especificado
    # AÑADIMOS FLAGS CLAVE para forzar la salida de la URL:
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
        "--browser.serverAddress=localhost",
        "--server.headless=false",
    ]

    try:
        sys.exit(stcli.main())
    except Exception as e:
        print(f"❌ ERROR FATAL EN MAIN: {e}")
