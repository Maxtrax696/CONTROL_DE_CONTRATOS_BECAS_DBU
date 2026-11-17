<<<<<<< HEAD
# frontend/crear_formato.py

import streamlit as st
import pandas as pd
from backend.db_operaciones.crear_archivo_xlsx import fun_crear_plantilla
import time

def renderizar_creador_archivos():
    st.header("Generador de Plantillas Dinámicas")
    
    lista_columnas_base = [
        "NUM_CONTRATO", "PERIODO", "FACULTAD", "CARRERA", 
        "COD CARRERA", "CEDULA", "NOMBRE", "CORREO", "CELULAR", "DIRECCION", 
        "SEMESTRE", "APROBADAS", "REPROBADAS", "CONVALIDADAS", "TOMADAS", 
        "APROBADOS", "REPROBADOS", "CONVALIDADOS", "TOMADOS", "* MATRICULADOS", 
        "* PERIODO", "CARRERA_1", "GENERAL", "ACADEMICO", "* < 30%", "DEFINITIVA", 
        "* >= 60%", "TEMPORAL", "GENERO", "EDAD", "ETNIA", "DISCAPACIDAD", "TIPO", 
        "BECAS UCE", "BECAS SENECYT", "BECAS MUNICIPIO", "HCU", "CORO", "FINANCIERO",
        "ENTIDAD_BANCARIA", "CODIGO_BANCO", "TIPO_CUENTA", "NUM_CUENTA", "GRUPO", 
        "REQUERIMIENTO_DBU", "APROBACION_VICERECTORADO","OBSERVACIONES"
    ]
    
    lista_hojas_pred = ["EXCELENCIA", "VULNERABILIDAD"]
    
    input_nombre_archivo = st.text_input("Nombre del nuevo archivo (ej. BECARIOS_2026):")
    
    st.divider()
    st.subheader("1. Configuración de Hojas")
    check_hojas_pred = st.checkbox("Usar hojas predeterminadas", value=True)
    
    lista_hojas_final = []
    if check_hojas_pred:
        st.info(f"Hojas predeterminadas a generar: {', '.join(lista_hojas_pred)}")
        lista_hojas_final = lista_hojas_pred.copy()
    else:
        if "status_num_hojas" not in st.session_state:
            st.session_state["status_num_hojas"] = [0]
            st.session_state["contador_hojas"] = 0
            
        dic_hojas_dinamicas = {}
        hoja_a_eliminar = None
        
        for h_id in st.session_state["status_num_hojas"]:
            col1, col2 = st.columns([5, 1])
            with col1:
                dic_hojas_dinamicas[h_id] = st.text_input(f"Nombre de la hoja {h_id+1}:", key=f"hoja_{h_id}")
            with col2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_h_{h_id}", help="Eliminar esta hoja"):
                    hoja_a_eliminar = h_id
                    
        if hoja_a_eliminar is not None:
            st.session_state["status_num_hojas"].remove(hoja_a_eliminar)
            st.rerun()
            
        btn_ag_hoja = st.button("➕ Agregar hoja")
        if btn_ag_hoja:
            st.session_state["contador_hojas"] += 1
            st.session_state["status_num_hojas"].append(st.session_state["contador_hojas"])
            st.rerun()
            
        lista_hojas_final = [v.strip() for v in dic_hojas_dinamicas.values() if v.strip()]

    st.divider()
    st.subheader("2. Configuración de Columnas")
    check_col_pred = st.checkbox("Usar columnas predeterminadas", value=True)
    
    lista_columnas_final = []
    if check_col_pred:
        st.info(f"Se crearán las {len(lista_columnas_base)} columnas oficiales del sistema.")
        lista_columnas_final = lista_columnas_base.copy()
    else:
        # Multiselector vacío por defecto con sugerencias de la base
        multiselect_sugerencias = st.multiselect(
            "Seleccione columnas sugeridas de la base (opcional):",
            options=lista_columnas_base,
            default=[]
        )
        
        st.write("Añada manualmente columnas personalizadas:")
        if "status_num_columnas" not in st.session_state:
            st.session_state["status_num_columnas"] = [0]
            st.session_state["contador_columnas"] = 0
            
        columna_a_eliminar = None
        dic_cols_dinamicas = {}
        
        for c_id in st.session_state["status_num_columnas"]:
            col1, col2 = st.columns([5, 1])
            with col1:
                dic_cols_dinamicas[c_id] = st.text_input(f"Nombre de columna {c_id+1}:", key=f"col_{c_id}")
            with col2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_c_{c_id}", help="Eliminar esta columna"):
                    columna_a_eliminar = c_id
                    
        if columna_a_eliminar is not None:
            st.session_state["status_num_columnas"].remove(columna_a_eliminar)
            st.rerun()
            
        btn_ag_columna = st.button("➕ Agregar columna")
        if btn_ag_columna:
            st.session_state["contador_columnas"] += 1
            st.session_state["status_num_columnas"].append(st.session_state["contador_columnas"])
            st.rerun()
            
        # Fusión de columnas seleccionadas del multiselect y las ingresadas dinámicamente
        dinamicas_limpias = [v.strip() for v in dic_cols_dinamicas.values() if v.strip()]
        lista_columnas_final = multiselect_sugerencias + dinamicas_limpias
        
    st.divider()
    btn_crear_archivo = st.button("Crear Plantilla", type="primary")
    
    if btn_crear_archivo:
        if not input_nombre_archivo.strip():
            st.error("El nombre del archivo es obligatorio.")
            return
        if not lista_hojas_final:
            st.error("Debe definir al menos una hoja.")
            return
        if not lista_columnas_final:
            st.error("Debe definir al menos una columna.")
            return
            
        txt_estado_proceso = "ejecución en proceso, espere"
        with st.spinner(txt_estado_proceso):
            status_creacion, mensaje = fun_crear_plantilla(input_nombre_archivo, lista_hojas_final, lista_columnas_final)
            
            if status_creacion:
                st.success(mensaje)
                ruta_salida = f"data/{input_nombre_archivo.strip()}.xlsx" if not input_nombre_archivo.endswith('.xlsx') else f"data/{input_nombre_archivo.strip()}"
                try:
                    with open(ruta_salida, "rb") as file:
                        bytes_archivo = file.read()
                        st.download_button(
                            label="📥 Descargar Plantilla",
                            data=bytes_archivo,
                            file_name=ruta_salida.split("/")[-1],
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception as e:
                    st.error(f"Error al generar botón de descarga: {str(e)}")
                
                # Pausa y limpieza de interfaz
                time.sleep(4)  # Pausa de 4 segundos antes de recargar la página
                st.rerun()
            else:
=======
<<<<<<< HEAD
# frontend/crear_formato.py

import streamlit as st
import pandas as pd
from backend.db_operaciones.crear_archivo_xlsx import fun_crear_plantilla
import time

def renderizar_creador_archivos():
    st.header("Generador de Plantillas Dinámicas")
    
    lista_columnas_base = [
        "NUM_CONTRATO", "PERIODO", "FACULTAD", "CARRERA", 
        "COD CARRERA", "CEDULA", "NOMBRE", "CORREO", "CELULAR", "DIRECCION", 
        "SEMESTRE", "APROBADAS", "REPROBADAS", "CONVALIDADAS", "TOMADAS", 
        "APROBADOS", "REPROBADOS", "CONVALIDADOS", "TOMADOS", "* MATRICULADOS", 
        "* PERIODO", "CARRERA_1", "GENERAL", "ACADEMICO", "* < 30%", "DEFINITIVA", 
        "* >= 60%", "TEMPORAL", "GENERO", "EDAD", "ETNIA", "DISCAPACIDAD", "TIPO", 
        "BECAS UCE", "BECAS SENECYT", "BECAS MUNICIPIO", "HCU", "CORO", "FINANCIERO",
        "ENTIDAD_BANCARIA", "CODIGO_BANCO", "TIPO_CUENTA", "NUM_CUENTA", "GRUPO", 
        "REQUERIMIENTO_DBU", "APROBACION_VICERECTORADO","OBSERVACIONES"
    ]
    
    lista_hojas_pred = ["EXCELENCIA", "VULNERABILIDAD"]
    
    input_nombre_archivo = st.text_input("Nombre del nuevo archivo (ej. BECARIOS_2026):")
    
    st.divider()
    st.subheader("1. Configuración de Hojas")
    check_hojas_pred = st.checkbox("Usar hojas predeterminadas", value=True)
    
    lista_hojas_final = []
    if check_hojas_pred:
        st.info(f"Hojas predeterminadas a generar: {', '.join(lista_hojas_pred)}")
        lista_hojas_final = lista_hojas_pred.copy()
    else:
        if "status_num_hojas" not in st.session_state:
            st.session_state["status_num_hojas"] = [0]
            st.session_state["contador_hojas"] = 0
            
        dic_hojas_dinamicas = {}
        hoja_a_eliminar = None
        
        for h_id in st.session_state["status_num_hojas"]:
            col1, col2 = st.columns([5, 1])
            with col1:
                dic_hojas_dinamicas[h_id] = st.text_input(f"Nombre de la hoja {h_id+1}:", key=f"hoja_{h_id}")
            with col2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_h_{h_id}", help="Eliminar esta hoja"):
                    hoja_a_eliminar = h_id
                    
        if hoja_a_eliminar is not None:
            st.session_state["status_num_hojas"].remove(hoja_a_eliminar)
            st.rerun()
            
        btn_ag_hoja = st.button("➕ Agregar hoja")
        if btn_ag_hoja:
            st.session_state["contador_hojas"] += 1
            st.session_state["status_num_hojas"].append(st.session_state["contador_hojas"])
            st.rerun()
            
        lista_hojas_final = [v.strip() for v in dic_hojas_dinamicas.values() if v.strip()]

    st.divider()
    st.subheader("2. Configuración de Columnas")
    check_col_pred = st.checkbox("Usar columnas predeterminadas", value=True)
    
    lista_columnas_final = []
    if check_col_pred:
        st.info(f"Se crearán las {len(lista_columnas_base)} columnas oficiales del sistema.")
        lista_columnas_final = lista_columnas_base.copy()
    else:
        # Multiselector vacío por defecto con sugerencias de la base
        multiselect_sugerencias = st.multiselect(
            "Seleccione columnas sugeridas de la base (opcional):",
            options=lista_columnas_base,
            default=[]
        )
        
        st.write("Añada manualmente columnas personalizadas:")
        if "status_num_columnas" not in st.session_state:
            st.session_state["status_num_columnas"] = [0]
            st.session_state["contador_columnas"] = 0
            
        columna_a_eliminar = None
        dic_cols_dinamicas = {}
        
        for c_id in st.session_state["status_num_columnas"]:
            col1, col2 = st.columns([5, 1])
            with col1:
                dic_cols_dinamicas[c_id] = st.text_input(f"Nombre de columna {c_id+1}:", key=f"col_{c_id}")
            with col2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_c_{c_id}", help="Eliminar esta columna"):
                    columna_a_eliminar = c_id
                    
        if columna_a_eliminar is not None:
            st.session_state["status_num_columnas"].remove(columna_a_eliminar)
            st.rerun()
            
        btn_ag_columna = st.button("➕ Agregar columna")
        if btn_ag_columna:
            st.session_state["contador_columnas"] += 1
            st.session_state["status_num_columnas"].append(st.session_state["contador_columnas"])
            st.rerun()
            
        # Fusión de columnas seleccionadas del multiselect y las ingresadas dinámicamente
        dinamicas_limpias = [v.strip() for v in dic_cols_dinamicas.values() if v.strip()]
        lista_columnas_final = multiselect_sugerencias + dinamicas_limpias
        
    st.divider()
    btn_crear_archivo = st.button("Crear Plantilla", type="primary")
    
    if btn_crear_archivo:
        if not input_nombre_archivo.strip():
            st.error("El nombre del archivo es obligatorio.")
            return
        if not lista_hojas_final:
            st.error("Debe definir al menos una hoja.")
            return
        if not lista_columnas_final:
            st.error("Debe definir al menos una columna.")
            return
            
        txt_estado_proceso = "ejecución en proceso, espere"
        with st.spinner(txt_estado_proceso):
            status_creacion, mensaje = fun_crear_plantilla(input_nombre_archivo, lista_hojas_final, lista_columnas_final)
            
            if status_creacion:
                st.success(mensaje)
                ruta_salida = f"data/{input_nombre_archivo.strip()}.xlsx" if not input_nombre_archivo.endswith('.xlsx') else f"data/{input_nombre_archivo.strip()}"
                try:
                    with open(ruta_salida, "rb") as file:
                        bytes_archivo = file.read()
                        st.download_button(
                            label="📥 Descargar Plantilla",
                            data=bytes_archivo,
                            file_name=ruta_salida.split("/")[-1],
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception as e:
                    st.error(f"Error al generar botón de descarga: {str(e)}")
                
                # Pausa y limpieza de interfaz
                time.sleep(4)  # Pausa de 4 segundos antes de recargar la página
                st.rerun()
            else:
=======
# frontend/crear_formato.py

import streamlit as st
import pandas as pd
from backend.db_operaciones.crear_archivo_xlsx import fun_crear_plantilla
import time

def renderizar_creador_archivos():
    st.header("Generador de Plantillas Dinámicas")
    
    lista_columnas_base = [
        "NUM_CONTRATO", "PERIODO", "FACULTAD", "CARRERA", 
        "COD CARRERA", "CEDULA", "NOMBRE", "CORREO", "CELULAR", "DIRECCION", 
        "SEMESTRE", "APROBADAS", "REPROBADAS", "CONVALIDADAS", "TOMADAS", 
        "APROBADOS", "REPROBADOS", "CONVALIDADOS", "TOMADOS", "* MATRICULADOS", 
        "* PERIODO", "CARRERA_1", "GENERAL", "ACADEMICO", "* < 30%", "DEFINITIVA", 
        "* >= 60%", "TEMPORAL", "GENERO", "EDAD", "ETNIA", "DISCAPACIDAD", "TIPO", 
        "BECAS UCE", "BECAS SENECYT", "BECAS MUNICIPIO", "HCU", "CORO", "FINANCIERO",
        "ENTIDAD_BANCARIA", "CODIGO_BANCO", "TIPO_CUENTA", "NUM_CUENTA", "GRUPO", 
        "REQUERIMIENTO_DBU", "APROBACION_VICERECTORADO","OBSERVACIONES"
    ]
    
    lista_hojas_pred = ["EXCELENCIA", "VULNERABILIDAD"]
    
    input_nombre_archivo = st.text_input("Nombre del nuevo archivo (ej. BECARIOS_2026):")
    
    st.divider()
    st.subheader("1. Configuración de Hojas")
    check_hojas_pred = st.checkbox("Usar hojas predeterminadas", value=True)
    
    lista_hojas_final = []
    if check_hojas_pred:
        st.info(f"Hojas predeterminadas a generar: {', '.join(lista_hojas_pred)}")
        lista_hojas_final = lista_hojas_pred.copy()
    else:
        if "status_num_hojas" not in st.session_state:
            st.session_state["status_num_hojas"] = [0]
            st.session_state["contador_hojas"] = 0
            
        dic_hojas_dinamicas = {}
        hoja_a_eliminar = None
        
        for h_id in st.session_state["status_num_hojas"]:
            col1, col2 = st.columns([5, 1])
            with col1:
                dic_hojas_dinamicas[h_id] = st.text_input(f"Nombre de la hoja {h_id+1}:", key=f"hoja_{h_id}")
            with col2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_h_{h_id}", help="Eliminar esta hoja"):
                    hoja_a_eliminar = h_id
                    
        if hoja_a_eliminar is not None:
            st.session_state["status_num_hojas"].remove(hoja_a_eliminar)
            st.rerun()
            
        btn_ag_hoja = st.button("➕ Agregar hoja")
        if btn_ag_hoja:
            st.session_state["contador_hojas"] += 1
            st.session_state["status_num_hojas"].append(st.session_state["contador_hojas"])
            st.rerun()
            
        lista_hojas_final = [v.strip() for v in dic_hojas_dinamicas.values() if v.strip()]

    st.divider()
    st.subheader("2. Configuración de Columnas")
    check_col_pred = st.checkbox("Usar columnas predeterminadas", value=True)
    
    lista_columnas_final = []
    if check_col_pred:
        st.info(f"Se crearán las {len(lista_columnas_base)} columnas oficiales del sistema.")
        lista_columnas_final = lista_columnas_base.copy()
    else:
        # Multiselector vacío por defecto con sugerencias de la base
        multiselect_sugerencias = st.multiselect(
            "Seleccione columnas sugeridas de la base (opcional):",
            options=lista_columnas_base,
            default=[]
        )
        
        st.write("Añada manualmente columnas personalizadas:")
        if "status_num_columnas" not in st.session_state:
            st.session_state["status_num_columnas"] = [0]
            st.session_state["contador_columnas"] = 0
            
        columna_a_eliminar = None
        dic_cols_dinamicas = {}
        
        for c_id in st.session_state["status_num_columnas"]:
            col1, col2 = st.columns([5, 1])
            with col1:
                dic_cols_dinamicas[c_id] = st.text_input(f"Nombre de columna {c_id+1}:", key=f"col_{c_id}")
            with col2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"del_c_{c_id}", help="Eliminar esta columna"):
                    columna_a_eliminar = c_id
                    
        if columna_a_eliminar is not None:
            st.session_state["status_num_columnas"].remove(columna_a_eliminar)
            st.rerun()
            
        btn_ag_columna = st.button("➕ Agregar columna")
        if btn_ag_columna:
            st.session_state["contador_columnas"] += 1
            st.session_state["status_num_columnas"].append(st.session_state["contador_columnas"])
            st.rerun()
            
        # Fusión de columnas seleccionadas del multiselect y las ingresadas dinámicamente
        dinamicas_limpias = [v.strip() for v in dic_cols_dinamicas.values() if v.strip()]
        lista_columnas_final = multiselect_sugerencias + dinamicas_limpias
        
    st.divider()
    btn_crear_archivo = st.button("Crear Plantilla", type="primary")
    
    if btn_crear_archivo:
        if not input_nombre_archivo.strip():
            st.error("El nombre del archivo es obligatorio.")
            return
        if not lista_hojas_final:
            st.error("Debe definir al menos una hoja.")
            return
        if not lista_columnas_final:
            st.error("Debe definir al menos una columna.")
            return
            
        txt_estado_proceso = "ejecución en proceso, espere"
        with st.spinner(txt_estado_proceso):
            status_creacion, mensaje = fun_crear_plantilla(input_nombre_archivo, lista_hojas_final, lista_columnas_final)
            
            if status_creacion:
                st.success(mensaje)
                ruta_salida = f"data/{input_nombre_archivo.strip()}.xlsx" if not input_nombre_archivo.endswith('.xlsx') else f"data/{input_nombre_archivo.strip()}"
                try:
                    with open(ruta_salida, "rb") as file:
                        bytes_archivo = file.read()
                        st.download_button(
                            label="📥 Descargar Plantilla",
                            data=bytes_archivo,
                            file_name=ruta_salida.split("/")[-1],
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception as e:
                    st.error(f"Error al generar botón de descarga: {str(e)}")
                
                # Pausa y limpieza de interfaz
                time.sleep(4)  # Pausa de 4 segundos antes de recargar la página
                st.rerun()
            else:
>>>>>>> 0b7154d72bff2a5861fc17effcf996fc49c975ed
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
                st.error(mensaje)