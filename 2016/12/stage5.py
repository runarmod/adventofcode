a = b = c = d = 0
a = 1
b = 1
c = 1

for _ in range(26 if c == 0 else 26 + 7):
    a, b = a + b, a

print(a + 17 * 18)
