import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    start, your, nearby = paras

    fields = dict()

    for line in start.splitlines():
        a, b = line.split(":" )
        
        fields[a] = every_n(positive_ints(b), 2)
    sprint(fields)
    
    for line in nearby.splitlines()[1:]:
        sprint(line)
        for i in ints(line):
            bad = 0
            if not any(a <= i <= b for ranges in fields.values() for a,b in ranges):
                out += i
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
