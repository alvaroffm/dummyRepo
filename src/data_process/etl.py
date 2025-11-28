import numpy as np
import pandas as pd


def obtener_datos_sensores():
    """
    Simula un proceso ETL (Extract, Transform, Load).
    Genera datos aleatorios para pruebas.
    """

    # Generamos 20 filas de datos aleatorios
    df = pd.DataFrame(
        np.random.randn(20, 3), columns=["Presión", "Temperatura", "Vibración"]
    )

    # Aquí podrías añadir lógica de limpieza, filtrado, etc.
    # Por ejemplo: df = df[df['Temperatura'] > 0]

    return df


def obtener_mensaje_estado():
    """Función simple para devolver un texto (reemplaza tu dummy_script)"""
    return "Sistemas de datos: ONLINE"
