# frontend/ver_datos.py

import streamlit as st
from backend.db_operaciones.lector_excel import leer_base_datos, obtener_hojas

def renderizar_tabla():
    st.header("Visualización de Datos Generales")
    
    # Validación de acceso y obtención de ruta dinámica
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.warning("Seleccione una base de datos activa en el menú lateral.")
        return
    dir_db_activa = f"data/{acceso_db_funciones}"
    
    # Inyección de la ruta en la función del backend
    nombre_hojas = obtener_hojas(dir_db_activa)
    
    if not nombre_hojas:
        st.warning("No se encontró el archivo base o no contiene hojas legibles.")
        return

    select_hoja = st.selectbox("Seleccione la hoja a visualizar:", options=nombre_hojas)
    
    # Inyección de la ruta para lectura de datos
    frame_principal = leer_base_datos(dir_db_activa, select_hoja)
    
    if frame_principal.empty:
        st.warning(f"No hay datos en la hoja seleccionada ({select_hoja}).")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        select_col = st.selectbox("Filtrar por columna:", options=frame_principal.columns.tolist())
    with col2:
        find_datos = st.text_input("Ingresar parámetro de búsqueda:")
        
    frame_fliter = frame_principal.copy()
    if find_datos:
        frame_fliter = frame_fliter[frame_fliter[select_col].astype(str).str.contains(find_datos, case=False, na=False)]
        
    if "NUM_CONTRATO" in frame_fliter.columns:
        frame_fliter = frame_fliter.sort_values(by="NUM_CONTRATO", ascending=True)

    st.dataframe(frame_fliter, use_container_width=True)