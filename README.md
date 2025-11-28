# PrototipoApp / Dashboard

Este proyecto es una aplicación de dashboard desarrollada con Streamlit para visualizar datos de sensores (Presión, Temperatura, Vibración). Está diseñado para ser empaquetado como un ejecutable independiente utilizando `cx_Freeze`.

## Descripción

La aplicación permite monitorizar el estado de sistemas y visualizar métricas en tiempo real. Incluye:
-   **Dashboard Interactivo**: Visualización de tendencias y datos detallados.
-   **Filtrado Dinámico**: Selección de métricas específicas (Presión, Temperatura, Vibración).
-   **Sistema de Logs**: Registro dual en consola y archivo (`info.log`).
-   **Configuración Automática**: Gestión de archivos de configuración de Streamlit en el entorno del usuario.

## Estructura del Proyecto

-   `ControlConfigurationApp.py`: Script principal de entrada (launcher) que configura el entorno y lanza Streamlit.
-   `setup.py`: Script de configuración para compilar el proyecto con `cx_Freeze`.
-   `src/`: Código fuente del proyecto.
    -   `dashboards/dummy1/app.py`: Lógica principal del dashboard de Streamlit.
    -   `data_process/etl.py`: Simulación de proceso ETL para generación de datos.
    -   `config/`: Archivos de configuración (`config.toml`, `credentials.toml`).

## Instalación

1.  Clona el repositorio.
2.  Crea un entorno virtual (opcional pero recomendado).
3.  Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

### Ejecución Local

Para ejecutar la aplicación en modo desarrollo:

**Opción A: Usando el launcher (recomendado para probar el flujo completo)**
```bash
python ControlConfigurationApp.py
```

**Opción B: Ejecutando directamente Streamlit**
```bash
streamlit run src/dashboards/dummy1/app.py
```

### Construcción del Ejecutable

Para generar el ejecutable independiente (Windows):

```bash
python setup.py build
```

Esto creará una carpeta `build/` con el ejecutable y todas las dependencias necesarias.

## Notas Adicionales

-   El sistema incluye un mecanismo de limpieza de logs automático (mantiene los últimos 10 inicios).
-   Al ejecutar el binario compilado, la aplicación inyectará automáticamente la configuración necesaria en la carpeta `.streamlit` del usuario.
