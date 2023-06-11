#ip 5

a, b, c, d, e, ip = register[0, 1, 2, 3, 4, 5]






e = 123
A: e = e & 456
if e == 72: jmp D else jmp A #e = e == 72
nop # ip = e + ip
nop # ip = A
D: e = 0
E: d = e | 65536
e = 14464005
F: c = d & 255
e = e + c
e = e & 16777215
e = e * 65899
e = e & 16777215
if 256 > d: jmp O else I #c = 256 > d
nop # ip = c + ip
nop # ip = I
nop # ip = O
I: c = 0
J: b = c + 1
b = b * 256
if b > d: jmp N else jmp M # b = b > d
nop ip = b + ip
nop K: ip = M
nop L: ip = N
M: c = c + 1
jmp J #ip = J
N: d = c
jmp F #ip = F
O: c = e == a
if e == a: jmp Q else jmp E #ip = c + ip
P: ip = E
Q: done
