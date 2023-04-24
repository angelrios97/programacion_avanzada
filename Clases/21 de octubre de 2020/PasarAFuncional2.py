from random import random


def mover():
    for i, _ in enumerate(posiciones):
        if random() > 0.3:
            posiciones[i] += 1


def muestracoche(poscoche):
    print('-' * poscoche)


def avanza():
    global pasos
    pasos -= 1
    mover()


def muestra():
    print('')
    for poscoche in posiciones:
        muestracoche(poscoche)


pasos = 5
posiciones = [1, 1, 1]


while pasos:
    avanza()
    muestra()
