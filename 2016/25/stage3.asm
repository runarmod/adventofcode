d=a
c=7
while c != 0:
    b = 365
    while b != 0:
        d++
        b--
    c--
while 1:
    a=d
    do while a != 0:
        b=a
        a=0
        E: c=2
        F: if b != 0: goto G
        if 1 != 0: goto H
        G: b--
        c--
        if c != 0: goto F
        a++
        if 1 != 0: goto E
        H: b=2
        I: if c != 0: goto J
        if 1 != 0: goto K
        J: b--
        c--
        if 1 != 0: goto I
        K: if 0 != 0: goto K
        print(b)
