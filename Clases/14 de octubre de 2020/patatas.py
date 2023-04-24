class Patata:
    '''Tubérculo con aplicaciones a la alimentación de varias especies.
    :ivar tamaño: Cómo es de grande la patata'''
    def __init__(self,tamaño):
        self.tamaño=tamaño
cena=Patata(32456546)

class Empleados:
    '''
    Un obrero de los que están en blanco, legal.
    :ivar nombre: Apelativo al que se suele responder
    :ivar sueldo: Lo que deberíamos pagarle
    :cvar cuantos: Total de la plantilla'''
    cuantos=0
    def __init__(self,nom,suel):
        self.nombre=nom
        self.sueldo=suel
        Empleados.cuantos+=1
    def sellama(self):
        return self.nombre
    def gana(self):
        return self.sueldo
    def total(self):
        return Empleados.cuantos
    def cambiarsueldo(self,incremento):
        self.sueldo+=incremento

