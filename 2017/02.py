import sys
a=sys.stdin.read()
q = [list(map(int, s.split())) for s in a.split("\n")]

o=0
for l in q:
    done=False
    for a in l:
        if done:break
        for b in l:
            if done: break
            if a == b: continue
            if a%b==0:
                o+=a//b
                done=True
                break
print(o)
print(sum(max(l) - min(l) for l in q if l))
