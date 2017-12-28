s=input()
s+=s[0]
o=0
for a,b in zip(s,s[1:]):
    if a == b:
        o+=int(a)
print(o)
