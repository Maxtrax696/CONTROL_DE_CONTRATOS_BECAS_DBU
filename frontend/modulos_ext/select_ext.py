<<<<<<< HEAD
# data/modulos_ext/select_ext.py

# Importación del framework gráfico y manipulación de datos
import streamlit as st
import pandas as pd

def renderizar_seleccion_hoja():
    # Recuperación del archivo físico desde el estado global
    archivo_fisico = st.session_state["file_key"]
    
    # Validación estructural: Si es CSV, se omite este paso y se asigna una hoja virtual
    if archivo_fisico.name.endswith('.csv'):
        st.session_state["storage_key"] = "CSV_Unico"
        st.rerun()
        return
        
    st.subheader("Paso 2: Selección de Hoja")
    
    try:
        # Variable para el objeto lector de metadata del archivo Excel
        lector_datos_externos = pd.ExcelFile(archivo_fisico)
        
        # Variable para el componente gráfico que expone las hojas disponibles
        box_select_hoja = st.selectbox("Seleccione la hoja a procesar:", options=lector_datos_externos.sheet_names)
        
        # Variable para el botón que confirmará la hoja y actualizará el estado
        btn_hoja_confirmada = st.button("Confirmar Hoja")
        
        if btn_hoja_confirmada:
            # Almacenamiento de la hoja y limpieza forzada de mapeos previos
            st.session_state["storage_key"] = box_select_hoja
            st.session_state["columnas_key"] = {}
            st.success(f"Hoja '{box_select_hoja}' confirmada para el cruce.")
            st.rerun()
            
    except Exception as e:
        # Detención completa de la ejecución en caso de archivo corrupto
        st.error(f"Error estructural al leer el archivo: {str(e)}")
=======
# data/modulos_ext/select_ext.py

# Importación del framework gráfico y manipulación de datos
import streamlit as st
import pandas as pd

def renderizar_seleccion_hoja():
    # Recuperación del archivo físico desde el estado global
    archivo_fisico = st.session_state["file_key"]
    
    # Validación estructural: Si es CSV, se omite este paso y se asigna una hoja virtual
    if archivo_fisico.name.endswith('.csv'):
        st.session_state["storage_key"] = "CSV_Unico"
        st.rerun()
        return
        
    st.subheader("Paso 2: Selección de Hoja")
    
    try:
        # Variable para el objeto lector de metadata del archivo Excel
        lector_datos_externos = pd.ExcelFile(archivo_fisico)
        
        # Variable para el componente gráfico que expone las hojas disponibles
        box_select_hoja = st.selectbox("Seleccione la hoja a procesar:", options=lector_datos_externos.sheet_names)
        
        # Variable para el botón que confirmará la hoja y actualizará el estado
        btn_hoja_confirmada = st.button("Confirmar Hoja")
        
        if btn_hoja_confirmada:
            # Almacenamiento de la hoja y limpieza forzada de mapeos previos
            st.session_state["storage_key"] = box_select_hoja
            st.session_state["columnas_key"] = {}
            st.success(f"Hoja '{box_select_hoja}' confirmada para el cruce.")
            st.rerun()
            
    except Exception as e:
        # Detención completa de la ejecución en caso de archivo corrupto
        st.error(f"Error estructural al leer el archivo: {str(e)}")
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
        st.stop()