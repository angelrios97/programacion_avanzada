import functools
import operator

triple=functools.partial(operator.mul,3)
print(triple(2))
print(triple(3))