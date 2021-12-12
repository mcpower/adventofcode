import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    adj = defaultdict(list)

    for line in lines:
        a, b = line.split("-")
        adj[a].append(b)
        adj[b].append(a)
    

    def paths(cur: str, seen):
        if cur == 'end':
            return 1
        if cur.islower() and cur in seen:
            return 0
        seen = seen | {cur}
        out = 0
        for thing in adj[cur]:
            out += paths(thing, seen)
        return out
    
    out = paths("start", set())
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
start-A
start-b
A-c
A-b
b-d
A-end
b-end

""",r"""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

""",r"""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
