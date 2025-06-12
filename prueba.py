import re

texto = "12.342.232,312 $$$"

# Extraer el número con puntos y coma
match = re.search(r'[\d\.]+,\d+', texto)

print(match)
if match:
    num_str = match.group(0)
    print(num_str)
    # Quitar puntos y cambiar coma por punto
    num_float = float(num_str.replace('.', '').replace(',', '.'))
    print(num_float)