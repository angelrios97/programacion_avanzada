import functools
#Se le pasa una lista de tuplas y se hace un hash sobre la segunda lista.

nombres = ['Anastasio', 'Buenaventura', 'Clodovea']
claves = ['adfdfsd', 'eije32o3nrwk', 'kfaksa2']

lista = list(zip(nombres, claves))


def hash2(lista):
    p = list(map(hash, lista))
    return p[1]
