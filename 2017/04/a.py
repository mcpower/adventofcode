s=open("inp").read().strip().split("\n")
o=0
for line in s:
    q = ["".join(sorted(s)) for s in line.split()]
    if len(q) == len(set(q)):
        o+=1
print(o)
