#PROGRAMACIÓN AVANZADA. 7 de octubre de 2020
from math import log2

fichero=open('frecuencias', 'r')
fabsolutas=[]
for linea in fichero.readlines():
    fabsolutas.append(int(linea.strip()))
print(fabsolutas)
frel=[i/sum(fabsolutas) for i in fabsolutas]
print(frel)
Htotal=sum([fi*log2(fi) for fi in frel])
print(Htotal)
fabscopia=fabsolutas.copy()
entropias=[]
for i in range(len(fabsolutas)): #DICEN QUE SON NECESARIAS LISTAS DE LISTAS, PERO YO NO VEO POR QUÉ.
    fabscopia.pop(i)
    entropias.append(sum([Htotal-fi*log2(fi)/sum(fabsolutas) for fi in fabscopia]))
    fabscopia=fabsolutas.copy()
print(entropias)