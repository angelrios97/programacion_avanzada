class Texvocal:
    """
Recorre un texto por sus vocales
:ivar texto
:ivar toca: la posición que toca sacar
:cvar vocales: lo que considera válido
"""
    vocales="aeiou"
    def __init__(self, tex):
        self.texto = tex
        self.toca = 0
    def __iter__(self):
        return self
    def __next__(self):
        for l in range(self.toca,len(self.texto)):
                 if self.texto[l] not in Texvocal.vocales:
                    self.toca=l+1
                    return self.texto[l]
        self.toca=0
        raise StopIteration
rev=Texvocal('spammization')
for item in rev:
    print(item)