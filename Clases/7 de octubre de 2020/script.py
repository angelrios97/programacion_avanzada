#PROGRAMACIÓN AVANZADA. 7 de octubre de 2020
#Tomamos la siguiente lista
numeros=[3,5,8,11]

#Podemos cambiar la lista con un for.
for i in range(10):
    numeros[i]=i*i

#List comprehension es una idea diferente para hacer lo mismo.
numeros=[i*i for i in range(10)]

todos=[17,18,19,21,25,32] #otra lista cualquiera
#A veces, se puede construir una lista a partir de otra.
for i in range(10):
    if todos[i]%3==0:
        numeros.append(i*i)

#El equivalente por comprensión sería
numeros=[i*i for range(10) if todos[i]%3==0] #Esta lista por comprensión está un poco al límite.
# Se podría hacer más larga, pero si es muy complejo, estilísticamente es mejor desarrollarlo.
#Siempre se tiene como alternativa desarrollarlo.



