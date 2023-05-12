a = b = c = d = 0
a = 1
b = 1
# c = 1
d = 26


if c != 0:
    for c in range(7, 0, -1):
        d += 1
while d != 0:
    c = a
    while b != 0:
        a += 1
        b -= 1
    b = c
    d -= 1
for c in range(17, 0, -1):
    for d in range(18, 0, -1):
        a += 1


print(a)
