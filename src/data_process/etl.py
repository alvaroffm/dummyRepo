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

    return df


def obtener_mensaje_estado():
    """
    Función simple para devolver un texto (reemplaza tu dummy_script)
    """

    return "Sistemas de datos: ONLINE"
