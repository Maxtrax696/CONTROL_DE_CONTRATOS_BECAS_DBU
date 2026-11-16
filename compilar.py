# compilar.py

import PyInstaller.__main__
import shutil
import os
import streamlit

# 1. Destrucción de caché corrupto de compilaciones anteriores
for carpeta in ['build', 'dist']:
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)
if os.path.exists('Control_de_Contratos_Becas_DBU.spec'):
    os.remove('Control_de_Contratos_Becas_DBU.spec')

# 2. Resolución algorítmica de la ruta estática del framework
ruta_streamlit = os.path.dirname(streamlit.__file__)

# 3. Determinación dinámica del separador del sistema operativo (Linux/Mac = ':' , Windows = ';')
separador = os.pathsep

# 4. Compilación con inyección forzada de assets
PyInstaller.__main__.run([
    'ejecutar_app.py',
    '--onefile',
    '--windowed',
    '--icon=icono.ico',
    '--name=Control_de_Contratos_Becas_DBU',
    '--copy-metadata=streamlit',
    '--collect-all=streamlit',
    f'--add-data={ruta_streamlit}{separador}streamlit'
])