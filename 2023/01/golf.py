def n(l,b,p):
    c=len(l)
    r=range(*((c,)if b else(c-1,-1,-1)))
    d={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9}
    return min(__import__("itertools").chain(((i,l[i])for i in r if l[i].isdigit()),((i,str(a))for i in r if p and(a:=next((d[k]for k in d if"".join(l[i:]).startswith(k)),0)))),key=lambda x:-x[0]if b else x[0])[1]
for p in(0,1):
    print(f"Part {p+1}:",sum(int(n(l,0,p)+n(l,1,p))for l in open("input.txt").read().strip().split("\n")))
