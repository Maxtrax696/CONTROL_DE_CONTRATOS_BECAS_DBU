# data/modulos_ext/select_column.py

# Importación de librerías base
import streamlit as st
import pandas as pd

def renderizar_mapeo_columnas():
    st.subheader("Paso 3: Mapeo de Columnas")
    
    # Recuperación de variables de estado global
    archivo_fisico = st.session_state.get("file_key")
    hoja_activa = st.session_state.get("storage_key")
    hoja_key = st.session_state.get("hoja_key")
    
    if archivo_fisico is None or hoja_key is None:
        st.warning("Faltan datos de selección. Complete los pasos anteriores.")
        return

    try:
        # Lectura optimizada del archivo externo (solo cabeceras)
        if archivo_fisico.name.endswith('.csv'):
            df_ext = pd.read_csv(archivo_fisico, nrows=0)
        elif hoja_activa == "HTML_Unico":
            df_ext = pd.read_html(archivo_fisico)[0]
        else:
            motor = "openpyxl" if archivo_fisico.name.endswith('.xlsx') else "xlrd"
            try:
                df_ext = pd.read_excel(archivo_fisico, sheet_name=hoja_activa, nrows=0, engine=motor)
            except Exception:
                motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                df_ext = pd.read_excel(archivo_fisico, sheet_name=hoja_activa, nrows=0, engine=motor_alt)
            
        lista_col_ext = df_ext.columns.tolist()
        
        # Lectura optimizada de la base principal dirigida a la hoja dinámica
        df_prin = pd.read_excel("data/excelencia total.xlsx", sheet_name=hoja_key, nrows=0)
        lista_col_principal = df_prin.columns.tolist()
        
        # Inicialización de estado para reglas de mapeo reactivas
        if "reglas_ids" not in st.session_state:
            st.session_state["reglas_ids"] = [0]
            st.session_state["contador_id"] = 0
            
        dic_temp_emparejados = {}
        regla_a_eliminar = None
        
        # Bucle de renderizado para los selectores de columnas con eliminación individual
        for regla_id in st.session_state["reglas_ids"]:
            col1, col2, col3 = st.columns([4, 4, 1])
            with col1:
                base_col = st.selectbox(f"Base Principal (Regla {regla_id+1}):", options=lista_col_principal, key=f"base_{regla_id}")
            with col2:
                ext_col = st.selectbox(f"Archivo Externo (Regla {regla_id+1}):", options=lista_col_ext, key=f"ext_{regla_id}")
            with col3:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_{regla_id}", help="Eliminar regla"):
                    regla_a_eliminar = regla_id
                    
            dic_temp_emparejados[base_col] = ext_col
            
        # Lógica de eliminación y limpieza de reglas
        if regla_a_eliminar is not None:
            st.session_state["reglas_ids"].remove(regla_a_eliminar)
            st.rerun()
            
        # Asignación al estado de sesión
        st.session_state["columnas_key"] = dic_temp_emparejados
        
        # Botón iterativo para adición de nuevas reglas
        btn_ag_regla = st.button("➕ Agregar regla")
        
        if btn_ag_regla:
            st.session_state["contador_id"] += 1
            st.session_state["reglas_ids"].append(st.session_state["contador_id"])
            st.rerun()
            
    except Exception as e:
        st.error(f"Error estructural al leer las columnas: {str(e)}")
        st.stop()