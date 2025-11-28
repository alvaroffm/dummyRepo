# --- CORRECCIÓN DE RUTAS (MAGIC PATH FIX) ---
# Esta función ajusta sys.path para que Python pueda importar desde 'src'
# Es necesaria cuando Streamlit ejecuta apps desde subcarpetas profundas
def ajustar_path_proyecto():
    """
    Ajusta sys.path para que los módulos en 'src' sean importables desde cualquier profundidad.

    Ejemplo: Si app.py está en src/dashboards/dummy1/, esta función sube 3 niveles
    para llegar a la raíz del proyecto (donde está 'src') y la añade a sys.path.
    """
    import os
    import sys

    # Obtener la ruta absoluta del archivo actual (utils.py o quien llame a esto)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Subir 2 niveles para llegar a la raíz desde dashboards/
    # dashboards (0) -> src (1) -> dummyRepo (2)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    # Añadir a sys.path si no está ya
    if project_root not in sys.path:
        sys.path.append(project_root)
