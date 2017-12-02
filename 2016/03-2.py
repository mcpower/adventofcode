dirs = dict(zip("UDLR", [-1j, 1j, -1+0j, 1+0j]))
SAMPLE = True

if SAMPLE:
    inp = r"""101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603"""
else:
    inp = r"""paste
your
input"""

out = 0
x = [list(map(int, l.split())) for l in inp.split("\n")]
for x, y, z in zip(x[::3], x[1::3], x[2::3]):
    for a, b, c in zip(x, y, z):
    #a,b,c = map(int,line.split())
        if not (a+b <= c or b+c <= a or a+c <= b):
            out += 1
print(out)
