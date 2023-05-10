
def main():
    a = b = c = d = e = f = g = h = 0

    a = 1
    b = 107900
    c = 124900
    while True:
        f = 1
        d = 2
        while b != d:
            e = 2
            while e != b:
                if d * e == b:
                    f = 0
                e += 1
            d += 1
        if f == 0:
            h += 1
        if b == c:
            break
        b += 17
    return h
print(main())
