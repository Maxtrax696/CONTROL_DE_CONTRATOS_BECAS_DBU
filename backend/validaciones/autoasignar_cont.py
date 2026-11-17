<<<<<<< HEAD
# backend/validaciones/autoasignar_cont.py

import pandas as pd
from backend.db_operaciones.lector_excel import leer_base_datos

def obtener_nuevo_contrato(dir_db_activa, select_hoja, periodo_extraido):
    import pandas as pd
    from backend.db_operaciones.lector_excel import leer_base_datos
    
    frame_principal = leer_base_datos(dir_db_activa, select_hoja)
    
    # Definición de la etiqueta según la hoja seleccionada
    etiqueta = "-BEA-" if str(select_hoja).strip().upper() == "EXCELENCIA" else "-VUL-"
    
    # Construcción del patrón base combinando los años y la etiqueta (ej: "2024-2025-BEA-")
    patron_periodo = f"{periodo_extraido}{etiqueta}"
    
    if 'NUM_CONTRATO' not in frame_principal.columns or frame_principal.empty:
        return f"{patron_periodo}0001"
        
    contratos_actuales = frame_principal['NUM_CONTRATO'].dropna().astype(str).tolist()
    numeros_existentes = []
    
    # Filtrado y extracción de los correlativos que coincidan estrictamente con el patrón del periodo actual
    for contrato in contratos_actuales:
        if patron_periodo in contrato:
            try:
                num = int(contrato.split(patron_periodo)[1].split("-")[0])
                numeros_existentes.append(num)
            except ValueError:
                pass
                
    numeros_existentes.sort()
    contratos_disponibles = []
    
    if numeros_existentes:
        max_num = max(numeros_existentes)
        for i in range(1, max_num):
            if i not in numeros_existentes:
                contratos_disponibles.append(i)
    
    if contratos_disponibles:
        num_asignar = contratos_disponibles[0]
    else:
        num_asignar = (max(numeros_existentes) + 1) if numeros_existentes else 1
        
    # Ensamblaje final del contrato
    asignacion_contrato = f"{patron_periodo}{num_asignar:04d}"
    
    return asignacion_contrato

def autoasignacion_contratos_vacios(dir_db_activa, select_hoja):
    try:
        import pandas as pd
        import re
        
        frame_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja)
        etiqueta = "-BEA-" if str(select_hoja).strip().upper() == "EXCELENCIA" else "-VUL-"
        
        if 'NUM_CONTRATO' not in frame_principal.columns or 'PERIODO' not in frame_principal.columns:
            return False, "Faltan las columnas NUM_CONTRATO o PERIODO."
            
        frame_principal['NUM_CONTRATO'] = frame_principal['NUM_CONTRATO'].fillna("").astype(str)
        frame_principal['NUM_CONTRATO'] = frame_principal['NUM_CONTRATO'].replace(["NAN", "NONE", "<NA>", "NAT"], "", regex=True)
        
        vacios_mask = frame_principal['NUM_CONTRATO'].str.strip() == ""
        if not vacios_mask.any():
            return False, "No se encontraron registros vacíos para autoasignar."
            
        contratos_actuales = frame_principal.loc[~vacios_mask, 'NUM_CONTRATO'].str.strip().tolist()
        dic_usados_por_periodo = {}
        
        # Agrupación de números ocupados por cada bloque de años independientes
        for c in contratos_actuales:
            if etiqueta in c:
                partes = c.split(etiqueta)
                if len(partes) == 2:
                    periodo_str = partes[0]
                    num_str = partes[1].split("-")[0]
                    try:
                        num = int(num_str)
                        if periodo_str not in dic_usados_por_periodo:
                            dic_usados_por_periodo[periodo_str] = set()
                        dic_usados_por_periodo[periodo_str].add(num)
                    except ValueError:
                        pass
                        
        conteo_asignados = 0
        
        for idx in frame_principal[vacios_mask].index:
            periodo_celda = str(frame_principal.at[idx, 'PERIODO']).strip()
            
            if not periodo_celda or periodo_celda.upper() in ["NAN", "NONE", ""]:
                continue
                
            anios_extraidos = re.findall(r'\d{4}', periodo_celda)
            if len(anios_extraidos) >= 2:
                periodo_regex = f"{anios_extraidos[0]}-{anios_extraidos[1]}"
            else:
                continue # Se omite si el texto no contiene al menos dos años (ej: 2024 y 2025)
                
            if periodo_regex not in dic_usados_por_periodo:
                dic_usados_por_periodo[periodo_regex] = set()
                
            set_usados = dic_usados_por_periodo[periodo_regex]
            max_actual = max(set_usados) if set_usados else 0
            disponibles_intermedios = [i for i in range(1, max_actual) if i not in set_usados]
            
            if disponibles_intermedios:
                num_asignar = disponibles_intermedios[0]
            else:
                num_asignar = max_actual + 1
                
            nuevo_contrato = f"{periodo_regex}{etiqueta}{num_asignar:04d}"
            frame_principal.at[idx, 'NUM_CONTRATO'] = nuevo_contrato
            
            # Se registra como ocupado para la siguiente iteración
            dic_usados_por_periodo[periodo_regex].add(num_asignar)
            conteo_asignados += 1
            
        with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_principal.to_excel(writer, sheet_name=select_hoja, index=False)
            
        return True, f"Se asignaron {conteo_asignados} contratos. Los expedientes sin periodo se omitieron."
    except Exception as e:
        return False, f"Error en asignación masiva: {str(e)}"

def autoasignacion_codigos_diccionarios(dir_db_activa, select_hoja):
    """
    Función de backend para autoasignar COD CARRERA y CODIGO_BANCO a registros 
    que posean la información matriz pero tengan el código vacío.
    """
    try:
        import pandas as pd
        from backend.db_operaciones.datos_academicos import dic_carrera, dic_bancos
        
        frame_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja)
        
        if 'COD CARRERA' not in frame_principal.columns or 'CODIGO_BANCO' not in frame_principal.columns:
            return False, "Faltan las columnas COD CARRERA o CODIGO_BANCO en la estructura de esta hoja."
            
        # Forzado estricto a tipo object para permitir inyección de cadenas de texto
        frame_principal['COD CARRERA'] = frame_principal['COD CARRERA'].astype(object)
        frame_principal['CODIGO_BANCO'] = frame_principal['CODIGO_BANCO'].astype(object)
            
        conteo_carreras = 0
        conteo_bancos = 0
        
        for idx, fila in frame_principal.iterrows():
            carrera_actual = str(fila.get('CARRERA', '')).strip()
            cod_carrera_actual = str(fila.get('COD CARRERA', '')).strip()
            
            if carrera_actual and carrera_actual.upper() not in ["NAN", "NONE"]:
                if not cod_carrera_actual or cod_carrera_actual.upper() in ["NAN", "NONE"]:
                    nuevo_cod = dic_carrera.get(carrera_actual, "")
                    if nuevo_cod:
                        frame_principal.at[idx, 'COD CARRERA'] = nuevo_cod
                        conteo_carreras += 1
                        
            banco_actual = str(fila.get('ENTIDAD_BANCARIA', '')).strip()
            cod_banco_actual = str(fila.get('CODIGO_BANCO', '')).strip()
            
            if banco_actual and banco_actual.upper() not in ["NAN", "NONE"]:
                if not cod_banco_actual or cod_banco_actual.upper() in ["NAN", "NONE"]:
                    nuevo_cod_banco = dic_bancos.get(banco_actual, "")
                    if nuevo_cod_banco:
                        frame_principal.at[idx, 'CODIGO_BANCO'] = nuevo_cod_banco
                        conteo_bancos += 1
                        
        with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_principal.to_excel(writer, sheet_name=select_hoja, index=False)
            
        return True, f"Proceso finalizado. Códigos de Carrera asignados: {conteo_carreras} | Códigos de Banco asignados: {conteo_bancos}."
        
    except Exception as e:
=======
<<<<<<< HEAD
# backend/validaciones/autoasignar_cont.py

import pandas as pd
from backend.db_operaciones.lector_excel import leer_base_datos

def obtener_nuevo_contrato(dir_db_activa, select_hoja, periodo_extraido):
    import pandas as pd
    from backend.db_operaciones.lector_excel import leer_base_datos
    
    frame_principal = leer_base_datos(dir_db_activa, select_hoja)
    
    # Definición de la etiqueta según la hoja seleccionada
    etiqueta = "-BEA-" if str(select_hoja).strip().upper() == "EXCELENCIA" else "-VUL-"
    
    # Construcción del patrón base combinando los años y la etiqueta (ej: "2024-2025-BEA-")
    patron_periodo = f"{periodo_extraido}{etiqueta}"
    
    if 'NUM_CONTRATO' not in frame_principal.columns or frame_principal.empty:
        return f"{patron_periodo}0001"
        
    contratos_actuales = frame_principal['NUM_CONTRATO'].dropna().astype(str).tolist()
    numeros_existentes = []
    
    # Filtrado y extracción de los correlativos que coincidan estrictamente con el patrón del periodo actual
    for contrato in contratos_actuales:
        if patron_periodo in contrato:
            try:
                num = int(contrato.split(patron_periodo)[1].split("-")[0])
                numeros_existentes.append(num)
            except ValueError:
                pass
                
    numeros_existentes.sort()
    contratos_disponibles = []
    
    if numeros_existentes:
        max_num = max(numeros_existentes)
        for i in range(1, max_num):
            if i not in numeros_existentes:
                contratos_disponibles.append(i)
    
    if contratos_disponibles:
        num_asignar = contratos_disponibles[0]
    else:
        num_asignar = (max(numeros_existentes) + 1) if numeros_existentes else 1
        
    # Ensamblaje final del contrato
    asignacion_contrato = f"{patron_periodo}{num_asignar:04d}"
    
    return asignacion_contrato

def autoasignacion_contratos_vacios(dir_db_activa, select_hoja):
    try:
        import pandas as pd
        import re
        
        frame_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja)
        etiqueta = "-BEA-" if str(select_hoja).strip().upper() == "EXCELENCIA" else "-VUL-"
        
        if 'NUM_CONTRATO' not in frame_principal.columns or 'PERIODO' not in frame_principal.columns:
            return False, "Faltan las columnas NUM_CONTRATO o PERIODO."
            
        frame_principal['NUM_CONTRATO'] = frame_principal['NUM_CONTRATO'].fillna("").astype(str)
        frame_principal['NUM_CONTRATO'] = frame_principal['NUM_CONTRATO'].replace(["NAN", "NONE", "<NA>", "NAT"], "", regex=True)
        
        vacios_mask = frame_principal['NUM_CONTRATO'].str.strip() == ""
        if not vacios_mask.any():
            return False, "No se encontraron registros vacíos para autoasignar."
            
        contratos_actuales = frame_principal.loc[~vacios_mask, 'NUM_CONTRATO'].str.strip().tolist()
        dic_usados_por_periodo = {}
        
        # Agrupación de números ocupados por cada bloque de años independientes
        for c in contratos_actuales:
            if etiqueta in c:
                partes = c.split(etiqueta)
                if len(partes) == 2:
                    periodo_str = partes[0]
                    num_str = partes[1].split("-")[0]
                    try:
                        num = int(num_str)
                        if periodo_str not in dic_usados_por_periodo:
                            dic_usados_por_periodo[periodo_str] = set()
                        dic_usados_por_periodo[periodo_str].add(num)
                    except ValueError:
                        pass
                        
        conteo_asignados = 0
        
        for idx in frame_principal[vacios_mask].index:
            periodo_celda = str(frame_principal.at[idx, 'PERIODO']).strip()
            
            if not periodo_celda or periodo_celda.upper() in ["NAN", "NONE", ""]:
                continue
                
            anios_extraidos = re.findall(r'\d{4}', periodo_celda)
            if len(anios_extraidos) >= 2:
                periodo_regex = f"{anios_extraidos[0]}-{anios_extraidos[1]}"
            else:
                continue # Se omite si el texto no contiene al menos dos años (ej: 2024 y 2025)
                
            if periodo_regex not in dic_usados_por_periodo:
                dic_usados_por_periodo[periodo_regex] = set()
                
            set_usados = dic_usados_por_periodo[periodo_regex]
            max_actual = max(set_usados) if set_usados else 0
            disponibles_intermedios = [i for i in range(1, max_actual) if i not in set_usados]
            
            if disponibles_intermedios:
                num_asignar = disponibles_intermedios[0]
            else:
                num_asignar = max_actual + 1
                
            nuevo_contrato = f"{periodo_regex}{etiqueta}{num_asignar:04d}"
            frame_principal.at[idx, 'NUM_CONTRATO'] = nuevo_contrato
            
            # Se registra como ocupado para la siguiente iteración
            dic_usados_por_periodo[periodo_regex].add(num_asignar)
            conteo_asignados += 1
            
        with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_principal.to_excel(writer, sheet_name=select_hoja, index=False)
            
        return True, f"Se asignaron {conteo_asignados} contratos. Los expedientes sin periodo se omitieron."
    except Exception as e:
        return False, f"Error en asignación masiva: {str(e)}"

def autoasignacion_codigos_diccionarios(dir_db_activa, select_hoja):
    """
    Función de backend para autoasignar COD CARRERA y CODIGO_BANCO a registros 
    que posean la información matriz pero tengan el código vacío.
    """
    try:
        import pandas as pd
        from backend.db_operaciones.datos_academicos import dic_carrera, dic_bancos
        
        frame_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja)
        
        if 'COD CARRERA' not in frame_principal.columns or 'CODIGO_BANCO' not in frame_principal.columns:
            return False, "Faltan las columnas COD CARRERA o CODIGO_BANCO en la estructura de esta hoja."
            
        # Forzado estricto a tipo object para permitir inyección de cadenas de texto
        frame_principal['COD CARRERA'] = frame_principal['COD CARRERA'].astype(object)
        frame_principal['CODIGO_BANCO'] = frame_principal['CODIGO_BANCO'].astype(object)
            
        conteo_carreras = 0
        conteo_bancos = 0
        
        for idx, fila in frame_principal.iterrows():
            carrera_actual = str(fila.get('CARRERA', '')).strip()
            cod_carrera_actual = str(fila.get('COD CARRERA', '')).strip()
            
            if carrera_actual and carrera_actual.upper() not in ["NAN", "NONE"]:
                if not cod_carrera_actual or cod_carrera_actual.upper() in ["NAN", "NONE"]:
                    nuevo_cod = dic_carrera.get(carrera_actual, "")
                    if nuevo_cod:
                        frame_principal.at[idx, 'COD CARRERA'] = nuevo_cod
                        conteo_carreras += 1
                        
            banco_actual = str(fila.get('ENTIDAD_BANCARIA', '')).strip()
            cod_banco_actual = str(fila.get('CODIGO_BANCO', '')).strip()
            
            if banco_actual and banco_actual.upper() not in ["NAN", "NONE"]:
                if not cod_banco_actual or cod_banco_actual.upper() in ["NAN", "NONE"]:
                    nuevo_cod_banco = dic_bancos.get(banco_actual, "")
                    if nuevo_cod_banco:
                        frame_principal.at[idx, 'CODIGO_BANCO'] = nuevo_cod_banco
                        conteo_bancos += 1
                        
        with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_principal.to_excel(writer, sheet_name=select_hoja, index=False)
            
        return True, f"Proceso finalizado. Códigos de Carrera asignados: {conteo_carreras} | Códigos de Banco asignados: {conteo_bancos}."
        
    except Exception as e:
=======
# backend/validaciones/autoasignar_cont.py

import pandas as pd
from backend.db_operaciones.lector_excel import leer_base_datos

def obtener_nuevo_contrato(dir_db_activa, select_hoja, periodo_extraido):
    import pandas as pd
    from backend.db_operaciones.lector_excel import leer_base_datos
    
    frame_principal = leer_base_datos(dir_db_activa, select_hoja)
    
    # Definición de la etiqueta según la hoja seleccionada
    etiqueta = "-BEA-" if str(select_hoja).strip().upper() == "EXCELENCIA" else "-VUL-"
    
    # Construcción del patrón base combinando los años y la etiqueta (ej: "2024-2025-BEA-")
    patron_periodo = f"{periodo_extraido}{etiqueta}"
    
    if 'NUM_CONTRATO' not in frame_principal.columns or frame_principal.empty:
        return f"{patron_periodo}0001"
        
    contratos_actuales = frame_principal['NUM_CONTRATO'].dropna().astype(str).tolist()
    numeros_existentes = []
    
    # Filtrado y extracción de los correlativos que coincidan estrictamente con el patrón del periodo actual
    for contrato in contratos_actuales:
        if patron_periodo in contrato:
            try:
                num = int(contrato.split(patron_periodo)[1].split("-")[0])
                numeros_existentes.append(num)
            except ValueError:
                pass
                
    numeros_existentes.sort()
    contratos_disponibles = []
    
    if numeros_existentes:
        max_num = max(numeros_existentes)
        for i in range(1, max_num):
            if i not in numeros_existentes:
                contratos_disponibles.append(i)
    
    if contratos_disponibles:
        num_asignar = contratos_disponibles[0]
    else:
        num_asignar = (max(numeros_existentes) + 1) if numeros_existentes else 1
        
    # Ensamblaje final del contrato
    asignacion_contrato = f"{patron_periodo}{num_asignar:04d}"
    
    return asignacion_contrato

def autoasignacion_contratos_vacios(dir_db_activa, select_hoja):
    try:
        import pandas as pd
        import re
        
        frame_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja)
        etiqueta = "-BEA-" if str(select_hoja).strip().upper() == "EXCELENCIA" else "-VUL-"
        
        if 'NUM_CONTRATO' not in frame_principal.columns or 'PERIODO' not in frame_principal.columns:
            return False, "Faltan las columnas NUM_CONTRATO o PERIODO."
            
        frame_principal['NUM_CONTRATO'] = frame_principal['NUM_CONTRATO'].fillna("").astype(str)
        frame_principal['NUM_CONTRATO'] = frame_principal['NUM_CONTRATO'].replace(["NAN", "NONE", "<NA>", "NAT"], "", regex=True)
        
        vacios_mask = frame_principal['NUM_CONTRATO'].str.strip() == ""
        if not vacios_mask.any():
            return False, "No se encontraron registros vacíos para autoasignar."
            
        contratos_actuales = frame_principal.loc[~vacios_mask, 'NUM_CONTRATO'].str.strip().tolist()
        dic_usados_por_periodo = {}
        
        # Agrupación de números ocupados por cada bloque de años independientes
        for c in contratos_actuales:
            if etiqueta in c:
                partes = c.split(etiqueta)
                if len(partes) == 2:
                    periodo_str = partes[0]
                    num_str = partes[1].split("-")[0]
                    try:
                        num = int(num_str)
                        if periodo_str not in dic_usados_por_periodo:
                            dic_usados_por_periodo[periodo_str] = set()
                        dic_usados_por_periodo[periodo_str].add(num)
                    except ValueError:
                        pass
                        
        conteo_asignados = 0
        
        for idx in frame_principal[vacios_mask].index:
            periodo_celda = str(frame_principal.at[idx, 'PERIODO']).strip()
            
            if not periodo_celda or periodo_celda.upper() in ["NAN", "NONE", ""]:
                continue
                
            anios_extraidos = re.findall(r'\d{4}', periodo_celda)
            if len(anios_extraidos) >= 2:
                periodo_regex = f"{anios_extraidos[0]}-{anios_extraidos[1]}"
            else:
                continue # Se omite si el texto no contiene al menos dos años (ej: 2024 y 2025)
                
            if periodo_regex not in dic_usados_por_periodo:
                dic_usados_por_periodo[periodo_regex] = set()
                
            set_usados = dic_usados_por_periodo[periodo_regex]
            max_actual = max(set_usados) if set_usados else 0
            disponibles_intermedios = [i for i in range(1, max_actual) if i not in set_usados]
            
            if disponibles_intermedios:
                num_asignar = disponibles_intermedios[0]
            else:
                num_asignar = max_actual + 1
                
            nuevo_contrato = f"{periodo_regex}{etiqueta}{num_asignar:04d}"
            frame_principal.at[idx, 'NUM_CONTRATO'] = nuevo_contrato
            
            # Se registra como ocupado para la siguiente iteración
            dic_usados_por_periodo[periodo_regex].add(num_asignar)
            conteo_asignados += 1
            
        with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_principal.to_excel(writer, sheet_name=select_hoja, index=False)
            
        return True, f"Se asignaron {conteo_asignados} contratos. Los expedientes sin periodo se omitieron."
    except Exception as e:
        return False, f"Error en asignación masiva: {str(e)}"

def autoasignacion_codigos_diccionarios(dir_db_activa, select_hoja):
    """
    Función de backend para autoasignar COD CARRERA y CODIGO_BANCO a registros 
    que posean la información matriz pero tengan el código vacío.
    """
    try:
        import pandas as pd
        from backend.db_operaciones.datos_academicos import dic_carrera, dic_bancos
        
        frame_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja)
        
        if 'COD CARRERA' not in frame_principal.columns or 'CODIGO_BANCO' not in frame_principal.columns:
            return False, "Faltan las columnas COD CARRERA o CODIGO_BANCO en la estructura de esta hoja."
            
        # Forzado estricto a tipo object para permitir inyección de cadenas de texto
        frame_principal['COD CARRERA'] = frame_principal['COD CARRERA'].astype(object)
        frame_principal['CODIGO_BANCO'] = frame_principal['CODIGO_BANCO'].astype(object)
            
        conteo_carreras = 0
        conteo_bancos = 0
        
        for idx, fila in frame_principal.iterrows():
            carrera_actual = str(fila.get('CARRERA', '')).strip()
            cod_carrera_actual = str(fila.get('COD CARRERA', '')).strip()
            
            if carrera_actual and carrera_actual.upper() not in ["NAN", "NONE"]:
                if not cod_carrera_actual or cod_carrera_actual.upper() in ["NAN", "NONE"]:
                    nuevo_cod = dic_carrera.get(carrera_actual, "")
                    if nuevo_cod:
                        frame_principal.at[idx, 'COD CARRERA'] = nuevo_cod
                        conteo_carreras += 1
                        
            banco_actual = str(fila.get('ENTIDAD_BANCARIA', '')).strip()
            cod_banco_actual = str(fila.get('CODIGO_BANCO', '')).strip()
            
            if banco_actual and banco_actual.upper() not in ["NAN", "NONE"]:
                if not cod_banco_actual or cod_banco_actual.upper() in ["NAN", "NONE"]:
                    nuevo_cod_banco = dic_bancos.get(banco_actual, "")
                    if nuevo_cod_banco:
                        frame_principal.at[idx, 'CODIGO_BANCO'] = nuevo_cod_banco
                        conteo_bancos += 1
                        
        with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_principal.to_excel(writer, sheet_name=select_hoja, index=False)
            
        return True, f"Proceso finalizado. Códigos de Carrera asignados: {conteo_carreras} | Códigos de Banco asignados: {conteo_bancos}."
        
    except Exception as e:
>>>>>>> 0b7154d72bff2a5861fc17effcf996fc49c975ed
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
        return False, f"Error técnico en asignación de códigos: {str(e)}"