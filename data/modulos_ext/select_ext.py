# data/modulos_ext/select_ext.py

import streamlit as st
import pandas as pd

def renderizar_seleccion_hoja():
    archivo_fisico = st.session_state["file_key"]
    
    st.subheader("Paso 2: Selección de Hojas")
    
    try:
        # Extracción dinámica de la base principal
        lista_hojas = pd.ExcelFile("data/excelencia total.xlsx").sheet_names
        
        # Componente de selección para la base principal
        informe_inyectados = st.selectbox("Seleccione la hoja de destino en la base principal:", options=lista_hojas)
        
        if archivo_fisico.name.endswith('.csv'):
            box_select_hoja = "CSV_Unico"
            st.info("Archivo CSV detectado. No requiere selección de hoja externa.")
        else:
            motor = "openpyxl" if archivo_fisico.name.endswith('.xlsx') else "xlrd"
            try:
                lector_datos_externos = pd.ExcelFile(archivo_fisico, engine=motor)
            except Exception:
                motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                lector_datos_externos = pd.ExcelFile(archivo_fisico, engine=motor_alt)
                
            box_select_hoja = st.selectbox("Seleccione la hoja externa a procesar:", options=lector_datos_externos.sheet_names)
            
        btn_hoja_confirmada = st.button("Confirmar Hojas")
        
        if btn_hoja_confirmada:
            # Registro en el estado global
            st.session_state["hoja_key"] = informe_inyectados
            st.session_state["storage_key"] = box_select_hoja
            st.session_state["columnas_key"] = {}
            st.success("Hojas confirmadas correctamente.")
            st.rerun()
            
    except Exception as e:
        try:
            if not archivo_fisico.name.endswith('.csv'):
                df_html = pd.read_html(archivo_fisico)[0]
                st.session_state["hoja_key"] = informe_inyectados
                st.session_state["storage_key"] = "HTML_Unico"
                st.success("Archivo HTML estructurado detectado.")
                st.rerun()
        except Exception as ex:
            st.error(f"Error estructural: {str(e)} | {str(ex)}")
            st.stop()