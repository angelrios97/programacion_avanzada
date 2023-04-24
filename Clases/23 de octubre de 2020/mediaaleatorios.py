from random import random

'''def mediaaleatorio(n,acum=0,k=1):
    acum=acum+random()
    media = acum/k
    yield media
    n -= 1
    k += 1
    if n != 0:
        yield from mediaaleatorio(n, acum, k)

print(list(mediaaleatorio(900)))'''

def gensumal(cantidadpedida,sumaprevia=0,nuevo=random(),cantidadprevia=0):
    yield (sumaprevia+nuevo)/(cantidadprevia+1)
    if cantidadpedida > cantidadprevia+1:
        yield from gensumal(cantidadpedida,sumaprevia+nuevo,random(),cantidadprevia+1)

print(list(gensumal(950)))