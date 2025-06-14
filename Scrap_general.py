import requests
from bs4 import BeautifulSoup
import re
import warnings
from itertools import chain
import pandas as pd
import os
from datetime import date

class Scraggy:
    def __init__(self, link_home, ):
        pass



    #----------------------------------------------------------------------------------------------
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
    