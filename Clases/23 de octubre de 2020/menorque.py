from functools import partial

def elementomenor(x,lista):
    return all(map(lambda y: x < y, lista))

def menorque(a,b):
    menor2=partial(elementomenor,lista=b)
    return all(map(menor2,a))
