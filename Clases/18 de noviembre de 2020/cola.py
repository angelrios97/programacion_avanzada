class Cola:

    def __init__(self):
        self.elementos = []

    def sacar(self):
        if self.elementos:
            self.elementos.pop(0)

    def mirar(self):
        if self.elementos:
            return self.elementos[0]

    def meter(self, elemento):
        self.elementos.append(elemento)

    def vacia(self):
        if self.elementos:
            return False
        else:
            return True
