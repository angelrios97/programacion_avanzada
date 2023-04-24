import itertools
import operator

numeros = range(10,21)
simetrico = range(20,9,-1)

lista = map(operator.mul,numeros,simetrico)
print(list(lista))

