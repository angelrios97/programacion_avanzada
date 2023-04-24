import itertools
from functools import reduce


def divisores(n):
    return list(itertools.filterfalse(lambda x: n % x != 0, range(1, n + 1)))


def intersect(a, b):
    if len(a) > 0:
        if a[len(a) - 1] in b:
            yield a[len(a) - 1]
        a.pop()
        yield from intersect(a, b)


def mcd(a, b):
    return max(list((intersect(divisores(a), divisores(b)))))


def mcm2(a, b):
    return mcd(a, b) * int(a / mcd(a, b)) * int(
        b / mcd(a, b))  # mcm(a,b)=mcd(a,b)*a'*b' con a'=a/mcd(a,b) y b'=b/mcd(a,b)


def mcm(lista):
    return reduce(mcm2, lista)
