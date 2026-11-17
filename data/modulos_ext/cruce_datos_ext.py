# data/modulos_ext/cruce_datos_ext.py

import streamlit as st
import pandas as pd
from backend.db_operaciones.lector_excel import obtener_hojas
from backend.cruce_archivos.comparador_ext import fn_cruzar_datos_ext
import time

def renderizar_cruce():
    st.subheader("Cruce e Inyección de Datos")
    
    aviso_verif_previa = st.warning("⚠️ Asegúrese de haber ejecutado la 'Verificación de duplicados' previamente para garantizar un cruce limpio.")
    
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.error("Seleccione una base de datos activa en el menú lateral.")
        return
        
    dir_db_activa = f"data/{acceso_db_funciones}"
    hojas_principales = obtener_hojas(dir_db_activa)
    
    if not hojas_principales:
        st.error("No se pudo leer la estructura de la base principal.")
        return
        
    select_hoja_principal = st.selectbox("Seleccione la hoja de la base principal:", options=hojas_principales)
    
    file_cruce_ext = st.file_uploader("Cargue el archivo externo depurado (.xlsx, .xls, .csv):", type=["xlsx", "xls", "csv"], key="upd_cruce")
    
    if file_cruce_ext is not None:
        try:
            df_ext = None
            select_hoja_cruce_ext = None
            
            if file_cruce_ext.name.endswith('.csv'):
                df_ext = pd.read_csv(file_cruce_ext, nrows=0)
            else:
                motor = "openpyxl" if file_cruce_ext.name.endswith('.xlsx') else "xlrd"
                try:
                    lector_ext = pd.ExcelFile(file_cruce_ext, engine=motor)
                except Exception:
                    motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                    try:
                        lector_ext = pd.ExcelFile(file_cruce_ext, engine=motor_alt)
                    except Exception:
                        lector_ext = None
                        df_ext = pd.read_html(file_cruce_ext)[0]
                
                if lector_ext is not None:
                    select_hoja_cruce_ext = st.selectbox("Seleccione la hoja del archivo externo:", options=lector_ext.sheet_names)
                    df_ext = pd.read_excel(lector_ext, sheet_name=select_hoja_cruce_ext, nrows=0)
                
            # Carga de cabeceras principales
            df_prin = pd.read_excel(dir_db_activa, sheet_name=select_hoja_principal, nrows=0)
            
            st.divider()
            st.write("### Identificador Principal Fijo")
            
            # Regla fija obligatoria
            select_ci_ext = st.selectbox(
                "Seleccione la columna equivalente a CÉDULA en el archivo externo:", 
                options=df_ext.columns.tolist()
            )
            
            st.divider()
            st.write("### Mapeo de Columnas Adicionales a Cruzar")
            
            if "status_reglas_cruce" not in st.session_state:
                st.session_state["status_reglas_cruce"] = [0]
                st.session_state["contador_reglas"] = 0
                
            dic_map_cruce = {}
            regla_a_eliminar = None
            
            for r_id in st.session_state["status_reglas_cruce"]:
                col1, col2, col3 = st.columns([4, 4, 1])
                with col1:
                    base_col = st.selectbox(f"Base Principal (Regla {r_id+1}):", options=df_prin.columns.tolist(), key=f"base_cruce_{r_id}")
                with col2:
                    ext_col = st.selectbox(f"Archivo Externo (Regla {r_id+1}):", options=df_ext.columns.tolist(), key=f"ext_cruce_{r_id}")
                with col3:
                    st.write("")
                    st.write("")
                    if st.button("❌", key=f"del_cruce_{r_id}", help="Eliminar regla"):
                        regla_a_eliminar = r_id
                        
                dic_map_cruce[base_col] = ext_col
                
            if regla_a_eliminar is not None:
                st.session_state["status_reglas_cruce"].remove(regla_a_eliminar)
                st.rerun()
                
            if st.button("➕ Agregar regla de cruce"):
                st.session_state["contador_reglas"] += 1
                st.session_state["status_reglas_cruce"].append(st.session_state["contador_reglas"])
                st.rerun()
                
            st.divider()
            
            if st.button("Ejecutar Cruce de Datos", type="primary"):
                if not select_ci_ext:
                    st.warning("Debe seleccionar la columna de cédula fija.")
                else:
                    txt_estado_proceso = "ejecución en proceso, espere"
                    with st.spinner(txt_estado_proceso):
                        status, msg = fn_cruzar_datos_ext(dir_db_activa, select_hoja_principal, file_cruce_ext, select_hoja_cruce_ext, select_ci_ext, dic_map_cruce)
                        
                        if status:
                            st.success(msg)
                            time.sleep(4)
                            # Limpieza de estados de reglas antes de reiniciar
                            st.session_state["status_reglas_cruce"] = [0]
                            st.session_state["contador_reglas"] = 0
                            st.rerun()
                        else:
                            st.error(msg)
                        
        except Exception as e:
            st.error(f"Error al estructurar el cruce: {str(e)}")