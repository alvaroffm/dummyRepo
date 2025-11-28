import os
import sys

import streamlit as st


# --- 1. BLOQUE DE AJUSTE DE RUTAS (OBLIGATORIO AL INICIO) ---
# Ajustar sys.path es necesario para que Streamlit encuentre módulos en 'src'
def arreglar_ruta_raiz():
    """
    Ajusta sys.path para importar módulos desde la carpeta 'src'.

    Esto es esencial porque app.py está en src/dashboards/dummy1/,
    pero necesita importar desde src/data_process/, que es 3 niveles arriba.
    """
    # Obtener la ruta absoluta de este archivo: .../src/dashboards/dummy1/app.py
    ruta_actual = os.path.dirname(os.path.abspath(__file__))

    # Subir 3 niveles:
    # dummy1/ -> dashboards/ -> src/ -> raíz del proyecto (dummyRepo/)
    ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..", "..", ".."))

    # Añadir la raíz a sys.path si no está ya
    if ruta_raiz not in sys.path:
        sys.path.append(ruta_raiz)


# ¡EJECUTAR LA FUNCIÓN ANTES DE CUALQUIER OTRA IMPORTACIÓN!
arreglar_ruta_raiz()

# --- 2. IMPORTACIONES DEL PROYECTO ---
# Ahora Python puede ver la carpeta 'src' desde la raíz del proyecto
try:
    # Importar funciones del módulo ETL
    from src.data_process.etl import obtener_datos_sensores, obtener_mensaje_estado
except ImportError as e:
    st.error(f"❌ Error importando ETL: {e}")
    st.stop()


# --- 3. UTILIDADES DE LA APLICACIÓN ---
def obtener_ruta_icono(nombre_icono="favicon.ico"):
    """
    Busca recursivamente un archivo de icono desde la ubicación actual
    hacia los directorios padres hasta encontrarlo.
    """
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    while True:
        ruta_potencial = os.path.join(ruta_actual, nombre_icono)
        if os.path.exists(ruta_potencial):
            return ruta_potencial
        ruta_padre = os.path.dirname(ruta_actual)
        if ruta_padre == ruta_actual:
            # Llegamos a la raíz del sistema sin encontrar el icono
            return None
        ruta_actual = ruta_padre


# --- 4. APLICACIÓN PRINCIPAL ---
def main():
    """
    Aplicación Streamlit: Control Configuration Dashboard.
    Muestra datos de sensores (simulados) con gráficos y tablas.
    """
    # Buscar icono personalizado
    ruta_icono = obtener_ruta_icono("favicon.ico")
    icono_final = ruta_icono if ruta_icono else "✈️"

    st.set_page_config(
        page_title="Control Configuration App", page_icon=icono_final, layout="wide"
    )

    st.title("✈️ Control Configuration Dashboard")

    # Obtener datos del módulo ETL y mostrar en la app
    try:
        # Mostrar estado del sistema
        st.info(f"{obtener_mensaje_estado()}")

        # Obtener datos de sensores
        data = obtener_datos_sensores()
        st.dataframe(data)

        # Layout de dos columnas: tendencias y distribución
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Tendencias")
            st.line_chart(data)

        with col2:
            st.markdown("### Distribución")
            st.bar_chart(data["Presión"])

        # Mostrar tabla detallada
        st.subheader("📋 Datos Procesados")
        st.dataframe(data, width="stretch")
    except Exception as e:
        st.error(f"Error procesando datos: {e}")


if __name__ == "__main__":
    main()
