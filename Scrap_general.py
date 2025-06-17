import requests
from bs4 import BeautifulSoup
import re
import warnings
from itertools import chain, product
import pandas as pd
import os
from datetime import date

class Scraggy:
    def __init__(self):
        """
        elements_page: Todos los elements_page que añadamos en cualquier función deberá tener la siguiente forma:
        lista de elementos:
            string que indique que tipo de elemento buscamos
            diccionario que nos indique al tributo de este elemento
        """
        self.iterate = [""]

        self.dict_home = {}
        self.response_home = {}

        self.dict_articles = {}
        self.response_articles = {}
    #------------------------------------------------------------------------------------------------------------------------
    def create_dict(self, dictionary):
        """
        Genera un diccionario con las key del diccionario anterior y sus values serán listas vacias
        """
        return {key:[] for key in dictionary}
    #------------------------------------------------------------------------------------------------------------------------
    def iterator(self, dictionary):
        """
        Función para crear un iterador de las posibles paginas de una web

        Param
        -----
        dictionary

        Return
        ------
        iterable de todas las posibles combinaciones de paginas web"""

        result = [product([key], values) for key, values in dictionary.items()]
        result = list(chain.from_iterable(result))
        self.iterate = result
    #------------------------------------------------------------------------------------------------------------------------
    def filtro(self, dict_filtros, saved_tag):
        """
        Función determinada para que se guarden el diccionario el lugar donde se guardará el tag
        """
        def filtro_tags(tag):
            """
            Función que lee el DOM una vez y extrae las etiquetas deseadas
            """
            for key, values in dict_filtros.items():
                if tag.name == values[0]:
                    tag_values = " ".join(tag.get(values[1], []))
                    if tag_values == values[2]:
                        saved_tag[key].append(tag)
                        if not(values[3] == "all"):
                            del dict_filtros[key]
                        return tag
        return filtro_tags
    #------------------------------------------------------------------------------------------------------------------------
    def read_home(self, link_home, iterate, page_elements):
        """ 
        Función para sacar los articulos de la página principal
    
        Parametros
        ----------
        link_home: string del link de la pagina principal.
        iterate: Objeto iterable donde de todas las páginas principales
        page_elements: diccionario de los page elements que vamos a buscar y sus usos
            "link_article": link del articulo 
            "price_article": precio del articulo
            "place_article": lugar de venta
            "no_result": page element que indica que esta pagina no tiene elementos
            "actual_page": pagina actual
    
        Devuelve
        --------
        Una lista con información de todos los articulos en forma de set
            El set contiene:
                link al anuncion
                precio del anuncio
    
        """


        links = []
        iterate = self.iterate[:]
        for name_page in iterate:
            num_page = 1
            
            while True:
                url = link_home.format(name_page[0], name_page[1], num_page)
                
                # Obtener el HTML de la página
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Apartado en caso de que la página no tenga resultado
                response_no_result = soup.find_all(page_elements["no_result"][0], attrs=page_elements["no_result"][1])
                if response_no_result:
                    self.iterate.remove(name_page)
                    break

                
                self.filtro(self.dict_home, self.response_home)
                    

                


    #------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------------------------------------------
    # Funcion para convertir los textos en numero
    def text_to_num(self, text, dec_sep=None, mil_sep="."):

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
    
    #------------------------------------------------------------------------------------


filtro_home = filtro(dict_filtros, saved_tag)
resultados = soup.find_all(filtro_home)