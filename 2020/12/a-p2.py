import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    waypoint = (-1, 10)
    ship = (0, 0)
    direction = CHAR_TO_DELTA["E"]

    for line in lines:
        dir = line[0]
        move = ints(line)[0]
        
        delta = CHAR_TO_DELTA[dir] if dir != "F" else waypoint
        if dir in "NESW":
            waypoint = padd(waypoint, pmul(move, delta))
        elif dir in "LR":
            for _ in range((move // 90) % 4):
                if dir == "L":
                    waypoint = turn_left(waypoint)
                else:
                    waypoint = turn_right(waypoint)
        else:
            ship = padd(ship, pmul(move, delta))
    
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
