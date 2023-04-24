from copy import deepcopy


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


lista = ListaEnlazada()
el4 = ListaEnlazada.Elemento(4, None)
el3 = ListaEnlazada.Elemento(3, el4)
el2 = ListaEnlazada.Elemento(2, el3)
el1 = ListaEnlazada.Elemento(1, el2)
lista.insertar(el1, lista.primero)  # Inserción en lista enlazada vacía.
lista.insertar(el2, el1)  # Inserción en lista enlazada con un elemento.
lista.insertar(el3, el1)  # Inserción en lista enlazada con más de un elemento.
lista.insertar(el4, el2)  # Inserción al final de una lista enlazada con más de un elemento.
lista.insertar_fin(65)  # Inserción al final
print(len(lista))  # Tamaño de la lista enlazada
n = 0
for _ in lista:  # Valores indexados de la lista enlazada.
    n += 1
    print(n, _.valor)
listado = ListaEnlazada()  # Inserción al final en lista enlazada vacía.
listado.insertar_fin(78)
listado.insertar_fin(-2.5)
suma = lista + listado  # Concatenación de listas enlazadas.
print(len(suma))  # Tamaño de la lista suma.
k = 0
for _ in suma:  # Valores indexados de la lista enlazada suma.
    k += 1
    print(k, _.valor)
