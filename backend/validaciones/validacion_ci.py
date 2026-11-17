<<<<<<< HEAD
# backend/validaciones/validacion_ci.py

def validar_cedula(ingreso_ci):
    # Variable booleana que almacenará el resultado si la cédula es válida o inválida
    validez_ci = False
    
    # Validación estructural: el ingreso debe ser un string de exactamente 10 dígitos numéricos
    if isinstance(ingreso_ci, str) and ingreso_ci.isdigit() and len(ingreso_ci) == 10:
        provincia = int(ingreso_ci[0:2])
        
        # Verificación del código de provincia de Ecuador (01 a 24 y 30)
        if 1 <= provincia <= 24 or provincia == 30:
            digito_verificador = int(ingreso_ci[9])
            suma = 0
            
            # Algoritmo de Módulo 10 para validación de cédulas ecuatorianas
            for i in range(9):
                valor = int(ingreso_ci[i])
                if i % 2 == 0:
                    valor *= 2
                    if valor > 9:
                        valor -= 9
                suma += valor
            
            decena_superior = (suma // 10 + 1) * 10 if suma % 10 != 0 else suma
            
            # Comparación final con el dígito verificador
            if (decena_superior - suma) == digito_verificador:
                validez_ci = True
                
=======
# backend/validaciones/validacion_ci.py

def validar_cedula(ingreso_ci):
    # Variable booleana que almacenará el resultado si la cédula es válida o inválida
    validez_ci = False
    
    # Validación estructural: el ingreso debe ser un string de exactamente 10 dígitos numéricos
    if isinstance(ingreso_ci, str) and ingreso_ci.isdigit() and len(ingreso_ci) == 10:
        provincia = int(ingreso_ci[0:2])
        
        # Verificación del código de provincia de Ecuador (01 a 24 y 30)
        if 1 <= provincia <= 24 or provincia == 30:
            digito_verificador = int(ingreso_ci[9])
            suma = 0
            
            # Algoritmo de Módulo 10 para validación de cédulas ecuatorianas
            for i in range(9):
                valor = int(ingreso_ci[i])
                if i % 2 == 0:
                    valor *= 2
                    if valor > 9:
                        valor -= 9
                suma += valor
            
            decena_superior = (suma // 10 + 1) * 10 if suma % 10 != 0 else suma
            
            # Comparación final con el dígito verificador
            if (decena_superior - suma) == digito_verificador:
                validez_ci = True
                
>>>>>>> 9be2433dd95145d28317e4ad2724d1b44587ea0d
    return validez_ci