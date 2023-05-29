#ip 2 # a, b, ip, d, e, f = register[0, 1, 2, 3, 4, 5]








jmp 17 #ip = ip + 16
e = 1
b = 1
nop #d = e * b
nop #d = d == f
if e*b==f: jmp +2 else jmp +1 #ip = d + ip
jmp +2 #ip = ip + 1
a += e
b++
nop #d = b > f
if b>f: jmp +2 else jmp +1 #ip = ip + d
jmp 3 #ip = 2
e++
nop #d = e > f
if e>f jmp +2 else jmp +1 #ip = d + ip
jmp 2 #ip = 1
quit #ip = ip * ip
f += 2
f **= 2
f *= 19 #ip * f
f *= 11
d += 8
d *= 22 #d * ip
d += 5
f += d #f + d
jmp +(a+1) #ip = ip + a
jmp 1 #ip = 0
d = 27 #ip
d *= 28 #d * ip
d += 29 #ip + d
d *= 30 #ip * d
d *= 14 #d * 14
d *= 32 #d * ip
f += d #f + d
a = 0
jmp 1 #ip = 0
