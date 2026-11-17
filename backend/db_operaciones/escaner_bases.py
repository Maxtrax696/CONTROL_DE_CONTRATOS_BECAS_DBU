<<<<<<< HEAD
# backend/db_operaciones/escaner_bases.py

# Importación de librerías del sistema
import os
import glob

def fun_lista_bases():
    # Definición de la ruta de búsqueda para archivos Excel
    ruta_busqueda = os.path.join("data", "*.xlsx")
    archivos_encontrados = glob.glob(ruta_busqueda)
    
    lista_bases = []
    
    # Iteración y filtrado de la carpeta de respaldos
    for archivo in archivos_encontrados:
        # Normalización de la ruta para evitar errores entre sistemas operativos
        archivo_norm = archivo.replace("\\", "/")
        if "backup" not in archivo_norm:
            # Extracción del nombre puro del archivo
            nombre_base = os.path.basename(archivo)
            lista_bases.append(nombre_base)
            
=======
# backend/db_operaciones/escaner_bases.py

# Importación de librerías del sistema
import os
import glob

def fun_lista_bases():
    # Definición de la ruta de búsqueda para archivos Excel
    ruta_busqueda = os.path.join("data", "*.xlsx")
    archivos_encontrados = glob.glob(ruta_busqueda)
    
    lista_bases = []
    
    # Iteración y filtrado de la carpeta de respaldos
    for archivo in archivos_encontrados:
        # Normalización de la ruta para evitar errores entre sistemas operativos
        archivo_norm = archivo.replace("\\", "/")
        if "backup" not in archivo_norm:
            # Extracción del nombre puro del archivo
            nombre_base = os.path.basename(archivo)
            lista_bases.append(nombre_base)
            
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
    return lista_bases