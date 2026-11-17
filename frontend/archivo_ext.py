<<<<<<< HEAD
# frontend/archivo_ext.py

import streamlit as st
from data.duplicados.verificar_duplicados_ext import renderizar_verificacion
from data.modulos_ext.cruce_datos_ext import renderizar_cruce

def renderizar_modulo_sincronizacion():
    st.header("Gestión de Archivos Externos")
    
    with st.sidebar:
        st.divider()
        selector_modulo_ext = st.radio(
            "Seleccione una operación externa:",
            options=["Verificar duplicados", "Agregar datos externos"]
        )
        
    if selector_modulo_ext == "Verificar duplicados":
        renderizar_verificacion()
    elif selector_modulo_ext == "Agregar datos externos":
=======
# frontend/archivo_ext.py

import streamlit as st
from data.duplicados.verificar_duplicados_ext import renderizar_verificacion
from data.modulos_ext.cruce_datos_ext import renderizar_cruce

def renderizar_modulo_sincronizacion():
    st.header("Gestión de Archivos Externos")
    
    with st.sidebar:
        st.divider()
        selector_modulo_ext = st.radio(
            "Seleccione una operación externa:",
            options=["Verificar duplicados", "Agregar datos externos"]
        )
        
    if selector_modulo_ext == "Verificar duplicados":
        renderizar_verificacion()
    elif selector_modulo_ext == "Agregar datos externos":
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
        renderizar_cruce()