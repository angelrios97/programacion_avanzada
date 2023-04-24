'''class Dog:
    ''' Perro de competición. Esta clase tendrá subclases de seguridad y espectáculo...
    :cvar kind: Género zoológico según Lambert
       :ivar name: Nombre y apellidos del perro'''
    kind = 'canine'         # class variable shared by all instances
    def __init__(self, name):
        self.name = name '''

''' class Card:
"""Definition  of a numeric rank playing card.
Subclasses will define ``FaceCard`` and ``AceCard``.
Se usaría:
>>> c1=Card(7,'copas',0)
:ivar rank: Rank
:ivar suit: Suit
:ivar hard: Hard point total for a card
:ivar soft: Soft total; same as hard for all cards except
Aces.
"""
    def __init__(self,rank,suit,hard):
        self.rank=rank
        self.suit=suit
        self.hard=hard
        self.pasoaoros()
    def pasoaoros(objeto):
        objeto.suit='oros' '''

import math
class Complex:
    def __init__(self,realpart,imagpart):
        self.r=realpart
        self.i=imagpart
    def polar(self):
        return [math.sqrt(self.r**2+self.i**2),math.atan2(self.i,self.r)]