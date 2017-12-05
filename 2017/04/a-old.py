s=open("inp").read().strip().split("\n")
o=0
for line in s:
    if len(line.split()) == len(set(line.split())):
        o+=1
print(o)
