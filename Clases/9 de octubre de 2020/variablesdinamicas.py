# La función local() devuelve lo que está guardado en este momento en memoria.
locals()

x = 6
z = 26
print(locals())  # Pongo print porque al ser un script, no se imprime en pantalla.

locals()['y'] = 60  # Define una variable con nombre y y valor 60

texto = 'mmx'
valor = 33
locals()[texto] = valor
