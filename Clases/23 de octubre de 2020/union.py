def interseccion(a,b):
    return filter(lambda x: x in b, a)

def

def difsim(a,b):
    return list(filter(lambda x: x not in interseccion(a,b),a+b))

def union(a,b):
    return list(filter(lambda x: x not in difsim(a,b),a+b))


