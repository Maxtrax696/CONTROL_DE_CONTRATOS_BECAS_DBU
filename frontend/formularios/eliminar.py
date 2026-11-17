# frontend/formularios/eliminar.py

import streamlit as st
from backend.db_operaciones.lector_excel import leer_base_datos, obtener_hojas
from backend.db_operaciones.escritura_excel import fn_eliminar_registro
import time

@st.dialog("Confirmación de Eliminación")
def confirmacion_emg(dir_db_activa, select_hoja, select_contrato_eliminar):
    st.warning(f"¿Está completamente seguro de que desea eliminar el registro **{select_contrato_eliminar}**?")
    st.write("Esta acción modificará la base de datos de manera irreversible.")
    boton_confirmar_del = st.button("Sí, Eliminar Registro", type="primary")
    
    if boton_confirmar_del:
        txt_estado_proceso = "ejecución en proceso, espere"
        
        with st.spinner(txt_estado_proceso):
            conf_operacion = fn_eliminar_registro(dir_db_activa, select_hoja, select_contrato_eliminar)
            
            if conf_operacion:
                st.success("Registro eliminado de la base de datos.")
                time.sleep(3)  # Pausa de 3 segundos antes de recargar la página
                st.rerun()
            else:
                st.error("Error al intentar eliminar el registro.")

def renderizar_formulario_el():
    st.header("Eliminar Registro")
    
    # Validación de acceso
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.warning("Seleccione una base de datos activa en el menú lateral.")
        return
    dir_db_activa = f"data/{acceso_db_funciones}"
    
    nombre_hojas = obtener_hojas(dir_db_activa)
    if not nombre_hojas:
        st.error("Archivo base no encontrado.")
        return
        
    select_hoja = st.selectbox("Seleccione la hoja:", options=nombre_hojas, key="hoja_eliminar")
    # Inyección de ruta en lectura
    frame_principal = leer_base_datos(dir_db_activa, select_hoja)
    
    if frame_principal.empty:
        st.warning("La base de datos está vacía.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        filtro_col_eliminar = st.selectbox("Filtrar por columna:", options=frame_principal.columns.tolist(), key="filtro_eliminar")
    with col2:
        input_busqueda_eliminar = st.text_input("Parámetro de búsqueda:", key="busqueda_eliminar")
        
    frame_fliter = frame_principal.copy()
    if input_busqueda_eliminar:
        frame_fliter = frame_fliter[frame_fliter[filtro_col_eliminar].astype(str).str.contains(input_busqueda_eliminar, case=False, na=False)]
        
    st.dataframe(frame_fliter, use_container_width=True)
    
    lista_contratos = frame_fliter['NUM_CONTRATO'].dropna().astype(str).tolist()
    select_contrato_eliminar = st.selectbox("NUM_CONTRATO a eliminar:", options=[""] + lista_contratos, key="select_eliminar")
    
    if select_contrato_eliminar:
        if st.button("Eliminar Registro"):
            confirmacion_emg(dir_db_activa, select_hoja, select_contrato_eliminar)