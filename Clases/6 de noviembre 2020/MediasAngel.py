import numpy as np


def medias(valor):  # Retorna las medias de los números menores que valor y la de los mayores que valor.
    fichero = open('secuencia', 'r')  # Abrimos el fichero.
    numeros = np.array([int(x.strip()) for x in fichero.readlines()])  # Guardamos cada número en un array.
    media_menor = np.mean(numeros[numeros < valor])  # Calculamos la media
    media_mayor = np.mean(numeros[numeros > valor])  # Calculamos la media
    return media_menor, media_mayor  # Retornamos la media menor y la media mayor como una tupla.

print(medias(20))