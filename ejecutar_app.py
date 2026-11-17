# ejecutar_app.py

import streamlit.web.cli as stcli
import sys
import threading
import time
import webbrowser
import os

def abrir_navegador():
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        directorio_raiz = os.path.dirname(sys.executable)
    else:
        directorio_raiz = os.path.dirname(os.path.abspath(__file__))
        
    # Bloqueo estricto del directorio de trabajo
    os.chdir(directorio_raiz)
    ruta_script_principal = os.path.join(directorio_raiz, "main.py")
    
    threading.Thread(target=abrir_navegador).start()
    
    sys.argv = ["streamlit", "run", ruta_script_principal, "--server.headless=True", "--global.developmentMode=false"]
    sys.exit(stcli.main())