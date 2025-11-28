# Prototipo Streamlit - DummyRepo

Este repositorio contiene un prototipo de dashboard construido con Streamlit y una pequeña capa ETL de ejemplo. Durante el arranque se instala un `DualLogger` que duplica la salida a consola y a un fichero de log (`info.log`) e intenta capturar la salida de `logging` para que los mensajes (incluyendo los de Streamlit) queden registrados.

## Estructura relevante

```
dummyRepo/
├── ControlConfigurationApp.py       # Punto de entrada principal (script/launcher)
├── setup.py                         # Empaquetado con cx_Freeze (incluye carpeta src)
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── src/
│   ├── data_process/
│   │   └── etl.py                   # Módulo ETL: genera datos simulados
│   └── dashboards/
│       ├── utils.py                 # Utilidades (ajuste de sys.path)
│       └── dummy1/
│           ├── app.py               # App Streamlit (Dashboard Airbus)
│           └── dummy_script.py      # Script auxiliar (mensaje simple)
├── mi_entorno/                      # Entorno virtual (opcional)
└── build/                           # Artefactos compilados por cx_Freeze
```

## Comportamiento actual (resumen técnico)

- El lanzador `ControlConfigurationApp.py` implementa `DualLogger`, que reemplaza `sys.stdout` y `sys.stderr` por un objeto que escribe tanto en la consola original como en `info.log` (archivo en la carpeta donde se ejecuta el script / ejecutable).
- Tras reemplazar `sys.stdout` se reconfigura el módulo `logging` (con `logging.basicConfig(..., stream=sys.stdout, force=True)`) para intentar que los mensajes de logging (de Streamlit y otros módulos) se redirijan al `DualLogger` y queden en el fichero.
- `configurar_entorno_usuario()` copia archivos de configuración (p. ej. `config.toml`, `credentials.toml`) desde la copia incluida en el build:
  - ruta preferida: `dashboard/src/config/`
  - fallback: `src/config/`
- El script construye la ruta absoluta del `app.py` esperado en `dashboard/src/dashboards/dummy1/app.py` y usa un fallback `src/dashboards/dummy1/app.py` si el anterior no existe.
- Cuando lanza Streamlit, añade flags que ayudan a que la URL se muestre y la salida no quede en modo headless:
  - `--browser.serverAddress=localhost`
  - `--server.headless=false`

## Detalles por componente

### `ControlConfigurationApp.py`
- `DualLogger` (clase): duplica la salida a la terminal original y a `info.log`. Implementa `write`, `flush` y maneja `isatty`/`fileno` a través de la terminal real cuando es posible.
- `configurar_logs(application_path)`: crea/rota el log `info.log`, reemplaza `sys.stdout`/`sys.stderr` y reconfigura `logging` para usar `sys.stdout`.
- `configurar_entorno_usuario(application_path)`: copia archivos de configuración de la copia incluida en el build hacia `~/.streamlit/`.
- Lanzamiento: calcula `script_path` y ejecuta `stcli.main()`.

### `src/data_process/etl.py`
- `obtener_datos_sensores()`: genera un `DataFrame` de 20 filas con columnas `Presión`, `Temperatura`, `Vibración` (datos aleatorios).
- `obtener_mensaje_estado()`: devuelve un string de estado ("Sistemas de datos: ONLINE").

### `src/dashboards/dummy1/app.py` (Dashboard)
- Ajusta `sys.path` subiendo 3 niveles para poder importar `src.data_process.etl`.
- Configura la página con `st.set_page_config(...)` (título: "Dashboard Airbus").
- Permite seleccionar vistas (Presión/Temperatura/Vibración) y muestra gráficos de línea y tablas.
- Emite mensajes con `logging.info(...)` para marcar eventos (datos cargados, dashboard renderizado).

### `src/dashboards/utils.py`
- `ajustar_path_proyecto()`: función auxiliar para añadir la raíz del proyecto a `sys.path` (sube 2 niveles desde `dashboards/` en la implementación actual).

## Cómo ejecutar (Windows, PowerShell)

1) Activar entorno virtual (si existe):

```powershell
.\mi_entorno\Scripts\Activate.ps1
```

2) Ejecutar el launcher (recomendado — captura logs y copia configuración):

```powershell
python ControlConfigurationApp.py
```

3) O ejecutar Streamlit directamente para desarrollo:

```powershell
streamlit run src/dashboards/dummy1/app.py
```

4) Compilar con `cx_Freeze`:

```powershell
python setup.py build
```

## Dependencias

Las dependencias principales que necesita el proyecto son (ver `requirements.txt`):

- streamlit
- pandas
- numpy
- altair
- cx-Freeze (solo para empaquetado)

## Notas y recomendaciones

- Si no ves los banners de Streamlit en consola al ejecutar `ControlConfigurationApp.py`, revisa el orden de importación de Streamlit en tu entorno: algunos mensajes se pueden imprimir durante la importación del paquete, antes de que `sys.stdout` sea reemplazado. La implementación actual intenta reconfigurar `logging` para redirigir la salida a `DualLogger`, pero capturar impresiones a muy bajo nivel (C) podría requerir redirección de descriptores de archivo (`os.dup2`) si fuera necesario.
- `configurar_entorno_usuario()` busca `config.toml` en la copia incluida en el build (`dashboard/src/config`), si tu `setup.py` copia los archivos a otra ruta, actualiza esta función.
- Si quieres que genere un `requirements.txt` con versiones exactas desde `mi_entorno`, puedo activarlo y volcar `pip freeze`.

---

**Última actualización:** $(Get-Date -Format "yyyy-MM-dd")
