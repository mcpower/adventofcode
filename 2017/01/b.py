s=input()
o=0
for a,b in zip(s,s[len(s)//2:]):
    print(a,b)
    if a == b:
        o+=int(a)
print(o*2)
