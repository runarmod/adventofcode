d=a
c=7
A: b=365
B: d++
b--
if b != 0: goto B
c--
if c != 0: goto A
C: a=d
D: if 0 != 0: goto D
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
if a != 0: goto D
if 1 != 0: goto C
