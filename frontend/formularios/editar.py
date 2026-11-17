# frontend/formularios/editar.py

import streamlit as st
import pandas as pd
from backend.db_operaciones.lector_excel import leer_base_datos, obtener_hojas
from backend.db_operaciones.escritura_excel import fn_modificar_registro
from backend.db_operaciones.datos_academicos import dic_facultad, dic_carrera, dic_bancos
from backend.validaciones.autoasignar_cont import autoasignacion_contratos_vacios, autoasignacion_codigos_diccionarios
import time

@st.dialog("Confirmación de Edición")
def confirmacion_emg_editar(dir_db_activa, select_hoja, select_contrato_editar, dic_contrato_editar):
    st.warning(f"¿Está seguro de que desea sobreescribir los datos del registro **{select_contrato_editar}**?")
    
    boton_emg_edit = st.button("Sí, Actualizar Registro", type="primary")
    
    if boton_emg_edit:
        txt_estado_proceso = "ejecución en proceso, espere"
        
        with st.spinner(txt_estado_proceso):
            status_edit, detalle_error = fn_modificar_registro(dir_db_activa, select_hoja, select_contrato_editar, dic_contrato_editar)
            
            if status_edit:
                st.success("Registro modificado correctamente.")
                # Restablecimiento obligatorio del bloqueo de seguridad
                st.session_state["status_desbloqueo_contrato"] = False
                time.sleep(4)
                st.rerun()
            else:
                st.error(f"Error al intentar modificar el registro. Detalle técnico: {detalle_error}")

# Declaración global de la ventana emergente de autoasignación de contratos
@st.dialog("Autoasignación Masiva de Contratos")
def emg_autoasignar_vacios(dir_db_activa, select_hoja):
    st.warning(f"Se escanearán todos los estudiantes sin número de contrato en la hoja **{select_hoja}** y se les asignará automáticamente una secuencia válida (llenando espacios disponibles o creando nuevas continuaciones).")
    
    btn_iniciar_asignacion = st.button("Sí, Iniciar Asignación", type="primary")
    
    if btn_iniciar_asignacion:
        txt_estado_proceso = "ejecución en proceso, espere"
        with st.spinner(txt_estado_proceso):
            status, msg = autoasignacion_contratos_vacios(dir_db_activa, select_hoja)
            if status:
                st.success(msg)
                time.sleep(4)
                st.rerun()
            else:
                st.error(msg)

# Declaración global de la ventana emergente de asignación de códigos (Carrera y Banco)
@st.dialog("Autoasignación Masiva de Códigos")
def emg_asignar_codigos_dic(dir_db_activa, select_hoja):
    st.info(f"Se escanearán los registros de la hoja **{select_hoja}**. Se asignará el 'COD CARRERA' y 'CODIGO_BANCO' a los espacios vacíos basándose en la información de Carrera y Entidad Bancaria.")
    
    btn_ejecutar_asignacion_codigos = st.button("Sí, Asignar Códigos", type="primary")
    
    if btn_ejecutar_asignacion_codigos:
        txt_estado_proceso = "ejecución en proceso, espere"
        with st.spinner(txt_estado_proceso):
            status, msg = autoasignacion_codigos_diccionarios(dir_db_activa, select_hoja)
            if status:
                st.success(msg)
                time.sleep(4)
                st.rerun()
            else:
                st.error(msg)

def renderizar_formulario_ed():
    st.header("Editar Registro Existente")
    
    acceso_db_funciones = st.session_state.get("base_activa")
    if not acceso_db_funciones:
        st.warning("Seleccione una base de datos activa en el menú lateral.")
        return
    dir_db_activa = f"data/{acceso_db_funciones}"
    
    nombre_hojas = obtener_hojas(dir_db_activa)
    if not nombre_hojas:
        st.error("Archivo base no encontrado.")
        return
        
    select_hoja = st.selectbox("Seleccione la hoja:", options=nombre_hojas)
    frame_principal = leer_base_datos(dir_db_activa, select_hoja)
    
    if frame_principal.empty:
        st.warning("La base de datos está vacía.")
        return

    # Distribución en columnas para alinear los botones a la esquina superior derecha
    col_tit_busq, col_btn_asignar = st.columns([7, 3])
    
    with col_btn_asignar:
        st.write("") # Espaciador ligero
        
        # Botón 1: Asignación de Contratos
        btn_asignacion_vacios = st.button("🚀 Autoasignar Vacíos", use_container_width=True)
        if btn_asignacion_vacios:
            emg_autoasignar_vacios(dir_db_activa, select_hoja)
            
        # Botón 2: Asignación de Códigos (Carrera y Banco) posicionado directamente debajo
        btn_asignar_codigos = st.button("🔄 Autoasignar Códigos", use_container_width=True)
        if btn_asignar_codigos:
            emg_asignar_codigos_dic(dir_db_activa, select_hoja)
            
    with col_tit_busq:
        st.write("Utilice los filtros para localizar un registro específico.")

    col1, col2 = st.columns([1, 2])
    with col1:
        filtro_col_editar = st.selectbox("Filtrar por columna para buscar:", options=frame_principal.columns.tolist())
    with col2:
        input_busqueda_editar = st.text_input("Ingresar parámetro de búsqueda:")
        
    frame_fliter = frame_principal.copy()
    if input_busqueda_editar:
        frame_fliter = frame_fliter[frame_fliter[filtro_col_editar].astype(str).str.contains(input_busqueda_editar, case=False, na=False)]
        
    st.dataframe(frame_fliter, use_container_width=True)
    
    lista_contratos = frame_fliter['NUM_CONTRATO'].dropna().astype(str).tolist()
    select_contrato_editar = st.selectbox("Seleccione el NUM_CONTRATO a editar:", options=[""] + lista_contratos)
    
    if select_contrato_editar:
        fila_actual = frame_principal[frame_principal['NUM_CONTRATO'].astype(str) == select_contrato_editar].iloc[0]
        st.subheader(f"Modificando registro: {select_contrato_editar}")
        
        dic_contrato_editar = {}
        
        def get_val(columna):
            if columna not in fila_actual: return ""
            return "" if pd.isna(fila_actual[columna]) else str(fila_actual[columna])
            
        # Contenedor 1: Sección Principal
        cont_periodo = st.expander("Sección Principal", expanded=True)
        with cont_periodo:
            import re
            
            # Verificación del estado de desbloqueo en memoria
            estado_desbloqueado = st.session_state.get("status_desbloqueo_contrato", False)
            
            # Distribución en columnas para alinear el input del contrato y el botón de seguridad
            col_cont, col_btn = st.columns([8, 2])
            with col_cont:
                # El valor capturado actualizará dinámicamente el diccionario si se edita
                dic_contrato_editar["NUM_CONTRATO"] = st.text_input("NUM_CONTRATO:", value=select_contrato_editar, disabled=not estado_desbloqueado)
            with col_btn:
                st.write("")
                st.write("")
                if not estado_desbloqueado:
                    if st.button("🔓 Desbloquear", use_container_width=True):
                        emg_desbloquear_contrato()
                else:
                    if st.button("🔒 Bloquear", use_container_width=True):
                        st.session_state["status_desbloqueo_contrato"] = False
                        st.rerun()
            
            # Extracción del periodo actual para la separación algorítmica
            periodo_actual = get_val("PERIODO").strip()
            m_inicio_val, a_inicio_val, m_fin_val, a_fin_val = "", "", "", ""
            
            if periodo_actual:
                patron = r"([A-Z]+)\s+(\d{4})\s*-\s*([A-Z]+)\s+(\d{4})"
                coincidencia = re.search(patron, periodo_actual, re.IGNORECASE)
                
                if coincidencia:
                    m_inicio_val = coincidencia.group(1).upper()
                    a_inicio_val = coincidencia.group(2)
                    m_fin_val = coincidencia.group(3).upper()
                    a_fin_val = coincidencia.group(4)
                else:
                    anios = re.findall(r'\d{4}', periodo_actual)
                    if len(anios) == 2:
                        a_inicio_val, a_fin_val = anios[0], anios[1]

            lista_meses = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
            
            idx_m1 = lista_meses.index(m_inicio_val) if m_inicio_val in lista_meses else 0
            idx_m2 = lista_meses.index(m_fin_val) if m_fin_val in lista_meses else 0
            
            col_m1, col_a1, col_m2, col_a2 = st.columns(4)
            with col_m1:
                mes_inicio = st.selectbox("Mes Inicio:", options=lista_meses, index=idx_m1, key="m_ini_ed")
            with col_a1:
                anio_inicio = st.text_input("Año Inicio:", value=a_inicio_val, key="a_ini_ed")
            with col_m2:
                mes_fin = st.selectbox("Mes Fin:", options=lista_meses, index=idx_m2, key="m_fin_ed")
            with col_a2:
                anio_fin = st.text_input("Año Fin:", value=a_fin_val, key="a_fin_ed")
                
            if mes_inicio and anio_inicio and mes_fin and anio_fin:
                dic_contrato_editar["PERIODO"] = f"{mes_inicio} {anio_inicio} - {mes_fin} {anio_fin}"
            else:
                dic_contrato_editar["PERIODO"] = periodo_actual
            
        # Contenedor 2: Datos Personales
        cont_datos_per = st.expander("Datos Personales", expanded=False)
        with cont_datos_per:
            dic_contrato_editar["CEDULA"] = st.text_input("CEDULA (10 dígitos numéricos):", value=get_val("CEDULA"))
            dic_contrato_editar["NOMBRE"] = st.text_input("NOMBRE:", value=get_val("NOMBRE"))
            dic_contrato_editar["CORREO"] = st.text_input("CORREO:", value=get_val("CORREO"))
            dic_contrato_editar["CELULAR"] = st.text_input("CELULAR:", value=get_val("CELULAR"))
            dic_contrato_editar["DIRECCION"] = st.text_input("DIRECCION:", value=get_val("DIRECCION"))
            dic_contrato_editar["EDAD"] = st.text_input("EDAD:", value=get_val("EDAD"))
            
            # Inyección de opción vacía al inicio de todas las listas
            lista_opciones_genero = ["", "MUJER", "HOMBRE"]
            lista_opciones_etnia = ["", "MESTIZO", "OTRO", "INDIGENA", "MULATO", "BLANCO"]
            lista_opciones_discapacidad = ["", "NO", "SI"]
            lista_opciones_tipo = ["", "NINGUNA", "VISUAL", "FISICA", "AUDITIVA", "INTELECTUAL"]
            
            idx_genero = lista_opciones_genero.index(get_val("GENERO")) if get_val("GENERO") in lista_opciones_genero else 0
            dic_contrato_editar["GENERO"] = st.selectbox("GENERO:", options=lista_opciones_genero, index=idx_genero)
            
            idx_etnia = lista_opciones_etnia.index(get_val("ETNIA")) if get_val("ETNIA") in lista_opciones_etnia else 0
            dic_contrato_editar["ETNIA"] = st.selectbox("ETNIA:", options=lista_opciones_etnia, index=idx_etnia)
            
            idx_disc = lista_opciones_discapacidad.index(get_val("DISCAPACIDAD")) if get_val("DISCAPACIDAD") in lista_opciones_discapacidad else 0
            dic_contrato_editar["DISCAPACIDAD"] = st.selectbox("DISCAPACIDAD:", options=lista_opciones_discapacidad, index=idx_disc)
            
            # Lógica reactiva: Bloqueo del selector de tipo si es "NO" o está vacío
            if dic_contrato_editar["DISCAPACIDAD"] in ["NO", ""]:
                dic_contrato_editar["TIPO"] = st.selectbox("TIPO DE DISCAPACIDAD:", options=[""], index=0, disabled=True, key="tipo_disc_inactivo_ed")
            else:
                idx_tipo = lista_opciones_tipo.index(get_val("TIPO")) if get_val("TIPO") in lista_opciones_tipo else 0
                dic_contrato_editar["TIPO"] = st.selectbox("TIPO DE DISCAPACIDAD:", options=lista_opciones_tipo, index=idx_tipo, key="tipo_disc_activo_ed")
                
        # Contenedor 3: Información Académica
        cont_info_academica = st.expander("Información Académica", expanded=False)
        with cont_info_academica:
            # Inyección de opción vacía en la lista de facultades
            facultades_list = [""] + list(dic_facultad.keys())
            idx_fac = facultades_list.index(get_val("FACULTAD")) if get_val("FACULTAD") in facultades_list else 0
            opc_facultad = st.selectbox("FACULTAD:", options=facultades_list, index=idx_fac)
            dic_contrato_editar["FACULTAD"] = opc_facultad
            
            # Filtro de carreras condicionado a la existencia de facultad seleccionada
            carreras_disponibles = [""] + dic_facultad.get(opc_facultad, []) if opc_facultad else [""]
            idx_car = carreras_disponibles.index(get_val("CARRERA")) if get_val("CARRERA") in carreras_disponibles else 0
            opc_carrera = st.selectbox("CARRERA:", options=carreras_disponibles, index=idx_car)
            dic_contrato_editar["CARRERA"] = opc_carrera
            
            codigo_auto = dic_carrera.get(opc_carrera, "")
            dic_contrato_editar["COD CARRERA"] = codigo_auto
            st.text_input("COD CARRERA (Autoasignado):", value=codigo_auto, disabled=True)
            
            # Generación de la lista de semestres integrando la opción vacía
            lista_opciones_semestre = [""] + [str(i) for i in range(1, 12)]
            idx_sem = lista_opciones_semestre.index(get_val("SEMESTRE")) if get_val("SEMESTRE") in lista_opciones_semestre else 0
            dic_contrato_editar["SEMESTRE"] = st.selectbox("SEMESTRE:", options=lista_opciones_semestre, index=idx_sem)
            
            columnas_acad = [
                "APROBADAS", "REPROBADAS", "CONVALIDADAS", "TOMADAS", "APROBADOS", "REPROBADOS", 
                "CONVALIDADOS", "TOMADOS", "* MATRICULADOS", "* PERIODO", "CARRERA_1", 
                "GENERAL", "ACADEMICO", "* < 30%", "DEFINITIVA", "* >= 60%", "TEMPORAL"
            ]
            for col in columnas_acad:
                dic_contrato_editar[col] = st.text_input(f"{col}:", value=get_val(col))

        # Contenedor 4: Becas
        cont_becas_ot = st.expander("Becas y Ayudas", expanded=False)
        with cont_becas_ot:
            columnas_becas = ["BECAS UCE", "BECAS SENECYT", "BECAS MUNICIPIO", "HCU", "CORO", "FINANCIERO", "No BECARIO"]
            for col in columnas_becas:
                dic_contrato_editar[col] = st.text_input(f"{col}:", value=get_val(col))

        # Contenedor 5: Datos Bancarios
        cont_datos_bancarios = st.expander("Datos Bancarios", expanded=False)
        with cont_datos_bancarios:
            # La lista de bancos ya poseía el vacío, se mantiene la estructura
            bancos_list = [""] + list(dic_bancos.keys())
            idx_banco = bancos_list.index(get_val("ENTIDAD_BANCARIA")) if get_val("ENTIDAD_BANCARIA") in bancos_list else 0
            opc_entidad = st.selectbox("ENTIDAD BANCARIA:", options=bancos_list, index=idx_banco)
            dic_contrato_editar["ENTIDAD_BANCARIA"] = opc_entidad
            
            cod_entidad_bancaria_auto = dic_bancos.get(opc_entidad, "")
            dic_contrato_editar["CODIGO_BANCO"] = cod_entidad_bancaria_auto
            st.text_input("CODIGO BANCO (Autoasignado):", value=cod_entidad_bancaria_auto, disabled=True)
            
            # Inyección de opción vacía en tipo de cuenta
            lista_opc_tipo_cuenta = ["", "AHORROS", "CORRIENTE"]
            
            if not opc_entidad:
                dic_contrato_editar["TIPO_CUENTA"] = st.selectbox("TIPO_CUENTA:", options=[""], disabled=True, key="tipo_cuenta_ed_inactivo")
            else:
                idx_cuenta = lista_opc_tipo_cuenta.index(get_val("TIPO_CUENTA")) if get_val("TIPO_CUENTA") in lista_opc_tipo_cuenta else 0
                dic_contrato_editar["TIPO_CUENTA"] = st.selectbox("TIPO_CUENTA:", options=lista_opc_tipo_cuenta, index=idx_cuenta, key="tipo_cuenta_ed_activo")
                
            dic_contrato_editar["NUM_CUENTA"] = st.text_input("NUM_CUENTA:", value=get_val("NUM_CUENTA"))

        # Contenedor 6: Requerimientos Institucionales
        cont_requerimientos = st.expander("Requerimientos y Grupos", expanded=False)
        with cont_requerimientos:
            dic_contrato_editar["GRUPO"] = st.text_input("GRUPO (Solo números):", value=get_val("GRUPO"))
            dic_contrato_editar["REQUERIMIENTO_DBU"] = st.text_input("REQUERIMIENTO_DBU:", value=get_val("REQUERIMIENTO_DBU"))
            dic_contrato_editar["APROBACION_VICERECTORADO"] = st.text_input("APROBACION_VICERECTORADO:", value=get_val("APROBACION_VICERECTORADO"))

        # Contenedor 7: Observaciones
        cont_observaciones = st.expander("Observaciones", expanded=False)
        with cont_observaciones:
            # Variable de tipo text_area que recupera el valor existente en la base mediante get_val()
            input_observaciones = st.text_area("OBSERVACIONES:", value=get_val("OBSERVACIONES"))
            # Asignación del texto modificado al diccionario principal de edición
            dic_contrato_editar["OBSERVACIONES"] = input_observaciones

        if st.button("Actualizar Registro"):
            confirmacion_emg_editar(dir_db_activa, select_hoja, select_contrato_editar, dic_contrato_editar)

# Función de backend integrada para validación de archivo token
def fn_validar_token(token_upload):
    import os
    ruta_token_oficial = "data/security/token_seguridad.key"
    
    if not os.path.exists(ruta_token_oficial):
        return False, "Error crítico: Archivo token oficial no configurado en el servidor."
        
    try:
        # Lectura del contenido original en el servidor
        with open(ruta_token_oficial, "r") as f_oficial:
            token_original = f_oficial.read().strip()
            
        # Lectura de los bytes cargados por el usuario
        token_ingresado = token_upload.getvalue().decode("utf-8").strip()
        
        if token_original == token_ingresado:
            return True, "Token válido."
        else:
            return False, "El archivo token cargado es incorrecto o inválido."
            
    except Exception as e:
        return False, f"Error al procesar el archivo token: {str(e)}"

@st.dialog("Desbloqueo de Seguridad Avanzado")
def emg_desbloquear_contrato():
    st.info("Cargue el archivo Token de Seguridad (.key) autorizado para habilitar la edición del Número de Contrato.")
    
    # Componente de carga restringido a archivos .key
    token_upload = st.file_uploader("Seleccione su archivo Token:", type=["key"])
    
    btn_verificar_pass = st.button("Verificar Token y Desbloquear", type="primary")
    
    if btn_verificar_pass:
        if token_upload is None:
            st.warning("Debe cargar un archivo para proceder con la verificación.")
        else:
            estado_validacion, mensaje = fn_validar_token(token_upload)
            
            if estado_validacion:
                st.session_state["status_desbloqueo_contrato"] = True
                st.success("Contrato desbloqueado exitosamente.")
                time.sleep(2)
                st.rerun()
            else:
                st.error(mensaje)