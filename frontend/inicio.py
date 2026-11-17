<<<<<<< HEAD
# frontend/inicio.py

import streamlit as st
from backend.db_operaciones.contador_excel import conteo_total_cont

def renderizar_inicio():
    st.header("Dashboard - Bienestar Estudiantil")
    
    # Validación de bloqueo de acceso global
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.warning("Seleccione una base de datos activa en el menú lateral para acceder a este módulo.")
        return
        
    # Construcción de la ruta dinámica
    dir_db_activa = f"data/{acceso_db_funciones}"
    
    # Envío de la ruta dinámica al backend
    conteo_total = conteo_total_cont(dir_db_activa)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total de Contratos", value=conteo_total)
    
    st.divider()
    st.subheader("Estadísticas de la Base de Datos")
    grafico_est = st.empty()
    grafico_est.info("Espacio reservado para renderizado del gráfico estadístico.")
=======
# frontend/inicio.py

import streamlit as st
from backend.db_operaciones.contador_excel import conteo_total_cont

def renderizar_inicio():
    st.header("Dashboard - Bienestar Estudiantil")
    
    # Validación de bloqueo de acceso global
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.warning("Seleccione una base de datos activa en el menú lateral para acceder a este módulo.")
        return
        
    # Construcción de la ruta dinámica
    dir_db_activa = f"data/{acceso_db_funciones}"
    
    # Envío de la ruta dinámica al backend
    conteo_total = conteo_total_cont(dir_db_activa)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total de Contratos", value=conteo_total)
    
    st.divider()
    st.subheader("Estadísticas de la Base de Datos")
    grafico_est = st.empty()
    grafico_est.info("Espacio reservado para renderizado del gráfico estadístico.")
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
    return True