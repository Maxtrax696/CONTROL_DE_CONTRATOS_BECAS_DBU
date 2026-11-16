# SISTEMA DE GESTIÓN BIENESTAR ESTUDIANTIL

## Descripción del Proyecto
Plataforma informática de escritorio desarrollada en Python y Streamlit para la gestión, control y sincronización masiva de expedientes de bienestar estudiantil. El sistema opera bajo una arquitectura modular distribuida (Frontend/Backend), aislando la interfaz gráfica de la lógica de negocio y procesamiento de datos. Realiza operaciones CRUD con escrituras atómicas sobre bases de datos dinámicas en formato Excel (`.xlsx`), garantizando la integridad referencial y estructural ante bloqueos del sistema operativo.

## Arquitectura y Árbol de Directorios
El código obedece a un patrón cliente-servidor interno, estructurado de la siguiente manera:

```text
/proyecto_bienestar
│
├── /data                               # Directorio principal de persistencia
│   ├── /backup                         # Respaldos generados previamente a cada cruce
│   ├── /duplicados                     # Bases de datos exportadas con registros en conflicto
│   ├── /security                       # Archivos de validación física (.key)
│   └── [Bases de datos dinámicas .xlsx]
│
├── /backend                            # Núcleo algorítmico y reglas de negocio
│   ├── /db_operaciones
│   │   ├── lector_excel.py             # Extracción de metadatos y lectura dinámica
│   │   ├── escritura_excel.py          # Motor de anexado seguro (if_sheet_exists='replace')
│   │   ├── contador_excel.py           # Cálculo en tiempo real de volumetría
│   │   ├── escaner_bases.py            # Detección algorítmica de archivos activos en /data
│   │   └── datos_academicos.py         # Diccionarios estáticos de mapeo (Facultades, Bancos)
│   │
│   ├── /validaciones
│   │   ├── validacion_ci.py            # Algoritmo matemático (Módulo 10) para cédulas
│   │   └── autoasignar_cont.py         # Motores lógicos de secuencias y correlativos
│   │
│   └── /cruce_archivos
│       └── comparador_ext.py           # Algoritmos de verificación cruzada y depuración
│
├── /frontend                           # Renderizado de vistas e interfaces (Streamlit)
│   ├── inicio.py                       # Dashboard de estado y contadores estadísticos
│   ├── ver_datos.py                    # Motor de filtros interactivos y renderizado tabular
│   ├── archivo_ext.py                  # Controlador del submódulo de sincronización externa
│   ├── /formularios
│   │   ├── agregar.py                  # Interfaz de inserción estructurada
│   │   ├── editar.py                   # Interfaz de alteración, autoasignación y token
│   │   └── eliminar.py                 # Interfaz de borrado lógico con barreras modales
│   │
│   └── /modulos_ext                    # Componentes modulares del cruce de datos
│       ├── select_column.py
│       ├── select_ext.py
│       ├── upd_archivo.py
│       └── boton_confirmar.py
│
├── compilar.py                         # Orquestador nativo de PyInstaller y gestión de caché
├── ejecutar_app.py                     # Script puente para inyección de servidor web local
├── main.py                             # Enrutador principal y gestión de Session State
└── icono.ico                           # Identificador gráfico del ejecutable final
```
## Especificaciones de Módulos Core

### 1. Escáner Dinámico y Escritura Atómica

- **Lectura:** Rastrea dinámicamente el directorio `/data` y permite al operador interactuar con múltiples archivos `.xlsx` sin configuraciones de código rígidas.
- **Escritura:** Utiliza `pandas.ExcelWriter` con motor `openpyxl` en modo anexado (`mode="a"`). Altera exclusivamente la pestaña específica procesada sin cargar, corromper ni sobrescribir el resto de las hojas del documento activo. Controla bloqueos del sistema operativo (`[WinError 5]`).
    

### 2. Operaciones Estructurales (CRUD)

- **Gestión de Cédulas:** Integra validación paramétrica mediante el algoritmo Módulo 10 para garantizar la exactitud del identificador nacional ecuatoriano.
- **Autoasignación de Contratos:** Evalúa el formato `YYYY-YYYY-ETIQUETA-XXXX` (ej. `2024-2025-BEA-0001`), extrae secuencias utilizando expresiones regulares (`re`) y rellena huecos de manera lógica y ordenada por bloque de periodo.
- **Mapeo por Diccionarios:** Inyecta automáticamente los códigos paramétricos de Carreras y Entidades Bancarias sobre celdas vacías basándose en selecciones validadas.
- **Seguridad de Capa Física:** El módulo de Edición bloquea la llave primaria (Contrato). El operador debe cargar en memoria un archivo Token explícito (`.key`) el cual se valida contra algoritmos del backend para habilitar la sobreescritura de dicho campo.
### 3. Sincronización Externa Masiva

- **Extracción de Duplicados:** Analiza documentos externos (`.csv`, `.xls`, `.xlsx`), localiza colisiones internas de contratos y exporta dichos registros de manera aislada al directorio `/data/duplicados/` preservando el 100% de sus columnas para auditoría manual.
- **Cruce y Emparejamiento:** Permite el mapeo visual entre columnas de ambas bases de datos. Si detecta coincidencias lógicas con base a las reglas impuestas por el operador, inyecta contratos faltantes hacia el archivo principal o, en su defecto, ingresa automáticamente estudiantes completamente nuevos a la matriz transaccional.
## Guía de Compilación y Despliegue (Ejecutable)

El sistema ha sido estructurado para empaquetarse en un único archivo ejecutable aislado (Standalone executable) en entornos Windows, ocultando la terminal y montando el servidor web interno automáticamente.

**Pasos de compilación:**
1. Instalar la librería en el entorno virtual activo: `pip install pyinstaller`.
2. Asegurar la presencia del archivo `icono.ico` y los scripts `ejecutar_app.py` y `compilar.py` en la raíz del directorio.
3. Ejecutar el orquestador destructivo de caché: `python compilar.py`.
4. El proceso generará el archivo `Control_de_Contratos_Becas_DBU.exe` en la carpeta `/dist`. Dicho ejecutable debe ubicarse obligatoriamente en la misma ruta que la carpeta `/data` para operar sobre las bases físicas.

## Stack Tecnológico y Dependencias
- **Motor Lógico:** Python 3.x
- **Interfaz de Usuario:** Streamlit (Manejo de `st.session_state`, `@st.dialog`)
- **Procesamiento de Datos:** Pandas
- **Motores I/O Excel:** Openpyxl, Xlrd
- **Empaquetado y Distribución:** PyInstaller