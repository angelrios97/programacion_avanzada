# -*- coding: utf-8 -*-
import operator
from random import random
from itertools import islice


# Simula una carrera de coches aleatoria mediante programación funcional imprimiendo el avance de los coches en
# pantalla con guiones.


def mover(posiciones):  # Calcula de manera aleatoria los coches que avanzan y devuelve las nuevas posiciones.
    def cambiaprob(x):  # Si el número que se le pasa es mayor que 0.3, retorna 1 y en caso contrario, retorna cero.
        if x > 0.3:
            return 1
        else:
            return 0

    aleatorios = tuple(map(cambiaprob, map(lambda x: random(), range(len(posiciones)))))  # Para cada coche, se
    # calcula un número pseudoaleatorio con distribución uniforme en [0,1) y solo si es mayor que 0,3, el coche avanza.
    return tuple(
        map(operator.add, aleatorios, posiciones))  # Modifica las posiciones sumando 1 si avanza y 0 si no avanza.


def muestra(posiciones):  # Dada una posición fija de los coches, la muestra mediante guiones.
    print('-' * posiciones[0])  # Imprime tantos guiones como posiciones ha avanzado el primer coche de la tupla.
    if len(posiciones) > 1:  # Si quedan más coches,
        posiciones = tuple(islice(posiciones, 1, len(posiciones)))  # Elimina el primer coche de la tupla.
        muestra(posiciones)  # Muestra la posición del primer coche de la tupla.


def carrera(posiciones, pasos):  # Ejecuta la simulación
    print('')  # Separa con una línea en blanco cada paso de la carrera.
    muestra(posiciones)  # Muestra la situación actual de la carrera en ese paso.
    posiciones = mover(posiciones)  # Calcula aleatoriamente las nuevas posiciones.
    if pasos - 1 > 0:  # Si quedan más pasos, se repite recursivamente.
        carrera(posiciones, pasos - 1)


carrera((1, 1, 1), 5)
