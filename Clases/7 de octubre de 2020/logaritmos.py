'''PROGRAMACIÓN AVANZADA. 7 de octubre.
Tenemos dos variables
x=...
z=...
Queremos calcular log(x+y) y meterlo en x, sería, x=math.log(x+z)'''

'''#Tenemos lo siguiente
a=3
b=2
print((b>a) && (b==2))
#Puede ser que
#A) VERDADERO B) FALSO C) MAL ESCRITO D) FALTAN DATOS.
#Está mal escrito porque en Python el y lógico se escribe and.'''

a=3
b=2
print((b>a) and (b==2))

'''#Tenemos
y=1
j=2
for i in range(j,10,2): #Inicia en j, acaba en 10 y va de 2 en 2.
    if i==k:
        k=j
print(k)
¿Qué sale en pantalla? Sale 3.'''

y=1
j=2
k=3
for i in range(j,10,2):
    if i==k:
        k=j
print(k)

'''#Las listas de Python pueden tener elementos de tipos variados incluso listas.
i=[1,"techo",[2,4,6]]
#Podemos guardar en Python matrices como listas de listas de la siguiente forma
matriz=[[1,2,3],[4,5,6],[7,8,9]]
#Ahora queremos poner la diagonal a cero.
matriz[0][0]=0
matriz[1][1]=0
matriz[2][2]=0
#Lo podemos hacer con un bucle for y además de manera que tome el orden de la matriz.
for i in range(len(matriz)):
    matriz[i][i]=0
'''

'''#Tenemos unos datos que son una lista de números: 64 71 59 68 71 69... Valores entre
los que puede haber repeticiones. (Listas de pesos de personas.) Queremos saber
cuánta gente se repite.'''
