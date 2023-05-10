



from tqdm import trange


def main():
    b = d = e = f = h = 0

    for b in trange(107900, 124900 + 1, 17):
        f = 1
        for d in range(2, b):
            for e in range(2, b):
                if d * e == b:
                    f = 0
                    break
            if f == 0:
                break
        if f == 0:
            h += 1
    return h


print(main())
