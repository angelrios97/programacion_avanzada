# Multiplica matrices guardadas por filas como listas de listas mediante el algoritmo divide y vencerás de
# Strassen. Por esta programación del algoritmo y suponiendo que no hay errores de entrada, si una matriz no es una
# lista, siempre será un número.

from random import seed, uniform
from functools import reduce
from itertools import islice

seed(0.7730284088535233)  # Fijamos una semilla para la generación de matrices pseudoaleatorias. La semilla ha sido
# generada pseudoaleatoriamente en consola mediante random del paquete random. Se usará solo para hacer pruebas.


# Definimos una colección de funciones previas necesarias.


def bloques(matriz):  # Recibe una matriz de orden no 1 potencia de 2 y devuelve sus cuatro bloques.
    if len(matriz) == 2:  # Si la matriz es de orden 2, devolvemos los cuatro números como una lista.
        return [matriz[0][0], matriz[0][1], matriz[1][0], matriz[1][1]]

    orden = len(matriz)
    corte = len(matriz) // 2  # Como el orden es siempre par, la división es entera.
    m1 = [[matriz[i][j] for j in range(corte)] for i in range(corte)]  # Primer bloque
    m2 = [[matriz[i][j] for j in range(corte, orden)] for i in range(corte)]  # Segundo bloque
    m3 = [[matriz[i][j] for j in range(corte)] for i in range(corte, orden)]  # Tercer bloque
    m4 = [[matriz[i][j] for j in range(corte, orden)] for i in range(corte, orden)]  # Cuarto bloque
    return [m1, m2, m3, m4]  # Retornamos los bloques en una lista


def suma(matriz, matriz2):  # Calcula la suma de matrices pasadas como listas de listas.
    if type(matriz) != list:  # Si matriz es es un número, matriz2 también y retornamos la suma.
        return matriz + matriz2
    orden = len(matriz)  # Si las matrices no son números, devolvemos la suma habitual coordenada a coordenada.
    return [[matriz[i][j] + matriz2[i][j] for j in range(orden)] for i in range(orden)]


def opuesta(matriz):  # Devuelve la opuesta de la matriz.
    if type(matriz) != list:  # Si la matriz es un número, devolvemos el opuesto.
        return -matriz
    orden = len(matriz)  # Si la matriz no es un número, devolvemos el opuesto coordenada a coordenada.
    return [[-matriz[i][j] for j in range(orden)] for i in range(orden)]


# Programamos el método de Strassen original para matrices cuadradas de orden una potencia de 2.

def strassen_inicial(matriz, matriz2):  # Calcula el producto de dos matrices cuadradas de orden potencia de 2
    # mediante el algoritmo de Strassen.
    if type(matriz) != list:  # Si las matrices son números, es la última división del algoritmo de Strassen en la
        # que el cálculo se ha reducido a un producto de números.
        return matriz * matriz2
    # Dividimos cada matriz en sus cuatro bloques.
    a11, a12, a21, a22 = bloques(matriz)
    b11, b12, b21, b22 = bloques(matriz2)
    # Calculamos las sumas del algoritmo de Strassen.
    s1 = suma(b12, opuesta(b22))
    s2 = suma(a11, a12)
    s3 = suma(a21, a22)
    s4 = suma(b21, opuesta(b11))
    s5 = suma(a11, a22)
    s6 = suma(b11, b22)
    s7 = suma(a12, opuesta(a22))
    s8 = suma(b21, b22)
    s9 = suma(a11, opuesta(a21))
    s10 = suma(b11, b12)
    # Calculamos los productos necesarios recursivamente llamando de nuevo al algoritmo de Strassen.
    p1 = strassen_inicial(a11, s1)
    p2 = strassen_inicial(s2, b22)
    p3 = strassen_inicial(s3, b11)
    p4 = strassen_inicial(a22, s4)
    p5 = strassen_inicial(s5, s6)
    p6 = strassen_inicial(s7, s8)
    p7 = strassen_inicial(s9, s10)
    # Calculamos los bloques principales del resultado.
    c11 = reduce(suma, [p5, p4, opuesta(p2), p6])
    c12 = suma(p1, p2)
    c21 = suma(p3, p4)
    c22 = reduce(suma, [p5, p1, opuesta(p3), opuesta(p7)])
    if type(c11) != list:  # Si c11 es un número, es porque la matriz era de orden 2, la función bloques ha devuelto los
        # números en una lista. Los ponemos en forma de matriz para poder seguir hacia atrás reconstruyendo.
        return [[c11, c12], [c21, c22]]
    mitad_superior = [c11[i] + c12[i] for i in range(len(c11))]  # Reconstruimos las dos primeras filas del resultado.
    mitad_inferior = [c21[i] + c22[i] for i in range(len(c11))]  # Reconstruimos las dos últimas filas del resultado.
    return mitad_superior + mitad_inferior  # Retornamos la matriz resultado compuesta por los cuatro bloques.


# Las siguientes funciones permiten generalizar la función anterior para pares de funciones multiplicables de
# dimensiones cualesquiera.

def restos2(numero):  # Generador que devuelve una lista de ceros solo si el número pasado es potencia de 2.
    cociente = numero // 2
    resto = numero % 2
    if resto == 0:  # Si el resto de la división es 2,
        yield 0  # generamos 0
        if cociente == 2:  # Si el cociente es 2, todos los restos han sido 2,
            yield 0  # generamos 0 y terminamos.
        else:  # Si el cociente no es 0, seguimos generando a partir del cociente.
            yield from restos2(cociente)
    else:  # Si el resto no es 0, el número no es potencia de 2, generamos 1 y terminamos.
        yield 1


def siguientepotencia2(numero):  # Calcula la siguiente potencia de 2 de un número dado.
    if 1 not in restos2(numero):  # Si 1 no está en los restos del número, ya es potencia de 2.
        return numero
    else:
        while 1 in restos2(numero):  # Sumamos uno mientras 1 no sea potencia de 2.
            numero = numero + 1
        return numero  # Devolvemos la primera potencia de 2 calculada.


def strassen(matriz, matriz2):  # Generaliza el método de Strassen a matrices multiplicables cualesquiera
    # añadiendo y eliminando ceros.
    # Calculamos las dimensiones de las matrices a multiplicar.
    filam = len(matriz)
    filam2 = len(matriz2)
    columnam = len(matriz[0])  # Notar que debe ser filam2 == columnam para que sean multiplicables. Lo suponemos
    # cierto y que no hay errores de entrada.
    columnam2 = len(matriz2[0])
    dimensiones = [filam, filam2, columnam, columnam2]
    orden = siguientepotencia2(max(dimensiones))  # El nuevo orden de las matrices es la siguiente potencia de 2 de
    # la mayor de las dimensiones.
    diferencias = list(map(lambda x: orden - x, dimensiones))  # Calculamos el número de ceros que tenemos que añadir
    # en cada dimensión. Notamos de nuevo que diferencias[1] == diferencias[2]
    # Rellenamos con ceros.
    matriznueva = []
    for fila in matriz:
        fila.extend([0] * diferencias[2])  # Rellenamos las filas con ceros hasta la potencia de 2.
        matriznueva.append(fila)
    matriz = matriznueva
    matriz = matriz + [[0] * orden] * diferencias[0]  # Rellenamos con filas de ceros hasta la potencia de 2.
    matriz2nueva = []
    for fila in matriz2:
        fila.extend([0] * diferencias[3])  # Rellenamos las filas con ceros hasta la potencia de 2.
        matriz2nueva.append(fila)
    matriz2 = matriz2nueva
    matriz2 = matriz2 + [[0] * orden] * diferencias[1]  # Rellenamos con filas de ceros hasta la potencia de 2.

    previo = strassen_inicial(matriz, matriz2)  # Podemos calcular el producto con el algoritmo de Strassen para
    # matrices cuadradas de orden potencia de 2.
    # Ahora tenemos que eliminar los ceros que añadimos.
    resultado = []
    for fila in previo:
        fila = list(islice(fila, columnam2))  # Eliminamos los ceros añadidos de las filas
        resultado.append(fila)
    resultado = list(islice(resultado, filam))  # Eliminamos las filas de ceros añadidas.
    return resultado


# Para hacer pruebas, hemos programado también el producto habitual de matrices.
def producto(matriz, matriz2):  # Devuelve el producto de matrices calculado con el algoritmo por definición.
    if type(matriz) != list:
        return matriz * matriz2
    orden = len(matriz)
    return [[sum([matriz[i][k] * matriz2[k][j] for k in range(orden)]) for j in range(orden)] for i in range(orden)]


# Probamos la función strassen para matrices de orden potencia de 2, por ejemplo, de orden 64.
CUAD_MATRIZ = [[uniform(-100, 100) for j1 in range(64)] for i1 in range(64)]
CUAD_MATRIZ2 = [[uniform(-100, 100) for j2 in range(64)] for i2 in range(64)]

print(CUAD_MATRIZ)
print(CUAD_MATRIZ2)
print(strassen_inicial(CUAD_MATRIZ, CUAD_MATRIZ2))
print(producto(CUAD_MATRIZ, CUAD_MATRIZ2))
print('')

# Probamos la función strassen generalizada para matrices de dimensiones generales y entradas punto flotante.
MATRIZ = [[uniform(-1000, 1000) for j3 in range(7)] for i3 in range(10)]
MATRIZ2 = [[uniform(-1000, 1000) for i4 in range(10)] for j4 in range(12)]

print(MATRIZ)
print(MATRIZ2)
print(strassen(MATRIZ, MATRIZ2))
print(producto(MATRIZ, MATRIZ2))
