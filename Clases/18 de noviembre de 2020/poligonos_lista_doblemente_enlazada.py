from copy import deepcopy
from math import sqrt


class ListaDoblementeEnlazada:
    """Clase cuyos objetos son listas doblemente enlazadas. Una lista doblemente enlazada consiste en elementos.
    Los elementos contienen su valor, otro elemento como enlace, que es el siguiente en la lista, y otro como referencia
    anterior, que es el anterior en la lista.. De esta manera tenemos una estructura en memoria de referencias de cada
    elemento a sus contiguos.
    :ivar primero: Primer elemento de la lista.
    :ivar ultimo: Último elemento de la lista. (Solamente es necesario para definir los métodos de inserción.)
    :ivar actual: Auxiliar que permite hacer que las instancias sean iterables."""

    class Elemento:
        """Subclase de ListaEnlazada cuyos objetos son los elementos que estructuran las listas enlazadas. Consisten en
        un valor, un enlace que es otro objeto elemento y una referencia al anterior que también es otro objeto de tipo
        elemento.
        :ivar valor: Valor del elemento.
        :ivar enlace: Objeto de la clase elemento que es el siguiente en la lista enlazada.
        :ivar refanterior: """

        def __init__(self, valor,
                     enlace, refanterior):  # Constructor de Elemento que inicializa el valor, el enlace y su anterior.
            self.valor = valor
            self.enlace = enlace
            self.refanterior = refanterior

    def __init__(self):  # Constructor de ListaDoblementeEnlazada que inicializa una lista enlazada vacía.
        self.primero = None
        self.ultimo = None
        self.actual = None  # Servirá para hacer iterables los objetos de la clase.

    def __add__(self, lista2):  # Operador suma que devuelve la concatenación de dos listas enlazadas.
        resultado = deepcopy(self)  # Usamos deepcopy() para que el operador no modifique self.
        lista2.primero.refanterior = resultado.ultimo
        resultado.ultimo.enlace = lista2.primero  # El enlace del último es el primero de la segunda lista enlazada.
        resultado.ultimo = lista2.ultimo
        return resultado

    def __iter__(self):
        self.actual = self.Elemento(None, self.primero, None)  # Inicializamos el elemento actual como un elemento
        # auxiliar cuyo enlace es el primero para poder iterar sobre este y avanzar.
        return self

    def __next__(self):
        if self.primero is None:  # Si la lista enlazada es vacía, no retornamos nada.
            raise StopIteration
        if self.actual.enlace is not None:  # Si el elemento actual tiene siguiente, lo retornamos.
            self.actual = self.actual.enlace  # En particular, estamos retornando de forma correcta el primer elemento.
            return self.actual
        else:  # Si el elemento actual no tiene siguiente, paramos de iterar.
            raise StopIteration

    def __len__(self):  # Calcula de manera funcional la longitud de la lista enlazada.
        return len(list(enumerate(self)))  # Como self es un iterable, se puede convertir en enumerate, que se puede
        # convertir en lista, a la que se le puede aplicar su función len().

    def insertar(self, elemento, anterior):  # Inserta un único elemento detrás de otro que se le pasa como anterior.
        elemento.enlace = None  # El enlace del elemento es vacío en la mayoría de casos y si no, cambia su valor.
        elemento.refanterior = None  # Lo mismo para la referencia anterior.
        if self.primero is None:  # Si es la lista enlazada vacía. (self.primero == None == self.ultimo)
            self.primero = elemento
            self.ultimo = elemento
        elif self.primero.enlace is None:  # Si es una lista enlazada con un elemento, estamos insertando al final.
            self.primero.enlace = elemento
            elemento.refanterior = self.ultimo
            self.ultimo = elemento
        elif anterior.enlace is None:  # Si la lista enlazada tiene más de un elemento e insertamos al final.
            anterior.enlace = elemento
            elemento.refanterior = self.ultimo
            self.ultimo = elemento
        else:  # Si es una lista enlazada con más de un elemento y no insertamos al final.
            elemento.enlace = anterior.enlace
            anterior.enlace = elemento

    def insertar_fin(self, valor):  # Inserta un elemento al final de la lista enlazada con el valor dado.
        elemento = self.Elemento(valor, None, None)
        if self.primero is None:  # Si la lista enlazada es vacía.
            self.primero = elemento
            self.ultimo = elemento
        elif self.primero.enlace is None:  # Si la lista enlazada tiene un único elemento.
            self.primero.enlace = elemento
            elemento.refanterior = self.primero
            self.ultimo = elemento
        else:  # Si la lista enlazada tiene más de un elemento.
            self.ultimo.enlace = elemento
            elemento.refanterior = self.ultimo
            self.ultimo = elemento

    def borrar(self, elemento):  # Borra el elemento de la lista enlazada.
        if elemento.refanterior is None:  # Estamos eliminando el primer elemento de la lista enlazada
            self.primero.enlace.anterior = None  # La referencia anterior del siguiente es None.
            self.primero = elemento.enlace  # El primer elemento es su enlace.
        elif elemento.enlace is None:  # Estamos eliminando el último elemento de la lista enlazada.
            self.ultimo = self.ultimo.refanterior
            self.ultimo.enlace = None
        elemento.refanterior.enlace = elemento.enlace  # Si estamos un eliminando un elemento intermedio


class Poligono(ListaDoblementeEnlazada):
    """Clase hija de ListaDoblementeEnlazada que modeliza un polígono en el plano. Un polígono es una lista doblemente
    enlazada cuyos elementos son vértices. Así, tenemos para cada vértice, su anterior y su siguiente (salvo el primero
    y el último). No tenemos atributos adicionales, pero sí métodos."""

    # Gracias a la herencia, no hace falta que programemos: constructor, métodos de inserción, borrado, número de
    # vértices, iteradores, etc.

    def mover(self, vertice, punto):  # Mueve el vértice que se le pasa a un punto = [x, y]
        for k in self:  # Buscamos por la lista hasta encontrar el vértice.
            if k == vertice:
                vertice.valor = punto

    def area(self):  # Calcula el área del polígono.
        suma1 = 0
        suma2 = 0
        for vertice in self:  # Recorremos los vértices y calculamos la suma x_1y_2+...+x_{n-1}y_n
            if vertice.enlace is not None:
                suma1 += vertice.valor[0]*vertice.enlace.valor[1]
        suma1 += self.ultimo.valor[0]*self.primero.valor[1]  # sumamos a lo anterior el sumando x_ny_1
        for vertice in self:  # Recorremos los vértices y calculamos la suma x_2y_1+...+x_ny_{n-1}
            if vertice.enlace is not None:
                suma2 += vertice.enlace.valor[0]*vertice.valor[1]
        suma2 += self.ultimo.valor[1]*self.primero.valor[0]  # sumamos a lo anterior el sumando x_1y_n
        return 0.5*abs(suma1-suma2)  # El área está dada por la
        # formula 0.5*abs((x_1y_2+...+x_{n-1}y_n+x_ny_1)-x_2y_1+...+x_ny_{n-1}+x_1y_n))

    def perimetro(self):  # Devuelve el perímetro del polígono.
        suma = 0
        for vertice in self:  # Recorremos los vértices del polígono.
            if vertice.enlace is not None:  # Sumamos la longitud de las aristas con la distancia euclídea.
                suma += sqrt((vertice.enlace.valor[0] - vertice.valor[0]) ** 2 + (
                        vertice.enlace.valor[1] - vertice.valor[1]) ** 2)
            else:
                suma += sqrt((self.primero.valor[0] - self.ultimo.valor[0]) ** 2 + (
                        self.primero.valor[1] - self.ultimo.valor[1]) ** 2)
        return suma


# PRUEBAS:
# Construimos el cuadrado unidad.
poligono = Poligono()
vertice1 = poligono.Elemento([1, 0], None, None)
vertice2 = poligono.Elemento([1, 1], None, None)
vertice3 = poligono.Elemento([0, 1], None, None)
vertice4 = poligono.Elemento([0, 0], None, None)

poligono.insertar(vertice1, vertice1.enlace)
poligono.insertar(vertice2, vertice1)
poligono.insertar(vertice3, vertice2)
poligono.insertar(vertice4, vertice3)

# El perímetro debe ser 4 y el área 1.
print(poligono.perimetro())
print(poligono.area())

# Movemos uno de los vértices.
poligono.mover(vertice2, [2, 0])

# El perímetro debe cambiar a 3+sqrt(5), pero el área no.
print(poligono.perimetro())
print(poligono.area())

# Volvemos al cuadrado unidad.
poligono.mover(vertice2, [1, 1])

# Consideramos un vértice extra.
vertice5 = poligono.Elemento([0.5, 1.5], None, None)
poligono.insertar(vertice5, vertice2)  # Gracias a la estructura de lista doblemente enlazada, es sencillo insertar el
# vértice de manera que los métodos de perímetro y área calculan las magnitudes correctamente.

# El área del polígono introducido debe ser 1.25 y el perímetro 3+sqrt(2).
print(poligono.area())
print(poligono.perimetro())
