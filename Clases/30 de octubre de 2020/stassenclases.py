# Se introducen dos matrices como listas de listas y se calcula el producto
# siguendo el algoritmo de Strassen de multiplicación rápida de matrices. (Que es de orden n^(log_2(7)), más rápido asintóticamente
# que el algoritmo del instituto).

class Matriz:

    def __init__(self,*filas):
        self.filas = filas
        self.orden = len(filas)

    def __add__(self, matriz2):
        return Matriz([[self.filas[i][j]+matriz2.filas[i][j] for j in range(self.orden)] for i in range(self.orden)])

    def __get__(self):
        print(self.filas)

    def bloques(self):
        k = round(self.orden / 2)
        m1 = [[self.filas[i][j] for j in range(k)] for i in range(k)]  # Primer bloque
        m2 = [[self.filas[i][j] for j in range(k, self.orden)] for i in range(k)]  # Segundo bloque
        m3 = [[self.filas[i][j] for j in range(k)] for i in range(k, self.orden)]  # Tercer bloque
        m4 = [[self.filas[i][j] for j in range(k, self.orden)] for i in range(k, self.orden)]  # Cuarto bloque
        return [m1, m2, m3, m4]  # Retornamos los bloques en una lista

    def bloques2(self,matriz2):
        return [Matriz.bloques(self), Matriz.bloques(matriz2)]


from random import uniform

m = [[uniform(-100, 100) for i in range(10)] for j in range(10)]


# punto flotante en [-1000,1000)



def divide2(a,b):
    return [divide(a), divide(b)]
'''
s1 =
s2 =
s3 =
s4 =
s5 =
s6 =
s7 =
s8 =
s9 =
s10 ='''