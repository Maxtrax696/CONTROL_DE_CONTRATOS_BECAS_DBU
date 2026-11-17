<<<<<<< HEAD
# backend/db_operaciones/crear_archivo_xlsx.py

# Importación de la librería Pandas para la creación estructurada del Excel
import pandas as pd
import os

def fun_crear_plantilla(input_nombre_archivo, lista_hojas, lista_columnas):
    # Limpieza y formateo del nombre del archivo asegurando la extensión .xlsx
    nombre_final = f"{input_nombre_archivo.strip()}.xlsx" if not input_nombre_archivo.endswith('.xlsx') else input_nombre_archivo.strip()
    
    # Directorio de guardado (asume la existencia de la carpeta 'data')
    directorio_salida = "data"
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    # Ruta absoluta/relativa del nuevo archivo
    ruta_salida = f"{directorio_salida}/{nombre_final}"
    
    # Variable para el DataFrame vacío estructurado únicamente con las cabeceras solicitadas
    frame_vacio = pd.DataFrame(columns=lista_columnas)
    
    try:
        # Uso de ExcelWriter con motor openpyxl para generar un archivo desde cero
        with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
            # Iteración sobre la lista de hojas para inyectar la misma estructura tabular en cada una
            for hoja in lista_hojas:
                frame_vacio.to_excel(writer, sheet_name=hoja, index=False)
        
        # Variable que confirmará el estado exitoso de la operación
        status_creacion = True
        return status_creacion, f"Archivo '{nombre_final}' creado exitosamente."
        
    except Exception as e:
        # Captura de errores del sistema operativo o permisos de escritura
        status_creacion = False
=======
<<<<<<< HEAD
# backend/db_operaciones/crear_archivo_xlsx.py

# Importación de la librería Pandas para la creación estructurada del Excel
import pandas as pd
import os

def fun_crear_plantilla(input_nombre_archivo, lista_hojas, lista_columnas):
    # Limpieza y formateo del nombre del archivo asegurando la extensión .xlsx
    nombre_final = f"{input_nombre_archivo.strip()}.xlsx" if not input_nombre_archivo.endswith('.xlsx') else input_nombre_archivo.strip()
    
    # Directorio de guardado (asume la existencia de la carpeta 'data')
    directorio_salida = "data"
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    # Ruta absoluta/relativa del nuevo archivo
    ruta_salida = f"{directorio_salida}/{nombre_final}"
    
    # Variable para el DataFrame vacío estructurado únicamente con las cabeceras solicitadas
    frame_vacio = pd.DataFrame(columns=lista_columnas)
    
    try:
        # Uso de ExcelWriter con motor openpyxl para generar un archivo desde cero
        with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
            # Iteración sobre la lista de hojas para inyectar la misma estructura tabular en cada una
            for hoja in lista_hojas:
                frame_vacio.to_excel(writer, sheet_name=hoja, index=False)
        
        # Variable que confirmará el estado exitoso de la operación
        status_creacion = True
        return status_creacion, f"Archivo '{nombre_final}' creado exitosamente."
        
    except Exception as e:
        # Captura de errores del sistema operativo o permisos de escritura
        status_creacion = False
=======
# backend/db_operaciones/crear_archivo_xlsx.py

# Importación de la librería Pandas para la creación estructurada del Excel
import pandas as pd
import os

def fun_crear_plantilla(input_nombre_archivo, lista_hojas, lista_columnas):
    # Limpieza y formateo del nombre del archivo asegurando la extensión .xlsx
    nombre_final = f"{input_nombre_archivo.strip()}.xlsx" if not input_nombre_archivo.endswith('.xlsx') else input_nombre_archivo.strip()
    
    # Directorio de guardado (asume la existencia de la carpeta 'data')
    directorio_salida = "data"
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    # Ruta absoluta/relativa del nuevo archivo
    ruta_salida = f"{directorio_salida}/{nombre_final}"
    
    # Variable para el DataFrame vacío estructurado únicamente con las cabeceras solicitadas
    frame_vacio = pd.DataFrame(columns=lista_columnas)
    
    try:
        # Uso de ExcelWriter con motor openpyxl para generar un archivo desde cero
        with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
            # Iteración sobre la lista de hojas para inyectar la misma estructura tabular en cada una
            for hoja in lista_hojas:
                frame_vacio.to_excel(writer, sheet_name=hoja, index=False)
        
        # Variable que confirmará el estado exitoso de la operación
        status_creacion = True
        return status_creacion, f"Archivo '{nombre_final}' creado exitosamente."
        
    except Exception as e:
        # Captura de errores del sistema operativo o permisos de escritura
        status_creacion = False
>>>>>>> 0b7154d72bff2a5861fc17effcf996fc49c975ed
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
        return status_creacion, f"Error técnico al crear el archivo: {str(e)}"