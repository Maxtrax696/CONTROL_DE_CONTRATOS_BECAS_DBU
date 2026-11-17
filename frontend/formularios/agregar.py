# frontend/formularios/agregar.py

import streamlit as st
from backend.db_operaciones.lector_excel import obtener_hojas
from backend.db_operaciones.escritura_excel import fn_guardar_nuevo_registro
from backend.validaciones.validacion_ci import validar_cedula
from backend.validaciones.autoasignar_cont import obtener_nuevo_contrato
from backend.db_operaciones.datos_academicos import dic_facultad, dic_carrera, dic_bancos
import time

@st.dialog("Confirmación de Guardado")
def confirmacion_emg_agregar(dir_db_activa, dic_temp, select_hoja, ingreso_ci, periodo_extraido):
    st.warning("¿Está seguro de que desea guardar este nuevo registro en la base de datos?")
    boton_confirmacion_ag = st.button("Sí, Guardar Registro", type="primary")
    
    if boton_confirmacion_ag:
        txt_estado_proceso = "ejecución en proceso, espere"
        with st.spinner(txt_estado_proceso):
            validez_ci = validar_cedula(ingreso_ci)
            if not validez_ci:
                st.error("Error: Cédula inválida. Cierre esta ventana y corrija el dato.")
            else:
                # Envío del periodo extraído al algoritmo de asignación
                asignacion_contrato = obtener_nuevo_contrato(dir_db_activa, select_hoja, periodo_extraido)
                dic_temp["NUM_CONTRATO"] = asignacion_contrato
                
                status_ag, detalle_error = fn_guardar_nuevo_registro(dir_db_activa, select_hoja, dic_temp)
                if status_ag:
                    st.success(f"Registro agregado correctamente. Contrato asignado: {asignacion_contrato}")
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(f"Error técnico: {detalle_error}")

def renderizar_formulario_ag():
    st.header("Agregar Nuevo Registro")
    
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.warning("Seleccione una base de datos activa en el menú lateral.")
        return
    dir_db_activa = f"data/{acceso_db_funciones}"
    
    nombre_hojas = obtener_hojas(dir_db_activa)
    if not nombre_hojas:
        st.error("Error: No se encontró el archivo base para insertar datos.")
        return
        
    select_hoja = st.selectbox("Seleccione la hoja de destino:", options=nombre_hojas)
    
    lista_opciones_genero = ["","MUJER", "HOMBRE"]
    lista_opciones_etnia = ["","MESTIZO", "OTRO", "INDIGENA", "MULATO", "BLANCO"]
    lista_opciones_discapacidad = ["", "NO", "SI"]
    lista_opciones_tipo = ["", "NINGUNA", "VISUAL", "FISICA", "AUDITIVA", "INTELECTUAL"]
    lista_opciones_semestre = [str(i) for i in range(1, 12)]
    
    cont_grafico = st.container()
    
    with cont_grafico:
        dic_temp = {}
        
        # Declaración global de la lista de meses para los selectores
        lista_meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

        # Contenedor 1: Sección Principal
        cont_periodo = st.expander("Sección Principal", expanded=True)
        with cont_periodo:
            st.info("El NUM_CONTRATO será generado basándose en los años del periodo ingresado.")
            col_m1, col_a1, col_m2, col_a2 = st.columns(4)
            with col_m1:
                mes_inicio = st.selectbox("Mes Inicio:", options=lista_meses, index=9)
            with col_a1:
                anio_inicio = st.text_input("Año Inicio:", value="2024")
            with col_m2:
                mes_fin = st.selectbox("Mes Fin:", options=lista_meses, index=1)
            with col_a2:
                anio_fin = st.text_input("Año Fin:", value="2025")
                
            # Concatenación para la columna PERIODO en la base de datos
            dic_temp["PERIODO"] = f"{mes_inicio} {anio_inicio} - {mes_fin} {anio_fin}"
            # Variable estricta con los años para generar el NUM_CONTRATO
            periodo_extraido = f"{anio_inicio}-{anio_fin}"
            
        # Contenedor 2: Datos Personales
        cont_datos_per = st.expander("Datos Personales", expanded=False)
        with cont_datos_per:
            ingreso_ci = st.text_input("Ingrese CEDULA (10 dígitos numéricos):")
            dic_temp["CEDULA"] = ingreso_ci
            dic_temp["NOMBRE"] = st.text_input("Ingrese NOMBRE:")
            dic_temp["CORREO"] = st.text_input("Ingrese CORREO:")
            dic_temp["CELULAR"] = st.text_input("Ingrese CELULAR:")
            dic_temp["DIRECCION"] = st.text_input("Ingrese DIRECCION:")
            dic_temp["EDAD"] = st.text_input("Ingrese EDAD:")
            
            dic_temp["GENERO"] = st.selectbox("Seleccione GENERO:", options=lista_opciones_genero)
            dic_temp["ETNIA"] = st.selectbox("Seleccione ETNIA:", options=lista_opciones_etnia)
            
            dic_temp["DISCAPACIDAD"] = st.selectbox("Seleccione DISCAPACIDAD:", options=lista_opciones_discapacidad)
            
            # Lógica reactiva: Bloqueo del selector de tipo si es "NO" o está vacío
            if dic_temp["DISCAPACIDAD"] in ["NO", ""]:
                dic_temp["TIPO"] = st.selectbox("Seleccione TIPO DE DISCAPACIDAD:", options=[""], disabled=True, key="tipo_ag_inactivo")
            else:
                dic_temp["TIPO"] = st.selectbox("Seleccione TIPO DE DISCAPACIDAD:", options=lista_opciones_tipo, key="tipo_ag_activo")

        # Contenedor 3: Información Académica
        cont_info_academica = st.expander("Información Académica", expanded=False)
        with cont_info_academica:
            opc_facultad = st.selectbox("Seleccione FACULTAD:", options=list(dic_facultad.keys()))
            dic_temp["FACULTAD"] = opc_facultad
            
            carreras_disponibles = dic_facultad.get(opc_facultad, [])
            opc_carrera = st.selectbox("Seleccione CARRERA:", options=carreras_disponibles)
            dic_temp["CARRERA"] = opc_carrera
            
            codigo_auto = dic_carrera.get(opc_carrera, "")
            dic_temp["COD CARRERA"] = codigo_auto
            st.text_input("COD CARRERA (Autoasignado):", value=codigo_auto, disabled=True)
            
            dic_temp["SEMESTRE"] = st.selectbox("Seleccione SEMESTRE:", options=lista_opciones_semestre)
            
            columnas_acad = [
                "APROBADAS", "REPROBADAS", "CONVALIDADAS", "TOMADAS", "APROBADOS", "REPROBADOS", 
                "CONVALIDADOS", "TOMADOS", "* MATRICULADOS", "* PERIODO", "CARRERA_1", 
                "GENERAL", "ACADEMICO", "* < 30%", "DEFINITIVA", "* >= 60%", "TEMPORAL"
            ]
            for col in columnas_acad:
                dic_temp[col] = st.text_input(f"Ingrese {col}:")

        # Contenedor 4: Becas
        cont_becas_ot = st.expander("Becas y Ayudas", expanded=False)
        with cont_becas_ot:
            columnas_becas = ["BECAS UCE", "BECAS SENECYT", "BECAS MUNICIPIO", "HCU", "CORO", "FINANCIERO", "No BECARIO"]
            for col in columnas_becas:
                dic_temp[col] = st.text_input(f"Ingrese {col}:")

        # Contenedor 5: Datos Bancarios
        cont_datos_bancarios = st.expander("Datos Bancarios", expanded=False)
        with cont_datos_bancarios:
            opc_entidad = st.selectbox("Seleccione ENTIDAD BANCARIA:", options=[""] + list(dic_bancos.keys()))
            dic_temp["ENTIDAD_BANCARIA"] = opc_entidad
            
            cod_entidad_bancaria_auto = dic_bancos.get(opc_entidad, "")
            dic_temp["CODIGO_BANCO"] = cod_entidad_bancaria_auto
            st.text_input("CODIGO BANCO (Autoasignado):", value=cod_entidad_bancaria_auto, disabled=True)
            
            lista_opc_tipo_cuenta = ["AHORROS", "CORRIENTE"]
            
            if not opc_entidad:
                dic_temp["TIPO_CUENTA"] = st.selectbox("Seleccione TIPO_CUENTA:", options=[""], disabled=True, key="tipo_cuenta_ag_inactivo")
            else:
                dic_temp["TIPO_CUENTA"] = st.selectbox("Seleccione TIPO_CUENTA:", options=lista_opc_tipo_cuenta, key="tipo_cuenta_ag_activo")
                
            dic_temp["NUM_CUENTA"] = st.text_input("Ingrese NUM_CUENTA:")

        # Contenedor 6: Requerimientos Institucionales
        cont_requerimientos = st.expander("Requerimientos y Grupos", expanded=False)
        with cont_requerimientos:
            dic_temp["GRUPO"] = st.text_input("Ingrese GRUPO (Solo números):")
            dic_temp["REQUERIMIENTO_DBU"] = st.text_input("Ingrese REQUERIMIENTO_DBU:")
            dic_temp["APROBACION_VICERECTORADO"] = st.text_input("Ingrese APROBACION_VICERECTORADO:")

        # Contenedor 7: Observaciones
        cont_observaciones = st.expander("Observaciones", expanded=False)
        with cont_observaciones:
            # Variable de tipo text_area para capturar comentarios multilinea sin forzar mayúsculas
            input_observaciones = st.text_area("Ingrese OBSERVACIONES:")
            # Asignación del texto capturado al diccionario principal de guardado
            dic_temp["OBSERVACIONES"] = input_observaciones

        # botón de guardado al final del formulario
        if st.button("Guardar Registro"):
            confirmacion_emg_agregar(dir_db_activa, dic_temp, select_hoja, ingreso_ci, periodo_extraido)