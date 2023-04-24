class Oveja:
    '''Ovejas.
    :ivar edad:
    :ivar peso:
    :ivar raza:'''
    def __init__(self,edad,peso,raza):
        self.edad=edad
        self.peso=peso
        self.raza=raza
        self.balidos=0

    def __lt__(self,oveja2):
        if self.edad<oveja2.edad:
            return True
        elif self.edad>oveja2.edad:
            return False
        elif self.peso<oveja2.peso:
            return True
        else:
            return False

    def __mul__(self,oveja2):
        if self.raza==oveja2.raza:
            return Oveja(0,0,self.raza)
        else:
            return Oveja(0,0,[self.raza,oveja2.raza])
    def __iter__(self):
        return self
    def __next__(self):
        if self.balidos<3:
            self.balidos+=1
            return "Beee"
        else:
            self.balidos=0
            raise StopIteration