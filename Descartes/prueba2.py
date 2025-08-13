from datetime import date
import os
import pandas as pd

hoy = str(date.today())
hoy  = hoy.replace("-", "_")
ruta = "data_engelyvoelkers/"+hoy+"/"
ruta_links = ruta + "Engelyvolkers_links.csv"
print(ruta_links)



# Genero el str del dia de ejecución
hoy = str(date.today())
hoy  = hoy.replace("-", "_")
ruta = "data_engelyvoelkers/"+hoy

#----------------------------------------------------------------------------------------------------------------
# Genero la carpeta de hoy
os.makedirs(ruta, exist_ok=True)

df_links = pd.DataFrame({"hola":[1], "adios":[2]})

ruta_links = ruta + "/prueba.csv"
df_links.to_csv(ruta_links, index=False, encoding="utf-8")