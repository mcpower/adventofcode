import sys; sys.dont_write_bytecode = True; from utils import *
import cmath

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    waypoint = (-1, 10)
    ship = (0, 0)

    for line in lines:
        dir = line[0]
        move = ints(line)[0]
        
        delta = CHAR_TO_DELTA[dir] if dir != "F" else waypoint
        if dir in "NESW":
            waypoint = padd(waypoint, pmul(move, delta))
        elif dir in "LR":
            angle = move # / 360 * math.tau
            if dir == "R":
                angle *= -1
            # drow, dcol
            # i.e. dcol is normal, drow is "negated".
            # and row and col are "mixed".
            c = complex(waypoint[1], -waypoint[0])
            c *= cmath.rect(1, angle)
            waypoint = [-c.imag, c.real]

            # for _ in range((move // 90) % 4):
            #     if dir == "L":
            #         waypoint = turn_left(waypoint)
            #     else:
            #         waypoint = turn_right(waypoint)
        else:
            ship = padd(ship, pmul(move, delta))
    
    print(ship)
    print(pdist1(ship))
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
F10
N3
F7
R90
F11
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
