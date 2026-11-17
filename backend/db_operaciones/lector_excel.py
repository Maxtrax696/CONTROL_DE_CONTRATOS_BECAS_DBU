# backend/db_operaciones/lector_excel.py

import pandas as pd

def obtener_hojas(ruta_base_activa):
    try:
        hojas_archivo = pd.ExcelFile(ruta_base_activa)
        nombre_hojas = hojas_archivo.sheet_names
        return nombre_hojas
    except FileNotFoundError:
        return []

def leer_base_datos(ruta_base_activa, select_hoja):
    try:
        frame_principal = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        return frame_principal
    except (FileNotFoundError, ValueError):
        frame_principal = pd.DataFrame()
        return frame_principal