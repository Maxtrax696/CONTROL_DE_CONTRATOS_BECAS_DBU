<<<<<<< HEAD
# frontend/archivo_ext.py

# Importación de librerías y submódulos de vista de manera explícita
import streamlit as st
from data.modulos_ext.upd_archivo import renderizar_carga

def renderizar_modulo_sincronizacion():
    # Título central de la vista
    st.header("Sincronización de Archivos Externos")
    
    # Inicialización obligatoria de las variables globales en el estado de sesión
    if "file_key" not in st.session_state:
        st.session_state["file_key"] = None
    if "storage_key" not in st.session_state:
        st.session_state["storage_key"] = None
    if "columnas_key" not in st.session_state:
        st.session_state["columnas_key"] = {}
        
    # Ejecución directa de la función del submódulo de carga
    renderizar_carga()
    
    # Desbloqueo secuencial del flujo
    if st.session_state["file_key"] is not None:
        st.info("Archivo validado. Siguiente paso: Selección de hoja (En construcción...).")
=======
# frontend/archivo_ext.py

# Importación de librerías y submódulos de vista de manera explícita
import streamlit as st
from data.modulos_ext.upd_archivo import renderizar_carga

def renderizar_modulo_sincronizacion():
    # Título central de la vista
    st.header("Sincronización de Archivos Externos")
    
    # Inicialización obligatoria de las variables globales en el estado de sesión
    if "file_key" not in st.session_state:
        st.session_state["file_key"] = None
    if "storage_key" not in st.session_state:
        st.session_state["storage_key"] = None
    if "columnas_key" not in st.session_state:
        st.session_state["columnas_key"] = {}
        
    # Ejecución directa de la función del submódulo de carga
    renderizar_carga()
    
    # Desbloqueo secuencial del flujo
    if st.session_state["file_key"] is not None:
        st.info("Archivo validado. Siguiente paso: Selección de hoja (En construcción...).")
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
        # TODO: Invocar select_ext.py aquí