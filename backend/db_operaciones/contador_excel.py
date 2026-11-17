<<<<<<< HEAD
# backend/db_operaciones/contador_excel.py

from backend.db_operaciones.lector_excel import leer_base_datos

# Inyección paramétrica de la ruta de la base de datos activa
def conteo_total_cont(dir_db_activa):
    # Lectura de la base dinámica enviando la ruta y la hoja objetivo
    frame_principal = leer_base_datos(dir_db_activa, select_hoja="EXCELENCIA")
    
    # Cálculo numérico
    filas_validas = len(frame_principal)
    
=======
# backend/db_operaciones/contador_excel.py

from backend.db_operaciones.lector_excel import leer_base_datos

# Inyección paramétrica de la ruta de la base de datos activa
def conteo_total_cont(dir_db_activa):
    # Lectura de la base dinámica enviando la ruta y la hoja objetivo
    frame_principal = leer_base_datos(dir_db_activa, select_hoja="EXCELENCIA")
    
    # Cálculo numérico
    filas_validas = len(frame_principal)
    
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
    return filas_validas