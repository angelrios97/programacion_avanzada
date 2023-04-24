cache = {0: 0}


def fib(n):
    if n in cache:
        return cache[n]
    if n == 0:
        return 0
    elif n == 1:
        return 1
    cache.update({n: fib(n - 1) + fib(n - 2)})
    return cache[n]


print(fib(2))
print(fib(5))
print(fib(100))
print(cache)
