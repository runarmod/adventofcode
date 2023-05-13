p="."
d=open(0).read()
print(sum((d.count(p),"".join((d:=(lambda x:"".join("^"if l!=r else p for(l,r)in zip(f".{x}.",f".{x}."[2:])))(d))for _ in range(399999)).count(p))))
