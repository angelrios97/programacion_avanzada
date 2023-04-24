# -*- coding: utf-8 -*-
import itertools

# Escribe en el fichero "parte1" las líneas del fichero "todo" contenidas entre el primer par de líneas
# de tres asteriscos "***". Suponemos que el fichero "todo" siempre contiene al menos dos líneas "***".


def escribe(fichsal, itdatos):  # Si no se captura ninguna excepción, escribe las líneas de itdatos en fichsal.
    try:
        fichsal.writelines(next(itdatos))
    except:
        fichsal.close()
        return
    escribe(fichsal, itdatos)

# Tupla auxiliar que contiene todas las líneas del fichero desde la primera línea "***" hasta el final.
auxiliar = tuple(itertools.dropwhile(lambda x: x != '***\n', open('todo', 'r')))
# Tupla auxiliar eliminando la primera línea que es exactamente "***".
auxiliar2 = tuple(itertools.islice(auxiliar, 1, len(tuple(auxiliar))))
# Generador que contene por orden las líneas entre los primeras líneas "***".
lee = itertools.takewhile(lambda x: x != '***\n', auxiliar2)
escribe(open('parte1', 'w'), lee)  # Escribimos las líneas en el fichero "parte1" que, si no existe, se crea.
