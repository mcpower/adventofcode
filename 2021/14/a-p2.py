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
    
    new_thing = defaultdict(int)
    for a, b in zip(thing, thing[1:]):
        new_thing[a+b] += 1
    
    def step(x: typing.Dict[str, int]):
        new = defaultdict(int)
        for key in x:
            if key in m:
                a, b = key
                c = m[key]
                for new2 in [a+c, c+b]:
                    new[new2] += x[key]
            else:
                new[key] += x[key]
        return new
        # new_x = []
        # for a, b in zip(x, x[1:]):
        #     if a+b in m:
        #         new_x.append(a)
        #         new_x.append(m[a+b])
        #     else:
        #         new_x.append(a)
        # new_x.append(x[-1])
        # return "".join(new_x)
    
    for _ in range(40):
        new_thing = step(new_thing)
    
    chars = Counter()
    for (a, b), val in new_thing.items():
        chars[a] += val
        chars[b] += val
    # note from future mcpower: we only counted the first and last chars once,
    # but we counted the middle chars multiple times, so intentionally
    # double-count the first and last chars. 
    chars[thing[0]] += 1
    chars[thing[-1]] += 1
    items = chars.values()
    m1 = max(items)
    m2 = min(items)
    print((m1-m2)//2)

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
