import logging  # <--- NECESARIO PARA EL LOG
import os
import sys

import streamlit as st


# --- 1. BLOQUE DE AJUSTE DE RUTAS (OBLIGATORIO) ---
def arreglar_ruta_raiz():
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    # Subimos 3 niveles: dummy1 -> dashboards -> src -> RAÍZ PROYECTO
    ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..", "..", ".."))
    if ruta_raiz not in sys.path:
        sys.path.append(ruta_raiz)


arreglar_ruta_raiz()

# --- 2. IMPORTACIONES DEL PROYECTO ---
try:
    from src.data_process.etl import obtener_datos_sensores, obtener_mensaje_estado
except ImportError as e:
    st.error(f"❌ Error importando ETL: {e}")
    # Registramos el error en el log también
    logging.error(f"Error crítico importando módulos: {e}")
    st.stop()


# --- 3. FUNCIONES DE UTILIDAD ---
def obtener_ruta_icono(nombre_icono="favicon.ico"):
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    while True:
        ruta_potencial = os.path.join(ruta_actual, nombre_icono)
        if os.path.exists(ruta_potencial):
            return ruta_potencial
        ruta_padre = os.path.dirname(ruta_actual)
        if ruta_padre == ruta_actual:
            return None
        ruta_actual = ruta_padre


# --- 4. APLICACIÓN PRINCIPAL ---
def main():
    # -- Configuración Inicial --
    ruta_icono = obtener_ruta_icono("favicon.ico")
    icono_final = ruta_icono if ruta_icono else "✈️"

    st.set_page_config(
        page_title="Dashboard Airbus", page_icon=icono_final, layout="wide"
    )

    # -- Lógica de la App --
    st.title("✈️ Dashboard Dummy 1")

    try:
        # Mensaje de estado
        st.info(f"Estado del Sistema: {obtener_mensaje_estado()}")

        # Obtenemos los datos brutos
        try:
            df = obtener_datos_sensores()
            if "log_datos_recibidos" not in st.session_state:
                logging.info("✅ Datos cargados desde ETL correctamente.")

                # Marcamos como enviado para que futuras interacciones (filtros, clicks) no lo repitan
                st.session_state["log_datos_recibidos"] = True
        except Exception:
            st.error("❌ Error obteniendo datos de sensores.")
            logging.error("Error obteniendo datos de sensores desde ETL.")
            return

        # --- SECCIÓN DEL MENÚ DESPLEGABLE ---
        st.markdown("### Configuración de Vista")
        opciones_filtro = [
            "Vista General (Todos)",
            "Solo Presión",
            "Solo Temperatura",
            "Solo Vibración",
        ]

        seleccion = st.selectbox("Seleccione la métrica a analizar:", opciones_filtro)

        # --- LÓGICA DE FILTRADO ---
        if seleccion == "Solo Presión":
            # Filtramos solo la columna Presión si existe
            if "Presión" in df.columns:
                df_view = df[["Presión"]]
            else:
                st.warning("Columna 'Presión' no encontrada en los datos.")
                df_view = df
        elif seleccion == "Solo Temperatura":
            if "Temperatura" in df.columns:
                df_view = df[["Temperatura"]]
            else:
                df_view = df
        elif seleccion == "Solo Vibración":
            if "Vibración" in df.columns:
                df_view = df[["Vibración"]]
            else:
                df_view = df
        else:
            # Vista General
            df_view = df

        # --- VISUALIZACIÓN ---
        st.subheader(f"📊 Análisis: {seleccion}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Tendencias Temporales**")
            st.line_chart(df_view)
        with col2:
            st.markdown("**Datos Detallados**")
            st.dataframe(df_view, width="stretch")

    except Exception as e:
        st.error(f"Error procesando datos: {e}")
        logging.error(f"Excepción en el dashboard: {e}")

    # --- PUNTO DE CONTROL DE CARGA (ANTI-SPAM) ---
    # Verificamos si ya hemos enviado el log en esta sesión de usuario.
    if "log_inicio_enviado" not in st.session_state:
        # Si no existe la variable, es la primera carga: escribimos en el log
        logging.info("✅ DASHBOARD CARGADO Y RENDERIZADO CORRECTAMENTE")

        # Marcamos como enviado para que futuras interacciones (filtros, clicks) no lo repitan
        st.session_state["log_inicio_enviado"] = True


if __name__ == "__main__":
    main()
