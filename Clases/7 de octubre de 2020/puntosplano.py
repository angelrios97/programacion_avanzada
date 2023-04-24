#PROGRAMACIÓN AVANZADA. 7 de octubre de 2020
#Se le pasan unos puntos en el plano desde fichero y un punto de referencia por teclado.
#El programa calcula la el punto a distancia mínimda de la referencia y devueve los puntos que se
#encuentran en a radio menor que el doble de esa distancia.

from math import sqrt

fichero=open('puntos', 'r')
zx=float(input("Introduce la coordenada x del punto de referencia: "))
zy=float(input("Introduce la coordenada y del punto de referencia: "))
coorx=[]
coory=[]
for linea in fichero.readlines():
    coorx.append(float(linea.split()[0])) #linea.split() divide los datos separados por espacios
    coory.append(float(linea.split()[1]))
print(coorx)
print(coory)

distancias=[]
for i in range(len(coorx)):
    distancias.append(sqrt((coorx[i]-zx)**2+(coory[i]-zy)**2))
print(distancias)
minimo=min(distancias) #min(distancias) calcula el mínimo de las distancias
radio=minimo*2

resultado=[]
for i in range(len(distancias)):
    if distancias[i]<=radio:
        resultado.append([coorx[i],coory[i]])
print(resultado)
