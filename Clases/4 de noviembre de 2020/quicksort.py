p = [1, 2, 4, 5, 9, 3, 0, 7, 6]

def quicksort(lista):
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
    return quicksort(sublista1) + [lista[i]] + quicksort(sublista2)

print(quicksort(p))