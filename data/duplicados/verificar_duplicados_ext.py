# data/modulos_ext/verificar_duplicados_ext.py

import streamlit as st
import pandas as pd
from backend.cruce_archivos.comparador_ext import fn_verificar_dupicados_ext
import time

def renderizar_verificacion():
    st.subheader("Verificación Aislada de Duplicados")
    st.write("Identifique y extraiga registros repetidos en un archivo externo antes de cruzarlo.")
    
    archivo_cargado = st.file_uploader("Cargue el archivo externo (.xlsx, .xls, .csv):", type=["xlsx", "xls", "csv"], key="upd_verif")
    
    if archivo_cargado is not None:
        try:
            df_temp = None
            hoja_activa_ext = None
            
            # Validación y lectura reactiva según el tipo de archivo
            if archivo_cargado.name.endswith('.csv'):
                df_temp = pd.read_csv(archivo_cargado, nrows=0)
            else:
                motor = "openpyxl" if archivo_cargado.name.endswith('.xlsx') else "xlrd"
                try:
                    lector_hojas_ext_duplicados = pd.ExcelFile(archivo_cargado, engine=motor)
                except Exception:
                    motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                    try:
                        lector_hojas_ext_duplicados = pd.ExcelFile(archivo_cargado, engine=motor_alt)
                    except Exception:
                        lector_hojas_ext_duplicados = None
                        df_temp = pd.read_html(archivo_cargado)[0]
                
                # Renderizado del selector solo si es un Excel válido
                if lector_hojas_ext_duplicados is not None:
                    select_hoja_ext_duplicados = st.selectbox("Seleccione la hoja a verificar:", options=lector_hojas_ext_duplicados.sheet_names)
                    hoja_activa_ext = select_hoja_ext_duplicados
                    df_temp = pd.read_excel(lector_hojas_ext_duplicados, sheet_name=select_hoja_ext_duplicados, nrows=0)
                    
            if df_temp is not None:
                columnas_disponibles = df_temp.columns.tolist()
                
                # Selector de columna ÚNICA para verificación
                select_columna_verif_ext = st.selectbox(
                    "Seleccione la columna para validar duplicidad (ej. NUM_CONTRATO):", 
                    options=columnas_disponibles
                )
                
                if st.button("Ejecutar Verificación de Duplicados", type="primary"):
                    if not select_columna_verif_ext:
                        st.warning("Debe seleccionar una columna para la validación.")
                    else:
                        txt_estado_proceso = "ejecución en proceso, espere"
                        with st.spinner(txt_estado_proceso):
                            status, msg, ruta = fn_verificar_dupicados_ext(archivo_cargado, select_columna_verif_ext, hoja_activa_ext)
                            
                            if status:
                                st.success(msg)
                                if ruta:
                                    st.info(f"Archivo exportado localmente en: **{ruta}**")
                                time.sleep(4)  # Pausa de 4 segundos antes de recargar la página
                                st.rerun()
                            else:
                                st.error(msg)
                            
        except Exception as e:
            st.error(f"Error estructural insalvable (Archivo severamente dañado). Detalle: {str(e)}")