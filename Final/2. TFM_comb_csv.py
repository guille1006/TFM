import numpy as np
import pandas as pd
import re
from io import StringIO

import requests

# URLs base
repo_html_url = "https://github.com/guille1006/TFM/tree/main/data2/datos_separados"
raw_base = "https://raw.githubusercontent.com/guille1006/TFM/main/Idealista/datos/"                     # Link datos Agosto
raw_base = "https://raw.githubusercontent.com/guille1006/TFM/refs/heads/main/data2/datos_separados/"    # Link datos Septiembre

# Obtener lista de archivos
html = requests.get(repo_html_url).text
csv_files = re.findall(r'datos_sec_pag_\d+\.csv', html)
csv_files = [(int(file.split('_')[3].split('.')[0]), file) for file in set(csv_files)]
csv_files = sorted(csv_files, key=lambda x: x[0])

print(f"Archivos encontrados: {len(csv_files)}")


# Al haber automatizado la obtención de datos, hay algunos .csv que están vacíos
dataframes = dict()
errores = []

for num_page, file in csv_files:
    file_url = raw_base + file

    # Descargaremos toda la información dentro de cada enlace para ver que tiene
    resp = requests.get(file_url)
    content = resp.text.strip()

    # Puede ser que no tengan contenido debido a que se acabaron el tipo de viviendas para el filtro usado
    if not content:
        errores.append((num_page, "Archivo vacío"))
        continue

    # Usaremos StringIO para poder pasar el contenido a un dataframe de pandas
    df = pd.read_csv(StringIO(content))

    # Por motivos de eficiencia de tiempo, hemos decidido ir guardando todos los df en una lista
    # que luego usaremos para concatenar todos ellos
    dataframes[num_page] = df

# Vamos a ordenar el set de all_columns y guardarlo como una lista
dfs = list(dataframes.values())

raw_data = pd.concat(dfs, ignore_index=True, sort=True)

# Tambien eliminaremos las filas duplicadas
initial_rows = raw_data.shape[0]
raw_data = raw_data.drop_duplicates()
final_rows = raw_data.shape[0]

print(f"Teniamos un total de {final_rows-initial_rows} duplicadas")

# Guardamos el DataFrame como un csv
raw_data.to_csv("data2/raw_data.csv", index=False)

#------------------------------------------------------------------------------------------
# Unión de los datos de Agosto con Septiembre

url_1 = "https://raw.githubusercontent.com/guille1006/TFM/refs/heads/main/data/raw_data.csv"    # Datos Agosto
url_2 = "https://raw.githubusercontent.com/guille1006/TFM/refs/heads/main/data2/raw_data.csv"   # Datos Septiembre
df_1 = pd.read_csv(url_1)
df_2 = pd.read_csv(url_2)

# Concatenamos todos los DataFrames
total_data = pd.concat([df_1, df_2], ignore_index=True, sort=True)

# También eliminaremos las filas duplicadas
initial_rows = total_data.shape[0]
total_data = total_data.drop_duplicates()
final_rows = total_data.shape[0]

print(f"Teníamos un total de {initial_rows-final_rows} duplicadas")
print(f"Y tenemos todas estas filas finales {final_rows}")

# Finalmente guardamos todos los datos en un csv
total_data.to_csv("data2/total_data.csv", index=False)