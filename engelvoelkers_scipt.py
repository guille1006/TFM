import requests
from bs4 import BeautifulSoup
import re
import warnings
from itertools import chain
import pandas as pd


# Funcion para convertir los textos en numero
def text_to_num(text, dec_sep=None, mil_sep="."):

    if (type(text)==int) or (type(text)==float):
        return text
    if (type(text)==bool):
        return int(text)
    
    # Primero quitaré los separadores de millares
    # Es posible que por equivocación se use el mismo dec_sep que mil_sep, por ello se cambiará mil_sep
    if dec_sep == mil_sep:
        change_sep = {".":",", ",":"."}
        mil_sep = change_sep[dec_sep]
        warnings.warn(f"Using same decimal separator as mil separator, mil_sep will be {change_sep[dec_sep]}")

    text = text.replace(mil_sep, "")


    if not dec_sep:
        numeros = re.findall(r'\d+', text)
        numero = int("".join(numeros))

    else: 
        if not dec_sep:
            raise ValueError("Error: Introduce un separador decimal para la variable [dec_sep]")
        else:
            match = re.search(fr'\d+{re.escape(dec_sep)}\d+', text)
            if match:
                num_str = match.group(0)
                if dec_sep == ",":
                    num_str = num_str.replace(",", ".")
                numero = float(num_str)

    
    return numero

# --------------------------------------------------------------------------------------------
# Funcion para leer cada pagina de cada casa
def read_link(link, location):
    url = link
     # Obtener el HTML de la página
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    v_independ = {
            "link": link,
            "title": None,
            "coment": None,
            "price": 0,
            "location": location,
            "num_photos": 0,
            "property_type": None,
            "condition": None,
            "num_rooms": 0,
            "num_bedrooms":0,
            "num_baths":0,
            "floor_number": 0,
            "garage": False,
            "total_surf":0,
            "living_surf":0,
            "usable_area":0,
            "floor_type": None,
            "construc_year":1900,
            "energy_cert_avail": False,
            "heating": None,
            "others": None
        }

    # num_photos
    button = soup.find('button', {'aria-label': 'Galería'})
    if button:
        num_photos = button.find('span').text.strip()
        num_photos = int(num_photos.split("/")[-1])
        v_independ["num_photos"] = num_photos

    # title
    titulo = soup.find('h1', {'data-test-id': 'expose-headline'})
    if titulo:
        titulo = titulo.text.strip()
        v_independ["title"] = titulo

    # price
    precio = soup.find('span', {'data-test-id': 'expose-price-value'})
    if precio:
        precio = precio.text.strip()
        precio = text_to_num(precio)
        v_independ["price"] = precio


    diccionario = {
            "property_type": ["propiedad"],
            "condition": ["Condic"],
            "num_rooms": ["Habitaciones"],
            "num_bedrooms": ["Dormitorios"],
            "num_baths": ["Baños"],
            "floor_number": ["Piso"],
            "garage": ["Garaje"],
            "total_surf": ["total"],
            "living_surf": ["habitable"],
            "usable_area": ["utilizable"],
            "floor_type": ["Suelo"],
            "construc_year": ["Año", "construcción"],
            "energy_cert_avail": ["Certificado"],
            "heating": ["Fuente"]
        }


    # Caracteristicas
    caracteristicas = soup.find("div", {"data-test-id":"expose-property-features"})
    if caracteristicas:
        caracteristicas = caracteristicas.find_all("span", class_="sc-4100f4c3-0 bncvQi sc-2f04d979-2 lgHRew")
        list_caracteristicas = {text.get_text() for text in caracteristicas}
        for carac in list(list_caracteristicas):
            if carac in chain.from_iterable(list(diccionario.values())):
                list_caracteristicas.remove(carac)
    
        v_independ["others"] = list_caracteristicas

        

    # key_info
    key_info = soup.find("div", {"data-test-id": "property-details"})
    if key_info:
        key_info = key_info.find_all('li')
        if key_info:
            for li in key_info:
                text = li.get_text(strip=True, separator="/")
                text = text.split("/")
                
            
                break_ = False
                for key, values in diccionario.items():
                    for value in values:
                        if value in text[0]:
                            v_independ[key] = text[1]
                            del diccionario[key]
                            break_ = True
                            break
            
                    if break_:
                        break

    # comentario
    comentario = soup.find('div', {'data-test-id': 'expose-property-description'})
    if comentario:
        comentario = comentario.find('p').text.strip()
        diccionario["coment"] = comentario

    # Reacondicioando de las variables numericas
    numericas = ["num_rooms", "num_bedrooms", "num_baths", "floor_number", "garage", "total_surf", "living_surf", "usable_area", "construc_year"]
    for num in numericas:
        v_independ[num] = text_to_num(v_independ[num])


    return v_independ

#---------------------------------------------------------------------------------------------------------------------------------
# Esto es solo para sacar los enlaces de cada articulo, y sus respectivos precios
num_max_pag = 2
links = []
for num_pagina in range(num_max_pag):
    url = f"https://www.engelvoelkers.com/es/es/inmuebles/res/compra/inmobiliario?businessArea[]=residential&currency=EUR&measurementSystem=metric&page={num_pagina}&placeId=ChIJi7xhMnjjQgwR7KNoB5Qs7KY&propertyMarketingType[]=sale&sortingOptions[]=PUBLISHED_AT_DESC&placeName=Espa%C3%B1a"
    # Obtener el HTML de la página
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar todos los <a> con href que contenga "/es/es/exposes/"
    articulos_pag = soup.find_all('article', attrs={"data-test-id":lambda x: x and x.startswith("search-components_result-card")})

    for articulo in articulos_pag:
        # Sacar el link
        enlace = articulo.find_all("a", href=True)
        link = enlace[0]["href"]

        # Sacar el precio
        price = articulo.find("p", {"data-test-id": "search-components_result-card_price"})
        if not price:
            warnings.warn(f"El articulo siguiente no tiene precio:{articulo} ")
        price = price.text.strip()
        price = text_to_num(price)

        # Sacar el lugar
        place = articulo.find("p", {"data-test-id": "search-components_result-card_location"}).text.strip()


        links.append([link, price, place])

#--------------------------------------------------------------------------------------------------------------------------------------
# Ahora itero sobre todos los links que tenemos
lectura = []

for link in links:
    url = f"https://www.engelvoelkers.com{link[0]}"
    readed_link = read_link(url, link[2])
    lectura.append(readed_link)

#----------------------------------------------------------------------------------------------------------------------------------------
# Guardo los datos de la request a las paginas principales
encabezados = ["link", "precio", "lugar"]
df_links = pd.DataFrame(links, columns=encabezados)
df_links.to_csv("Engelyvolkers_links.csv", index=False, encoding="utf-8")

#----------------------------------------------------------------------------------------------------------------------------------------
# Guardo los datos de todas las paginas
df_lectura = pd.Dataframe(lectura)
df_links.to_csv("Engelyvolkers_lectura.csv", index=False, encoding="utf-8")