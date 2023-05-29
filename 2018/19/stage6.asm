#ip 2 # a, b, ip, d, e, f = register[0, 1, 2, 3, 4, 5]


a = (part - 1)
b = 0
ip = 0
d = 0
e = 0
f = 0

f = 1017

if a == 1:
    f += 10550400
    a = 0
elif a != 0:
    raise WTF

for e in range(1, f + 1):
    for b in range(1, f + 1):
        if e * b == f:
            a += e


# Observing that it calculates the sum of ALL factors of f
# Part 1: f = 1017
# Part 2: f = 10551417

