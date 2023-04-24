class ColaPrioridadDict:
    """
    Cola de prioridad que se inserta con valores y prioridades y permite devolverlos uno a uno.
    :ivar cola: Guarda la cola como un diccionario.
    :ivar listavalores: Guarda los valores de la cola.
    :ivar toca: Permite iterar."""

    def __init__(self):
        self.cola = {}
        self.toca = -1  # Para iterar sobre la lista. Ponemos -1 para ahorrarnos dos lineas salvando valores.
        self.listavalores = []

    def inserta(self, nombre, prioridad):
        self.cola.update({prioridad: nombre})
        self.listavalores = list(self.cola.keys())
        self.listavalores.sort()
        return self.cola

    def __iter__(self):
        return self

    def __next__(self):
        if self.toca < len(self.listavalores) - 1:
            self.toca += 1
            return self.cola[self.listavalores[self.toca]]
        else:
            self.toca = 0
            raise StopIteration


p = ColaPrioridadDict()
p.inserta('Pepe', 2)
p.inserta("María", 1)
p.inserta("Lucía", 4)
p.inserta("Robin", 3)
p.inserta("Gato", 45)
p.inserta("Nube", 7)
for item in p:
    print(item)
