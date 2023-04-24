class Vector2:
    '''Vectores en el plano
    :ivar x: Primera coordenada
    :ivar y: Segunda coordeanda'''

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self,vector2):
        totalx=self.x+vector2.x
        totaly=self.y+vector2.y
        return Vector2(totalx,totaly)

    def __str__(self):
        return str((self.x,self.y))

    def __mul__(self,vector2):
        totalx=self.x*vector2.x
        totaly=self.y*vector2.y
        return totalx+totaly

v1=Vector2(2,3)
v2=Vector2(3,4)
v3=v1+v2
print(v3)
v4=v1*v2
print(v4)
