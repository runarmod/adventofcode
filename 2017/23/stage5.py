



def main():
    b = d = e = f = h = 0

    for b in range(107900, 124900 + 1, 17):
        f = 1
        for d in range(2, b):
            e = 2
            while e != b:
                if d * e == b:
                    f = 0
                e += 1
        if f == 0:
            h += 1
    return h


print(main())
