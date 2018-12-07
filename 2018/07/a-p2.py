import sys; sys.dont_write_bytecode = True; from utils import *
"""
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp

Previous problems:
knot

Dict things:
dict.keys()
dict.values()
dict.items()
"""

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    
    def get_time(c):
        return ord(c) - ord('A') + 1 + (0 if sample else 60)
    WORKERS = 2 if sample else 5
    
    lines = inp.splitlines()
    d = defaultdict(set)
    remaining = defaultdict(int)

    for line in lines:
        q = line.split()
        a, b = q[1] , q[-3]
        d[a].add(b)
        remaining[b]
        remaining[a]
        remaining[b] += 1
        sprint(a,b)
    out = ""

    cur_time = 0
    doing = [None] * WORKERS # (thing, time to finish)

    while remaining or any(doing):
        

        # any workers finished?
        for i in range(WORKERS):
            if doing[i] is not None and doing[i][-1] == cur_time:
                cur = doing[i][0]
                for other in d[cur]:
                    remaining[other] -= 1
                doing[i] = None
        
        zeroes = [key for key, value in keyvalues(remaining) if value == 0]
        zeroes.sort()
        zeroes.reverse()
        
        sprint(cur_time, doing)

        for i in range(WORKERS):
            if not zeroes:
                break
            if doing[i] is not None:
                continue
            cur = zeroes[-1]
            doing[i] = (cur, cur_time + get_time(cur))
            zeroes.pop()
            del remaining[cur]
        
        sprint(cur_time, doing)
        cur_time += 1
        
        
        # all workers are now assigned

        
    print(cur_time-1)
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""],[
# Part 2
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
