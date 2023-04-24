import itertools

lee=itertools.takewhile(lambda x: x!='***\n', open('todo', 'r'))
print(tuple(lee))