import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    minx,  maxx , miny, maxy = ints(inp)

    def height(vx, vy) -> typing.Optional[int]:
        x, y = 0, 0
        # from future mcpower: this is slooow. inline this for performance!
        def step():
            nonlocal vx, vy, x, y
            x += vx
            y += vy
            vy -= 1 
            vx -= signum(vx)
        
        highest = 0
        while True:
            highest = max(highest, y)
            if minx <= x <= maxx and miny <= y <= maxy:
                return highest
            if y < miny and vy < 0:
                return None
            if x > maxx:
                return None
            step()
        # return None

    for vx in range(0, 1000):
        for vy in range(0, 2000):
            asdf = height(vx, vy)
            if asdf is not None:
                out = max(out, asdf)
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
target area: x=20..30, y=-10..-5
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
