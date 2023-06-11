#ip 5

# a, b, c, d, e, ip = register[0, 1, 2, 3, 4, 5]
a = b = c = d = e = ip = 0



seen = set()

e = 123
while e != 72:
    e &= 456
e = 0
while True:
    d = e | 65536
    e = 14464005
    while True:
        c = d & 255
        e += c
        e &= 16777215
        e *= 65899
        e &= 16777215
        if d < 256:
            if e not in seen:
                print(e)
            seen.add(e)
            break
        d //= 256
