class ColaPrioridad:

    def __init__(self):
        self.cola={}
        self.toca=0

    def inserta(self,valor):
        self.cola.append(valor)
        self.cola=sort(self.cola)

    def __iter__(self):
        return self

    def __next__(self):
        if self.toca<len(self):
            self.toca+=1
            return self.pop()
        else:
            self.toca=0
            raise StopIteration