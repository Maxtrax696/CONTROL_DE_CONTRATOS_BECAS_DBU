<<<<<<< HEAD
# main.py

import streamlit as st

# Importación de los módulos del frontend
from frontend import inicio
from frontend import ver_datos
from frontend import archivo_ext
from frontend import crear_formato
from frontend.formularios import agregar, editar, eliminar
from backend.db_operaciones.escaner_bases import fun_lista_bases

def iniciar_sistema():
    head_navegador = "Sistema de Gestión Bienestar Estudiantil"
    st.set_page_config(page_title=head_navegador, layout="wide")
    
    # Sección de Configuración Global en la barra lateral
    st.sidebar.title("Configuración Global")
    lista_bases_disponibles = fun_lista_bases()
    
    # Despliegue del selector global de base activa
    if lista_bases_disponibles:
        selector_base_sug = st.sidebar.selectbox("Seleccione la Base de Datos Activa:", options=lista_bases_disponibles)
        st.session_state["base_activa"] = selector_base_sug
    else:
        st.sidebar.warning("No hay bases de datos detectadas en /data/")
        st.session_state["base_activa"] = None
        
    st.sidebar.divider()
    
    main_control = st.sidebar.radio(
        "Navegación del Sistema",
        [
            "Inicio", 
            "Visualizar Datos", 
            "Agregar Nuevo", 
            "Editar Existente", 
            "Eliminar Registro", 
            "Sincronizar Externo", 
            "Generar Formato"
        ]
    )
    
    # Lógica de enrutamiento
    if main_control == "Inicio":
        inicio.renderizar_inicio()
    elif main_control == "Visualizar Datos":
        ver_datos.renderizar_tabla()
    elif main_control == "Agregar Nuevo":
        agregar.renderizar_formulario_ag()
    elif main_control == "Editar Existente":
        editar.renderizar_formulario_ed()
    elif main_control == "Eliminar Registro":
        eliminar.renderizar_formulario_el()
    elif main_control == "Sincronizar Externo":
        archivo_ext.renderizar_modulo_sincronizacion()
    elif main_control == "Generar Formato":
        crear_formato.renderizar_creador_archivos()

if __name__ == "__main__":
=======
<<<<<<< HEAD
# main.py

import streamlit as st

# Importación de los módulos del frontend
from frontend import inicio
from frontend import ver_datos
from frontend import archivo_ext
from frontend import crear_formato
from frontend.formularios import agregar, editar, eliminar
from backend.db_operaciones.escaner_bases import fun_lista_bases

def iniciar_sistema():
    head_navegador = "Sistema de Gestión Bienestar Estudiantil"
    st.set_page_config(page_title=head_navegador, layout="wide")
    
    # Sección de Configuración Global en la barra lateral
    st.sidebar.title("Configuración Global")
    lista_bases_disponibles = fun_lista_bases()
    
    # Despliegue del selector global de base activa
    if lista_bases_disponibles:
        selector_base_sug = st.sidebar.selectbox("Seleccione la Base de Datos Activa:", options=lista_bases_disponibles)
        st.session_state["base_activa"] = selector_base_sug
    else:
        st.sidebar.warning("No hay bases de datos detectadas en /data/")
        st.session_state["base_activa"] = None
        
    st.sidebar.divider()
    
    main_control = st.sidebar.radio(
        "Navegación del Sistema",
        [
            "Inicio", 
            "Visualizar Datos", 
            "Agregar Nuevo", 
            "Editar Existente", 
            "Eliminar Registro", 
            "Sincronizar Externo", 
            "Generar Formato"
        ]
    )
    
    # Lógica de enrutamiento
    if main_control == "Inicio":
        inicio.renderizar_inicio()
    elif main_control == "Visualizar Datos":
        ver_datos.renderizar_tabla()
    elif main_control == "Agregar Nuevo":
        agregar.renderizar_formulario_ag()
    elif main_control == "Editar Existente":
        editar.renderizar_formulario_ed()
    elif main_control == "Eliminar Registro":
        eliminar.renderizar_formulario_el()
    elif main_control == "Sincronizar Externo":
        archivo_ext.renderizar_modulo_sincronizacion()
    elif main_control == "Generar Formato":
        crear_formato.renderizar_creador_archivos()

if __name__ == "__main__":
=======
# main.py

import streamlit as st

# Importación de los módulos del frontend
from frontend import inicio
from frontend import ver_datos
from frontend import archivo_ext
from frontend import crear_formato
from frontend.formularios import agregar, editar, eliminar
from backend.db_operaciones.escaner_bases import fun_lista_bases

def iniciar_sistema():
    head_navegador = "Sistema de Gestión Bienestar Estudiantil"
    st.set_page_config(page_title=head_navegador, layout="wide")
    
    # Sección de Configuración Global en la barra lateral
    st.sidebar.title("Configuración Global")
    lista_bases_disponibles = fun_lista_bases()
    
    # Despliegue del selector global de base activa
    if lista_bases_disponibles:
        selector_base_sug = st.sidebar.selectbox("Seleccione la Base de Datos Activa:", options=lista_bases_disponibles)
        st.session_state["base_activa"] = selector_base_sug
    else:
        st.sidebar.warning("No hay bases de datos detectadas en /data/")
        st.session_state["base_activa"] = None
        
    st.sidebar.divider()
    
    main_control = st.sidebar.radio(
        "Navegación del Sistema",
        [
            "Inicio", 
            "Visualizar Datos", 
            "Agregar Nuevo", 
            "Editar Existente", 
            "Eliminar Registro", 
            "Sincronizar Externo", 
            "Generar Formato"
        ]
    )
    
    # Lógica de enrutamiento
    if main_control == "Inicio":
        inicio.renderizar_inicio()
    elif main_control == "Visualizar Datos":
        ver_datos.renderizar_tabla()
    elif main_control == "Agregar Nuevo":
        agregar.renderizar_formulario_ag()
    elif main_control == "Editar Existente":
        editar.renderizar_formulario_ed()
    elif main_control == "Eliminar Registro":
        eliminar.renderizar_formulario_el()
    elif main_control == "Sincronizar Externo":
        archivo_ext.renderizar_modulo_sincronizacion()
    elif main_control == "Generar Formato":
        crear_formato.renderizar_creador_archivos()

if __name__ == "__main__":
>>>>>>> 0b7154d72bff2a5861fc17effcf996fc49c975ed
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
    iniciar_sistema()