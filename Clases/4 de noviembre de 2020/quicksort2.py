def quicksort2(lista, corte):
    if len(lista) <= 1:
        return list(lista)
    r = lista[-1]
    i = 0
    for j in range(len(lista)):
        if lista[j] < r:
            lista[i], lista[j] = lista[j], lista[i]
            i += 1
    lista[i], lista[j] = lista[j], lista[i]
    sublista1 = lista[:i]
    sublista2 = lista[i+1:]
    if len(sublista2) <= corte:
        return sublista1 + [lista[i]] + sublista2
    return quicksort2(sublista1, corte) + [lista[i]] + quicksort2(sublista2, corte)

p = [1, 2, 5, 4, 9, 3, 0, 7, 6]
k = quicksort2(p, 5)
print(k)