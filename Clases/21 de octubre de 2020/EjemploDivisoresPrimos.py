import itertools


def divisores(n):
    return list(itertools.filterfalse(lambda x: n % x != 0, range(2, n)))


def noesprimo(n):
    if divisores(n):
        return True
    else:
        return False


def divisorprimo(n):
    if noesprimo(n):
        return list(itertools.filterfalse(noesprimo, range(2, n)))
    else:
        return []


print(noesprimo(6))
print(divisores(3))
print(divisorprimo(12))
print(divisorprimo(11))