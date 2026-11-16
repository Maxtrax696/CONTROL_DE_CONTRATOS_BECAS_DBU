# data/modulos_ext/boton_confirmar.py

import streamlit as st
import pandas as pd
from backend.cruce_archivos.comparador_ext import fn_ejecutar_cruce, extraer_duplicados, duplicados_extraer

@st.dialog("Confirmación Final de Sincronización")
def frame_conf_final():
    st.warning("Está a punto de ejecutar la sincronización masiva de datos e inyectar contratos.")
    
    # Recuperación de la hoja seleccionada dinámicamente desde el estado global
    hoja_seleccionada = st.session_state.get("hoja_key", "EXCELENCIA")
    hoja_activa_ext = st.session_state.get("storage_key", "Desconocida")
    
    # Renderizado visual pre-cruce
    st.info(f"Destino en Base Principal: `{hoja_seleccionada}` | Origen Externo: `{hoja_activa_ext}`")
    
    st.write("**Resumen de Reglas de Emparejamiento:**")
    columnas_key = st.session_state["columnas_key"]
    
    for base_col, ext_col in columnas_key.items():
        st.info(f"Base Principal: `{base_col}` ↔ Archivo Externo: `{ext_col}`")
        
    btn_ejecutar_cruce = st.button("Ejecutar Cruce Definitivo", type="primary")
    
    if btn_ejecutar_cruce:
        frame_to_cruce = st.session_state.get("frame_datos_limpios", None)
        
        if frame_to_cruce is not None:
            # Ejecución del cruce transmitiendo la hoja principal seleccionada
            estado, mensaje, conteo_inyectados = fn_ejecutar_cruce(frame_to_cruce, columnas_key, hoja_seleccionada)
            
            if estado:
                st.success(mensaje)
                st.info(f"Total de registros procesados/inyectados exitosamente: {conteo_inyectados}")
                
                # Vaciado del estado de sesión
                st.session_state["file_key"] = None
                st.session_state["storage_key"] = None
                st.session_state["hoja_key"] = None
                st.session_state["columnas_key"] = {}
                st.session_state["frame_datos_limpios"] = None
            else:
                st.error(mensaje)
        else:
            st.error("Error: No se encontraron los datos limpios en memoria.")

def renderizar_ejecucion():
    st.subheader("Paso 4: Ejecución")
    
    if not st.session_state["columnas_key"]:
        st.button("Confirmar y Cruzar Datos", disabled=True, help="Debe mapear al menos una columna.")
    else:
        btn_pre_cruce = st.button("Confirmar y Cruzar Datos")
        if btn_pre_cruce:
            try:
                archivo_fisico = st.session_state["file_key"]
                hoja_activa = st.session_state["storage_key"]
                
                if archivo_fisico.name.endswith('.csv'):
                    df_ext_full = pd.read_csv(archivo_fisico)
                else:
                    motor = "openpyxl" if archivo_fisico.name.endswith('.xlsx') else "xlrd"
                    try:
                        df_ext_full = pd.read_excel(archivo_fisico, sheet_name=hoja_activa, engine=motor)
                    except Exception:
                        motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                        df_ext_full = pd.read_excel(archivo_fisico, sheet_name=hoja_activa, engine=motor_alt)
                
                col_contrato_ext = "NUM_CONTRATO"
                
                if col_contrato_ext in df_ext_full.columns:
                    frame_to_cruce, frame_duplicados_internos = extraer_duplicados(df_ext_full, col_contrato=col_contrato_ext)
                    duplicados_extraer(frame_duplicados_internos)
                else:
                    frame_to_cruce = df_ext_full.copy()
                
                st.session_state["frame_datos_limpios"] = frame_to_cruce
                frame_conf_final()
                
            except Exception as e:
                st.error(f"Error al procesar los datos externos: {str(e)}")