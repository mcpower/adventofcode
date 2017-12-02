dirs = dict(zip("UDLR", [-1j, 1j, -1+0j, 1+0j]))
SAMPLE = False

if SAMPLE:
    inp = r"""5 10 25"""
else:
    inp = r"""paste
your
input"""

out = 0
for line in inp.split("\n"):
    a,b,c = map(int,line.split())
    if not (a+b <= c or b+c <= a or a+c <= b):
        out += 1
print(out)
