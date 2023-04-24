class Item:
    def __init__(self,nom,val):
        self.nombre=nom
        self.valor=val

class Caja():
    def __init__(self):
        self._items=[]

    def mete(self,*items):
        self._items.extend(items)

    def vacia(self):
        items=self._items
        self._items=[]
        return items

    def cuenta(self):
        return len(self._items)

    def mirar(self,nombreitem):
        for i in self._items:
            if self._items[i].nombre==i:
                return self._items[i].nombre
            else:
                return None

'''caja1 = Caja()
caja1.mete(*(Item(str(i), i) for i in range(20)))
caja2 = Caja()
caja2.mete(*(Item(str(i), i) for i in range(9)))
organizar(caja1, caja2)
print(caja1.cuenta())
print(caja2.cuenta())'''

def organizar(*cajas):
    items=[]
    for caja in cajas:
        items.extend(caja.vacia())
    while items:
        for caja in cajas:
            try:
                caja.mete(items.pop())
            except IndexError:
                break