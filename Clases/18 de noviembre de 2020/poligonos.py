from copy import deepcopy
from math import sqrt

# Se recupera la clase ListaEnlazada sin modificar y se le añade una nueva clase hija Poligono que
# modeliza polígonos en el plano y que permite calcular perímetros y áreas.


class ListaEnlazada:
    """Clase cuyos objetos son listas enlazadas. Una lista enlazada consiste en elementos. Los elementos contienen su
    valor y otro elemento como enlace que es el siguiente en la lista. De esta manera tenemos una estructura en memoria
    de referencias de cada elemento a su siguiente.
    :ivar primero: Primer elemento de la lista.
    :ivar ultimo: Último elemento de la lista. (Solamente es necesario para definir los métodos de inserción.)
    :ivar actual: Auxiliar que permite hacer que las instancias sean iterables."""

    class Elemento:
        """Subclase de ListaEnlazada cuyos objetos son los elementos que estructuran las listas enlazadas. Consisten en
        un valor y un enlace que es otro objeto elemento.
        :ivar valor: Valor del elemento.
        :ivar enlace: Objeto de la clase elemento que es el siguiente en la lista enlazada."""

        def __init__(self, valor,
                     enlace):  # Constructor de la subclase Elemento que inicializa el valor y el enlace del elemento.
            self.valor = valor
            self.enlace = enlace

    def __init__(self):  # Constructor de ListaEnlazada que inicializa una lista enlazada vacía.
        self.primero = None
        self.ultimo = None
        self.actual = None  # Servirá para hacer iterables los objetos de la clase.

    def __add__(self, lista2):  # Operador suma que devuelve la concatenación de dos listas enlazadas.
        resultado = deepcopy(self)  # Usamos deepcopy() para que el operador no modifique self.
        resultado.ultimo.enlace = lista2.primero  # El enlace del último es el primero de la segunda lista enlazada.
        resultado.ultimo = lista2.ultimo
        return resultado

    def __iter__(self):
        self.actual = ListaEnlazada.Elemento(None, self.primero)  # Inicializamos el elemento actual como un elemento
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
        if self.primero is None:  # Si es la lista enlazada vacía. (self.primero == None == self.ultimo)
            self.primero = elemento
            self.ultimo = elemento
        elif self.primero.enlace is None:  # Si es una lista enlazada con un elemento, estamos insertando al final.
            self.primero.enlace = elemento
            self.ultimo = elemento
        elif anterior.enlace is None:  # Si la lista enlazada tiene más de un elemento e insertamos al final.
            anterior.enlace = elemento
            self.ultimo = elemento
        else:  # Si es una lista enlazada con más de un elemento y no insertamos al final.
            elemento.enlace = anterior.enlace
            anterior.enlace = elemento

    def insertar_fin(self, valor):  # Inserta un elemento al final de la lista enlazada con el valor dado.
        elemento = ListaEnlazada.Elemento(valor, None)
        if self.primero is None:  # Si la lista enlazada es vacía.
            self.primero = elemento
            self.ultimo = elemento
        elif self.primero.enlace is None:  # Si la lista enlazada tiene un único elemento.
            self.primero.enlace = elemento
            self.ultimo = elemento
        else:  # Si la lista enlazada tiene más de un elemento.
            self.ultimo.enlace = elemento
            self.ultimo = elemento

    def borrar(self, elemento):  # Borra el elemento de la lista enlazada.
        for x in self:  # Recorremos la lista hasta que encontramos un x cuyo enlace es el elemento a borar.
            if x.enlace == elemento:  # Cuando lo encontramos, modificamos los enlaces para que el elemento a
                # borrar se quede sin referencias en la memoria.
                x.enlace = x.enlace.enlace  # El enlace del elemento anterior se sustituye por el del siguiente.


class Poligono(ListaEnlazada):
    """Clase hija de ListaEnlazada que modeliza un polígono en el plano. Un polígono es una lista enlazada cuyos
    elementos son vértices. Así, tenemos para cada vértice su siguiente.
    No tenemos atributos adicionales, pero sí métodos."""

    # Gracias a la herencia, no hace falta que programemos: constructor, métodos de inserción, borrado, número de
    # vértices, iteradores, etc.

    def mover(self, vertice, punto):  # Mueve el vértice que se le pasa a un punto = [x, y]
        for k in self:  # Buscamos por la lista hasta encontrar el vértice y le asociamos el punto por valor.
            if k == vertice:
                vertice.valor = punto

    def area(self):  # Calcula el área del polígono.
        suma1 = 0
        suma2 = 0
        for vertice in self:  # Recorremos los vértices y calculamos la suma x_1y_2+...+x_{n-1}y_n.
            if vertice.enlace is not None:
                suma1 += vertice.valor[0]*vertice.enlace.valor[1]
        suma1 += self.ultimo.valor[0]*self.primero.valor[1]  # Sumamos a lo anterior el sumando x_ny_1.
        for vertice in self:  # Recorremos los vértices y calculamos la suma x_2y_1+...+x_ny_{n-1}
            if vertice.enlace is not None:
                suma2 += vertice.enlace.valor[0]*vertice.valor[1]
        suma2 += self.ultimo.valor[1] * self.primero.valor[0]  # Sumamos a lo anterior el sumando x_1y_n.
        return 0.5 * abs(suma1 - suma2)  # El área está dada por la
        # formula 0.5*abs((x_1y_2+...+x_{n-1}y_n+x_ny_1)-x_2y_1+...+x_ny_{n-1}+x_1y_n)).

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
vertice1 = poligono.Elemento([1, 0], None)
vertice2 = poligono.Elemento([1, 1], None)
vertice3 = poligono.Elemento([0, 1], None)
vertice4 = poligono.Elemento([0, 0], None)

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
vertice5 = poligono.Elemento([0.5, 1.5], None)
poligono.insertar(vertice5, vertice2)  # Gracias a la estructura de lista enlazada, es sencillo insertar el
# vértice de manera que los métodos de perímetro y área calculen las magnitudes correctamente siempre que el
# orden de introdución del vértice produzca verdaderamente un polígono.

# El área del polígono introducido debe ser 1.25 y el perímetro 3+sqrt(2).
print(poligono.area())
print(poligono.perimetro())
