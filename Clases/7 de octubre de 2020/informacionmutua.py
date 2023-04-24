#PROGRAMACIÓN AVANZADA. 7 de octubre de 2020

from math import log2
fichero=open('frecuencias', 'r')
lineas=fichero.readlines()
frecuencias=[]
for i in range(len(lineas)):
    frecuencias.append(lineas[i].strip().split(' ,'))
for i in range(len(frecuencias)):
    frecuencias[i]=frecuencias[i][0].strip().split(',')
    frecuencias[i]=[(frecuencias[i][j]) for j in range(len(frecuencias[i]))]
total=sum([len(frecuencias[i]) for i in range(len(frecuencias))])
def frecuencia_relativa(n):
    return sum([frecuencias[i].count(n) for i in range(len(frecuencias))])/total
# h0=sum([frecuencia_relativa(i)*log2(frecuencia_relativa(i)) for i in range(len(frecuencias[0]))])
# print(h0)
for i in range(len(frecuencias[5])):
    print(frecuencia_relativa(i))
print(frecuencias)
