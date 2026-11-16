# frontend/modulos_ext/select_column.py

# Importación de librerías y dependencias lógicas
import streamlit as st
import pandas as pd
from backend.db_operaciones.lector_excel import leer_base_datos

def renderizar_mapeo_columnas():
    st.subheader("Paso 3: Mapeo de Columnas")
    
    # Recuperación de variables globales de sesión
    archivo_fisico = st.session_state["status_archivo_fisico"]
    hoja_activa = st.session_state["hoja_activa"]
    
    try:
        # Lectura temporal optimizada de columnas externas (nrows=0 lee solo cabeceras)
        df_ext = pd.read_excel(archivo_fisico, sheet_name=hoja_activa, nrows=0)
        cols_ext = df_ext.columns.tolist()
        
        # Lectura de columnas de la base principal (hoja EXCELENCIA por defecto)
        df_prin = leer_base_datos(select_hoja="EXCELENCIA") 
        cols_prin = df_prin.columns.tolist() if not df_prin.empty else []
        
        # Inicialización del contador iterativo para las reglas de cruce
        if "contador_reglas" not in st.session_state:
            st.session_state["contador_reglas"] = 1
            
        # Diccionario local para capturar las selecciones antes de enviarlas al estado global
        mapeo_temporal = {}
        
        # Bucle de renderizado dinámico basado en el contador
        for i in range(st.session_state["contador_reglas"]):
            col1, col2 = st.columns(2)
            with col1:
                base_col = st.selectbox(f"Regla {i+1} - Columna Principal:", options=cols_prin, key=f"base_col_{i}")
            with col2:
                ext_col = st.selectbox(f"Regla {i+1} - Columna Externa:", options=cols_ext, key=f"ext_col_{i}")
            
            mapeo_temporal[base_col] = ext_col
        
        # Botón dinámico que añadirá nuevas reglas de emparejamiento de columnas
        btn_ag_reglas_col = st.button("➕ Agregar regla de columnas")
        
        if btn_ag_reglas_col:
            st.session_state["contador_reglas"] += 1
            st.rerun()
            
        # Guardado constante de las reglas en la llave de estado global
        st.session_state["status_columnas"] = mapeo_temporal
        
    except Exception as e:
        st.error(f"Error al leer la estructura de columnas: {str(e)}")