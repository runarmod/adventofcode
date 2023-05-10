a = 1
b = 79 * 100 + 100000
c = 79 * 100 + 100000 + 17000
A: f = 1
d = 2
B: e = 2
C: g = d * e - b
jnz g D
f = 0
D: e += 1
g = e - b
jnz g C
d += 1
g = d - b
jnz g B
jnz f E
h += 1
E: g = b - c
jnz g F
jnz 1 G
F: b -= -17
jnz 1 A
G: end
