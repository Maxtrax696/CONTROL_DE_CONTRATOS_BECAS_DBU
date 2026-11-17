# backend/cruce_archivos/comparador_ext.py

import os
import shutil
import pandas as pd

def backup_principal(ruta_base_activa):
    """Genera una copia de seguridad antes de modificar la base de datos."""
    nombre_base = os.path.basename(ruta_base_activa)
    directorio_backup = "data/backup"
    ruta_backup = f"{directorio_backup}/backup_{nombre_base}"
    
    if not os.path.exists(directorio_backup):
        os.makedirs(directorio_backup)
        
    try:
        shutil.copy2(ruta_base_activa, ruta_backup)
        return True, ruta_backup
    except Exception:
        return False, None

def fn_verificar_dupicados_ext(archivo_cargado, col_unica_ext, select_hoja_ext_duplicados=None):
    """Verifica y extrae duplicados basados en una columna única."""
    try:
        # Lectura con mecanismo de respaldo de motores
        if archivo_cargado.name.endswith('.csv'):
            df_ext = pd.read_csv(archivo_cargado)
        else:
            motor = "openpyxl" if archivo_cargado.name.endswith('.xlsx') else "xlrd"
            try:
                df_ext = pd.read_excel(archivo_cargado, sheet_name=select_hoja_ext_duplicados, engine=motor)
            except Exception:
                motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                try:
                    df_ext = pd.read_excel(archivo_cargado, sheet_name=select_hoja_ext_duplicados, engine=motor_alt)
                except Exception:
                    df_ext = pd.read_html(archivo_cargado)[0]
            
        # Algoritmo de filtrado por columna única
        mascara_dup = df_ext.duplicated(subset=[col_unica_ext], keep=False)
        df_duplicados = df_ext[mascara_dup].copy()
        
        if df_duplicados.empty:
            return True, "No se encontraron registros duplicados bajo la columna seleccionada.", ""
            
        directorio = "data/duplicados"
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            
        # Sanitización de nomenclatura
        col_sanitizada = str(col_unica_ext).strip().replace(" ", "_")
        nombre_base = os.path.splitext(archivo_cargado.name)[0]
        ruta_salida = f"{directorio}/duplicados_{col_sanitizada}_{nombre_base}.xlsx"
        
        df_duplicados.to_excel(ruta_salida, index=False)
        
        return True, f"Se extrajeron {len(df_duplicados)} registros duplicados exitosamente.", ruta_salida
        
    except Exception as e:
        return False, f"Error técnico durante el análisis: {str(e)}", ""


def fn_cruzar_datos_ext(dir_db_activa, select_hoja_principal, file_cruce_ext, select_hoja_cruce_ext, cedula_ext, dic_map_cruce):
    # Sub-función con inyección de carácter invisible (\u200b) para bloqueo estricto de autoconversión
    def _formatear_cedula(val):
        if pd.isna(val):
            return ""
        s_val = str(val).strip().upper()
        if s_val in ["", "NAN", "NONE", "NAT", "<NA>", "NULL"]:
            return ""
        if s_val.endswith(".0"):
            s_val = s_val[:-2]
        s_val = s_val.split(".")[0]
        # Inyección del zero-width space para forzar formato de texto en Excel
        return f"\u200b{s_val.zfill(10)}"

    try:
        status_backup, _ = backup_principal(dir_db_activa)
        if not status_backup:
            return False, "Error al crear el backup de seguridad. Se abortó el cruce."
            
        df_principal = pd.read_excel(dir_db_activa, sheet_name=select_hoja_principal, dtype=str).fillna("")
        
        if file_cruce_ext.name.endswith('.csv'):
            df_ext = pd.read_csv(file_cruce_ext, dtype=str).fillna("")
        else:
            motor = "openpyxl" if file_cruce_ext.name.endswith('.xlsx') else "xlrd"
            try:
                df_ext = pd.read_excel(file_cruce_ext, sheet_name=select_hoja_cruce_ext, engine=motor, dtype=str).fillna("")
            except Exception:
                motor_alt = "xlrd" if motor == "openpyxl" else "openpyxl"
                try:
                    df_ext = pd.read_excel(file_cruce_ext, sheet_name=select_hoja_cruce_ext, engine=motor_alt, dtype=str).fillna("")
                except Exception:
                    df_ext = pd.read_html(file_cruce_ext)[0].astype(str).fillna("")
                    
        if "CEDULA" in df_principal.columns:
            df_principal["CEDULA"] = df_principal["CEDULA"].apply(lambda x: str(x).replace('\u200b', '')).apply(_formatear_cedula)
            
        if cedula_ext in df_ext.columns:
            df_ext[cedula_ext] = df_ext[cedula_ext].apply(lambda x: str(x).replace('\u200b', '')).apply(_formatear_cedula)

        if "CEDULA" not in df_principal.columns:
            return False, "La base principal no contiene la columna 'CEDULA'."
        if cedula_ext not in df_ext.columns:
            return False, f"El archivo externo no tiene la columna '{cedula_ext}'."
            
        sufijo_duplicados = "-DUPLICADO"
        col_contrato_ext = dic_map_cruce.get("NUM_CONTRATO")
        
        if col_contrato_ext and col_contrato_ext in df_ext.columns:
            df_ext["_temp_contrato"] = df_ext[col_contrato_ext].astype(str).str.strip().str.upper()
            mascara_validos = ~df_ext["_temp_contrato"].isin(["", "NAN", "NONE", "NAT"])
            
            contratos_repetidos = df_ext[mascara_validos]["_temp_contrato"].value_counts()
            contratos_repetidos = contratos_repetidos[contratos_repetidos > 1].index.tolist()
            
            mascara_aplicar = df_ext["_temp_contrato"].isin(contratos_repetidos)
            if mascara_aplicar.any():
                df_ext.loc[mascara_aplicar, col_contrato_ext] = df_ext.loc[mascara_aplicar, col_contrato_ext].astype(str) + sufijo_duplicados
                
            df_ext = df_ext.drop(columns=["_temp_contrato"])
            
        conteo_actualizados = 0
        conteo_nuevos = 0
        nuevos_registros = []
        
        contratos_existentes = set(df_principal["NUM_CONTRATO"].astype(str).str.strip().str.upper())
        cuentas_existentes = set()
        if "NUM_CUENTA" in df_principal.columns:
            cuentas_existentes = set(df_principal["NUM_CUENTA"].astype(str).str.strip().str.upper())
            
        for idx_ext, row_ext in df_ext.iterrows():
            cedula_ext_val = row_ext[cedula_ext]
            
            if cedula_ext_val in ["", "NAN", "NONE", "NAT", "\u200b"]:
                continue
                
            if col_contrato_ext and col_contrato_ext in df_ext.columns:
                contrato_evaluar = str(row_ext[col_contrato_ext]).strip().upper()
                if contrato_evaluar not in ["", "NAN", "NONE", "NAT"]:
                    if select_hoja_principal == "EXCELENCIA" and "-BEA-" not in contrato_evaluar:
                        continue 
                    if select_hoja_principal == "VULNERABILIDAD" and "-VUL-" not in contrato_evaluar:
                        continue 
                
            mascara = df_principal["CEDULA"].astype(str).str.strip().str.upper() == cedula_ext_val.strip().upper()
            coincidencias = df_principal[mascara]
            
            if not coincidencias.empty:
                idx_prin = coincidencias.index[0]
                actualizado = False
                
                for col_prin, col_ext in dic_map_cruce.items():
                    if col_prin not in df_principal.columns or col_ext not in df_ext.columns:
                        continue
                        
                    valor_actual = df_principal.loc[idx_prin, col_prin]
                    valor_nuevo = row_ext[col_ext]
                    
                    if pd.isna(valor_actual) or str(valor_actual).strip().upper() in ["", "NAN", "NONE", "NAT"]:
                        valor_nuevo_str = str(valor_nuevo).strip().upper()
                        
                        if col_prin == "NUM_CONTRATO" and valor_nuevo_str not in ["", "NAN"]:
                            if valor_nuevo_str in contratos_existentes and not valor_nuevo_str.endswith(sufijo_duplicados):
                                mascara_preexistente = df_principal["NUM_CONTRATO"].astype(str).str.strip().str.upper() == valor_nuevo_str
                                df_principal.loc[mascara_preexistente, "NUM_CONTRATO"] = valor_nuevo_str + sufijo_duplicados
                                
                                etiqueta_contrato = f"{valor_nuevo_str}{sufijo_duplicados}"
                                valor_nuevo = etiqueta_contrato
                            else:
                                contratos_existentes.add(valor_nuevo_str)
                            
                        if col_prin == "NUM_CUENTA" and valor_nuevo_str not in ["", "NAN"]:
                            if valor_nuevo_str in cuentas_existentes:
                                continue
                            cuentas_existentes.add(valor_nuevo_str)
                            
                        df_principal.at[idx_prin, col_prin] = valor_nuevo
                        actualizado = True
                        
                if actualizado:
                    conteo_actualizados += 1
                    
            else:
                nuevo_dic = {}
                for col_prin, col_ext in dic_map_cruce.items():
                    if col_ext in df_ext.columns:
                        valor_nuevo = row_ext[col_ext]
                        valor_nuevo_str = str(valor_nuevo).strip().upper()
                        
                        if col_prin == "NUM_CONTRATO" and valor_nuevo_str not in ["", "NAN"]:
                            if valor_nuevo_str in contratos_existentes and not valor_nuevo_str.endswith(sufijo_duplicados):
                                mascara_preexistente = df_principal["NUM_CONTRATO"].astype(str).str.strip().str.upper() == valor_nuevo_str
                                df_principal.loc[mascara_preexistente, "NUM_CONTRATO"] = valor_nuevo_str + sufijo_duplicados
                                
                                etiqueta_contrato = f"{valor_nuevo_str}{sufijo_duplicados}"
                                nuevo_dic[col_prin] = etiqueta_contrato
                                continue
                            contratos_existentes.add(valor_nuevo_str)
                            
                        if col_prin == "NUM_CUENTA" and valor_nuevo_str not in ["", "NAN"]:
                            if valor_nuevo_str in cuentas_existentes:
                                nuevo_dic[col_prin] = ""
                                continue
                            cuentas_existentes.add(valor_nuevo_str)
                            
                        nuevo_dic[col_prin] = valor_nuevo
                        
                if "CEDULA" not in nuevo_dic:
                    nuevo_dic["CEDULA"] = cedula_ext_val
                    
                nuevos_registros.append(nuevo_dic)
                conteo_nuevos += 1
                
        if nuevos_registros:
            df_principal = pd.concat([df_principal, pd.DataFrame(nuevos_registros)], ignore_index=True)
            
        if "CEDULA" in df_principal.columns:
            df_principal["CEDULA"] = df_principal["CEDULA"].astype(str).replace({"nan": "", "NAN": "", "None": ""})
            
        try:
            with pd.ExcelWriter(dir_db_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df_principal.to_excel(writer, sheet_name=select_hoja_principal, index=False)
        except PermissionError:
            return False, f"El archivo '{dir_db_activa}' está abierto. Ciérrelo para permitir el cruce."
            
        return True, f"Cruce exitoso: {conteo_actualizados} estudiantes actualizados y {conteo_nuevos} nuevos insertados."
        
    except Exception as e:
        return False, f"Error técnico durante el cruce: {str(e)}"