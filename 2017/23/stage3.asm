a = 1
b = 107900
c = 124900
A: f = 1
d = 2
B: e = 2
C: g = d * e - b
if g != 0: goto D
f = 0
D: e++
g = e - b
if e != b: goto C
d++
g = d - b
if d != b: goto B
if f != 0: goto E
h++
E: g = b - c
if b != c: goto F
goto G
F: b += 17
goto A
G: end
