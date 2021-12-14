import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    thing, rules = paras
    thing = thing[0]

    m = {}

    for rule in rules:
        a, _, b = rule.split()
        m[a] = b
    
    def step(x):
        new_x = []
        for a, b in zip(x, x[1:]):
            if a+b in m:
                new_x.append(a)
                new_x.append(m[a+b])
            else:
                new_x.append(a)
        new_x.append(x[-1])
        return "".join(new_x)
    
    for _ in range(10):
        thing = step(thing)
    
    c = Counter(thing)
    items = c.values()
    m1 = max(items)
    m2 = min(items)
    # note from future mcpower: this is negative.
    print(m2-m1)

    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
