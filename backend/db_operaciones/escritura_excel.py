<<<<<<< HEAD
# backend/db_operaciones/escritura_excel.py

import pandas as pd

def fn_guardar_nuevo_registro(ruta_base_activa, select_hoja, dic_temp):
    try:
        # Lectura de la hoja específica
        frame_actual = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        
        # Concatenación del nuevo dato
        frame_nuevo = pd.DataFrame([dic_temp])
        frame_actualizado = pd.concat([frame_actual, frame_nuevo], ignore_index=True)
        
        # Escritura atómica en la base activa sin temporales
        with pd.ExcelWriter(ruta_base_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_actualizado.to_excel(writer, sheet_name=select_hoja, index=False)
            
        # Retorno obligatorio de 2 valores para coincidir con el desempaquetado del frontend
        return True, "Éxito"
    except Exception as e:
        # Retorno de 2 valores en caso de error
        return False, str(e)

def fn_modificar_registro(ruta_base_activa, select_hoja, buscar_contrato, dic_temp):
    try:
        frame_actual = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        
        indice = frame_actual[frame_actual['NUM_CONTRATO'].astype(str) == buscar_contrato].index
        
        if not indice.empty:
            for col, val in dic_temp.items():
                if col in frame_actual.columns:
                    # Conversión a object para prevenir Invalid value '...' for dtype 'int64'
                    if pd.api.types.is_numeric_dtype(frame_actual[col]):
                        frame_actual[col] = frame_actual[col].astype(object)
                    frame_actual.loc[indice[0], col] = val
                    
            with pd.ExcelWriter(ruta_base_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                frame_actual.to_excel(writer, sheet_name=select_hoja, index=False)
                
            return True, "Éxito"
        else:
            return False, "No se encontró el contrato."
    except PermissionError:
        return False, "El archivo Excel está abierto. Ciérrelo para permitir la modificación."
    except Exception as e:
        return False, str(e)

def fn_eliminar_registro(ruta_base_activa, select_hoja, buscar_contrato):
    try:
        frame_actual = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        
        indice = frame_actual[frame_actual['NUM_CONTRATO'].astype(str) == buscar_contrato].index
        
        if not indice.empty:
            frame_actual = frame_actual.drop(indice)
            
            with pd.ExcelWriter(ruta_base_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                frame_actual.to_excel(writer, sheet_name=select_hoja, index=False)
                
            return True
        else:
            return False
    except PermissionError:
        return False
    except Exception:
=======
# backend/db_operaciones/escritura_excel.py

import pandas as pd

def fn_guardar_nuevo_registro(ruta_base_activa, select_hoja, dic_temp):
    try:
        # Lectura de la hoja específica
        frame_actual = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        
        # Concatenación del nuevo dato
        frame_nuevo = pd.DataFrame([dic_temp])
        frame_actualizado = pd.concat([frame_actual, frame_nuevo], ignore_index=True)
        
        # Escritura atómica en la base activa sin temporales
        with pd.ExcelWriter(ruta_base_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            frame_actualizado.to_excel(writer, sheet_name=select_hoja, index=False)
            
        # Retorno obligatorio de 2 valores para coincidir con el desempaquetado del frontend
        return True, "Éxito"
    except Exception as e:
        # Retorno de 2 valores en caso de error
        return False, str(e)

def fn_modificar_registro(ruta_base_activa, select_hoja, buscar_contrato, dic_temp):
    try:
        frame_actual = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        
        indice = frame_actual[frame_actual['NUM_CONTRATO'].astype(str) == buscar_contrato].index
        
        if not indice.empty:
            for col, val in dic_temp.items():
                if col in frame_actual.columns:
                    # Conversión a object para prevenir Invalid value '...' for dtype 'int64'
                    if pd.api.types.is_numeric_dtype(frame_actual[col]):
                        frame_actual[col] = frame_actual[col].astype(object)
                    frame_actual.loc[indice[0], col] = val
                    
            with pd.ExcelWriter(ruta_base_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                frame_actual.to_excel(writer, sheet_name=select_hoja, index=False)
                
            return True, "Éxito"
        else:
            return False, "No se encontró el contrato."
    except PermissionError:
        return False, "El archivo Excel está abierto. Ciérrelo para permitir la modificación."
    except Exception as e:
        return False, str(e)

def fn_eliminar_registro(ruta_base_activa, select_hoja, buscar_contrato):
    try:
        frame_actual = pd.read_excel(ruta_base_activa, sheet_name=select_hoja)
        
        indice = frame_actual[frame_actual['NUM_CONTRATO'].astype(str) == buscar_contrato].index
        
        if not indice.empty:
            frame_actual = frame_actual.drop(indice)
            
            with pd.ExcelWriter(ruta_base_activa, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                frame_actual.to_excel(writer, sheet_name=select_hoja, index=False)
                
            return True
        else:
            return False
    except PermissionError:
        return False
    except Exception:
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
        return False