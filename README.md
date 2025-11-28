# Prototipo Streamlit - DummyRepo (estado actualizado)

Este repositorio contiene un prototipo de dashboard Streamlit con una capa ETL de ejemplo.
El launcher (`ControlConfigurationApp.py`) instala un `DualLogger` que duplica la salida a consola y a `info.log`.

## Archivos clave

- `ControlConfigurationApp.py`: lanzador principal. Sustituye `sys.stdout`/`sys.stderr` por `DualLogger`, reconfigura `logging` para apuntar a `sys.stdout` y lanza Streamlit con `stcli.main()`.
- `setup.py`: configuración de `cx_Freeze` (incluye la carpeta `src` en el build y define la versión).
- `requirements.txt`: dependencias mínimas (`streamlit`, `pandas`, `numpy`, `altair`, `cx-Freeze`).
- `src/data_process/etl.py`: módulo ETL que genera datos simulados (Presión, Temperatura, Vibración).
- `src/dashboards/dummy1/app.py`: aplicación Streamlit; ajusta `sys.path`, importa `etl`, muestra gráficos y tablas.
- `src/dashboards/utils.py`: utilidades para ajustar `sys.path` desde carpetas profundas.

## Notas sobre el logger y Streamlit

- `DualLogger` implementa `write()` y `flush()` y reemplaza `sys.stdout`/`sys.stderr`.
- Inmediatamente después de reemplazar `sys.stdout`, `configurar_logs()` reconfigura `logging` con `stream=sys.stdout` para que los mensajes de logging (incluyendo los que Streamlit emite a través de logging) se registren en `info.log`.
- Para capturar impresiones de muy bajo nivel (por ejemplo código C que escribe directamente al descriptor de archivo 1/2), se requeriría redirección de descriptores (`os.dup2`). Actualmente el proyecto usa la solución basada en `logging` y `DualLogger`.

## Ejecución (PowerShell)

Activar entorno (si existe):

```powershell
.\mi_entorno\Scripts\Activate.ps1
```

Ejecutar el lanzador (recomendado):

```powershell
python ControlConfigurationApp.py
```

Ejecutar Streamlit en modo desarrollo:

```powershell
streamlit run src/dashboards/dummy1/app.py
```

Compilar con cx_Freeze:

```powershell
python setup.py build
```

## Estado actual de los scripts

- `ControlConfigurationApp.py`: logger activo, rutas al `app.py` calculadas con fallback.
- `src/dashboards/dummy1/app.py`: vista interactiva con selección de métricas y visualizaciones.
- `src/data_process/etl.py`: funciones `obtener_datos_sensores()` y `obtener_mensaje_estado()`.

---

**Última actualización:** $(Get-Date -Format "yyyy-MM-dd")
