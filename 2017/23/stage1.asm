b = 79
c = b
b *= 100
b -= -100000
c = b
c -= -17000
A: f = 1
d = 2
B: e = 2
C: g = d
g *= e
g -= b
jnz g D
f = 0
D: e -= -1
g = e
g -= b
jnz g C
d -= -1
g = d
g -= b
jnz g B
jnz f E
h -= -1
E: g = b
g -= c
jnz g F
jnz 1 G
F: b -= -17
jnz 1 A
G: end
