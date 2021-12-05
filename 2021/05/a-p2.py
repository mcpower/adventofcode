import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    l = []
    blah = collections.Counter()
    for line in lines:
        x1, y1, x2, y2 = ints(line)
        # if x1 == x2 or y1 == y2:
        l.append((x1, y1, x2, y2))
        # if x1 > x2:
        #     x1, x2 = x2, x1
        # if y1 > y2:
        #     y1, y2 = y2, y1
        
        if (x1, y1) > (x2, y2):
            ((x1, y1), (x2, y2)) = ((x2, y2), (x1, y1)) 
        
        if x1  != x2:
            for x in range(x1, x2 + 1):
                if y1 == y2:
                    blah[(x, y1)] += 1
                else:
                    # sprint(x1,y1,x2,y2)
                    # sprint(x1, y1)
                    delta = (y2 - y1) // abs(y2 - y1)
                    # delta *= -1
                    c = (x - x1)
                    sprint((x, y1 + c * delta))
                    blah[(x, y1 + c * delta)] += 1
        else:
            for y in range(y1, y2 + 1):
                blah[(x1, y)] += 1
        sprint("new")
        
        

    sprint(blah)
    sprint(l)
    for x, y in blah.most_common():
        if y > 1:
            out += 1
    
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
