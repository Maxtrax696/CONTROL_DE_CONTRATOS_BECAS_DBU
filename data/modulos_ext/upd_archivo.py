# data/modulos_ext/upd_archivo.py

import streamlit as st

def renderizar_carga():
    st.subheader("Paso 1: Carga de Archivo Externo")
    
    archivo_cargado = st.file_uploader(
        "Seleccione el archivo externo (.xlsx, .xls, .csv):", 
        type=["xlsx", "xls", "csv"]
    )
    
    if archivo_cargado is not None:
        st.session_state["file_key"] = archivo_cargado
        st.success(f"Archivo '{archivo_cargado.name}' cargado exitosamente en memoria.")
    else:
        st.session_state["file_key"] = None
        st.session_state["storage_key"] = None
        st.session_state["columnas_key"] = {}