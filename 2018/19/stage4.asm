#ip 2 # a, b, ip, d, e, f = register[0, 1, 2, 3, 4, 5]








jmp H
A: e = 1
B: b = 1
nop
nop
C: if e*b==f: jmp D
jmp E
D: a += e
E: b++
nop
if b>f: jmp F
jmp C
F: e++
nop
if e>f: jmp G
jmp B
G: quit
H: f += 2
f **= 2
f *= 19
f *= 11
d += 8
d *= 22
d += 5
f += d
jmp +(a+1)
jmp A
d = ((27 * 28) + 29) * 30 * 14 * 32 #d = 27
nop #d *= 28
nop #d += 29
nop #d *= 30
nop #d *= 14
nop #d *= 32
f += d
a = 0
jmp A
