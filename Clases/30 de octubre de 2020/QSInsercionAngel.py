def quicksort5(lista):  # Devuelve el resultado del algoritmo quicksort hasta que la lista final tiene longitud 5.
    if len(lista) <= 1:  # Si la lista tiene un solo elemento o es vacía, la retornamos.
        return list(lista)
    r = lista[-1]  # Consideramos el último elemento.
    i = 0
    for j in range(len(lista)):  # Vamos aumentando j uno en cada paso.
        if lista[j] < r:  # Si el elemento en j es menor que el último, los intercambiamos y aumentamos i.
            lista[i], lista[j] = lista[j], lista[i]
            i += 1
    lista[i], lista[j] = lista[j], lista[i]  # Haccemos un último cambio de los elementos en i y en j.
    sublista1 = lista[:i]  # Consdieramos las dos partes de la lista generada.
    sublista2 = lista[i+1:]
    if len(sublista2) == 5:  # Cuando la segunda lista tenga tamaño 5, retornamos la lista tal cual.
        return sublista1 + [lista[i]] + sublista2
    return quicksort5(sublista1) + [lista[i]] + quicksort5(sublista2)  # Cuando tenga tamaño mayor, recursión.

                
def insercion(lista):  # Devuelve la lista que se le pasa ordenada mediante el algorítmo de inserción.
    for i in range(1, len(lista)):  # Para cada elemento de la lista a partir del segundo.
        for j in range(0, i):  # Para cada elemento anterior.
            if lista[i] < lista[j]:  # Si es mayor, los intercambiamos.
                lista[i], lista[j] = lista[j], lista[i]
    return lista


def quicksort_insercion(lista):  # Se le pasa una lista numérica y la devuelve ordenada aplicando quicksort
    # hasta que la lista tiene tamaño 5 y seguidamente el algoritmo de inserción.
    return insercion(quicksort5(lista))
