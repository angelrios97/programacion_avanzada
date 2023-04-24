#PROGRAMACIÓN AVANZADA. 7 de octubre de 2020

fichero=open('pesos', 'r')
pesos=[]
for linea in fichero.readlines():
    pesos.append(int(linea.strip()))
#Equivalente: pesos=[int(linea.strip()) for linea in fichero.readlines()]
print(pesos)
cantidad=[0]*80
for i in range(20,100):
    cantidad[i-20]=pesos.count(i) #pesos.count(68) dice cuántas veces aparece 68 en la lista de pesos.

for i in range(20,100):
    print(i,cantidad[i-20])



