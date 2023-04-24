def facacum(n,acum=1):
    yield acum*n
    if n!=1:
        yield from facacum(n-1,acum*n)
list(facacum(4))
print(list(facacum(4)))