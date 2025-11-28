# Prototipo Streamlit - DummyRepo

Una aplicación de **Control Configuration Dashboard** con Streamlit que simula un sistema de monitoreo de sensores. El proyecto incluye una estructura modular con procesamiento de datos (ETL) y dashboards interactivos compilables a ejecutable.

## 📁 Estructura del Proyecto

```
dummyRepo/
├── ControlConfigurationApp.py       # Punto de entrada principal (ejecutable/script)
├── setup.py                         # Configuración para compilar con cx_Freeze
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── src/
│   ├── __init__.py
│   ├── data_process/
│   │   ├── __init__.py
│   │   └── etl.py                  # Módulo ETL: genera datos simulados
│   └── dashboards/
│       ├── utils.py                # Utilidades (ajuste de rutas)
│       └── dummy1/
│           ├── app.py              # Aplicación Streamlit principal
│           └── dummy_script.py     # Script auxiliar
├── mi_entorno/                      # Entorno virtual (si está incluido)
└── build/                           # Artefactos compilados (cx_Freeze)
```

## 📊 Componentes Principales

### 1. **ControlConfigurationApp.py** (Punto de Entrada)
- Script que inicia la aplicación Streamlit
- Gestiona logs en `application.log`
- Inyecta configuración de Streamlit (`.streamlit/config.toml`, etc.)
- Compatible tanto con ejecución directa como ejecutable compilado

**Funciones principales:**
- `DualLogger`: Clase que redirige stdout/stderr tanto a consola como a archivo
- `configurar_logs()`: Inicializa grabación de logs con timestamp
- `configurar_entorno_usuario()`: Copia archivos de configuración de Streamlit a `~/.streamlit/`

### 2. **src/data_process/etl.py** (Módulo de Datos)
- Simula un proceso **ETL** (Extract, Transform, Load)
- Genera datos aleatorios de sensores para demostración

**Funciones:**
- `obtener_datos_sensores()`: Crea un DataFrame con 20 registros aleatorios de 3 columnas:
  - **Presión** (valores aleatorios)
  - **Temperatura** (valores aleatorios)
  - **Vibración** (valores aleatorios)
- `obtener_mensaje_estado()`: Devuelve estado del sistema ("ONLINE")

### 3. **src/dashboards/dummy1/app.py** (Aplicación Streamlit)
Dashboard interactivo que:
- Ajusta rutas automáticamente para importar módulos desde `src/`
- Obtiene datos del módulo ETL
- Muestra estado del sistema
- Renderiza dos columnas:
  - **Tendencias**: Gráfico de líneas con evolución de datos
  - **Distribución**: Gráfico de barras (Presión)
- Tabla detallada con datos procesados

**Funciones:**
- `arreglar_ruta_raiz()`: Añade la raíz del proyecto a `sys.path` (obligatorio antes de importaciones)
- `obtener_ruta_icono()`: Busca recursivamente un icono personalizado
- `main()`: Función principal con lógica de UI

### 4. **src/dashboards/utils.py** (Utilidades)
Contiene la función `ajustar_path_proyecto()` para resolver importaciones desde subcarpetas.

## 🚀 Uso

### Opción 1: Ejecutar como Script (Desarrollo)

```powershell
# Activar el entorno virtual (si está incluido)
.\mi_entorno\Scripts\Activate.ps1

# O crear uno nuevo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Ejecutar la app desde la raíz del proyecto
python ControlConfigurationApp.py
```

Esto iniciará Streamlit en `http://localhost:8501` con la aplicación en ejecución.

### Opción 2: Ejecutar Streamlit Directamente

```powershell
# Desde la raíz del proyecto
streamlit run src/dashboards/dummy1/app.py
```

### Opción 3: Compilar a Ejecutable (cx_Freeze)

```powershell
# Compilar el proyecto
python setup.py build

# El ejecutable se encontrará en:
# .\build\exe.win-amd64-3.12\ControlConfigurationApp.exe
```

**Nota:** El `setup.py` incluye automáticamente la carpeta `src` en el ejecutable.

## 📦 Dependencias

Las principales dependencias son:

- **streamlit** (>=1.0): Framework para dashboards interactivos
- **pandas** (>=1.0): Manipulación de datos
- **numpy**: Computación numérica
- **altair**: Visualizaciones (usado por Streamlit)
- **cx-Freeze**: Empaquetamiento a ejecutable (desarrollo)

Para instalar:

```powershell
pip install -r requirements.txt
```

Ver `requirements.txt` para la lista completa con versiones.

## 🔧 Configuración de Streamlit

Los archivos de configuración se encuentran en `src/.streamlit/`:
- `config.toml`: Configuración de Streamlit
- `credentials.toml`: Credenciales (si las hay)

Estos se copian automáticamente a `~/.streamlit/` al ejecutar `ControlConfigurationApp.py`.

## 📝 Comentarios en el Código

Todos los scripts han sido actualizados con comentarios claros y precisos:
- **ControlConfigurationApp.py**: Documentado en pasos numerados (1-5)
- **src/dashboards/dummy1/app.py**: Secciones bien marcadas con docstrings
- **src/dashboards/utils.py**: Función con documentación completa
- **src/data_process/etl.py**: Docstrings descriptivos

## 🐛 Troubleshooting

### Error: "No module named 'src'"
Asegúrate de ejecutar desde la **raíz del proyecto** (`dummyRepo/`).

### Error: "favicon.ico not found"
El icono es opcional. La app usará ✈️ como fallback si no lo encuentra.

### Logs no se graban
Verifica permisos de escritura en el directorio de la aplicación. Los logs se guardan en `application.log`.

## 📄 Licencia

Este es un proyecto de prototipo/demostración. Ajusta según tus necesidades.

---

**Última actualización:** Noviembre 2025
