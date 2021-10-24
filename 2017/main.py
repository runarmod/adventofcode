import math
c = 0

a = [14, 3, 0.8]
b = [2, 6, 0.8]


for x, y in zip(a, b):
    c += (x - y) ** 2

print(math.sqrt(c))