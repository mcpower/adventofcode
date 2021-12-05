import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    l = []
    counter = collections.Counter()
    for line in lines:
        x1, y1, x2, y2 = ints(line)
        a = [x1, y1]
        b = [x2, y2]
        diff = psub(b, a)
        delta = lmap(signum, diff)
        
        for i in range(pdistinf(diff)+1):
            point = padd(a, pmul(i, delta))
            counter[tuple(point)] += 1
        assert point == b, (point, b)

    for key in counter:
        counter[key] -= 1
    out = len(+counter)

    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

""",r"""
1,1 -> 3,3
1,1 -> 3,3
""",r"""
9,7 -> 7,9
9,7 -> 7,9
""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
