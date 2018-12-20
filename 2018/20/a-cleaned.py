import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, have utils on the side, collapse regions
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

Data structures:
Linked, UnionFind
use deque for queue: q[0], q.append and q.popleft

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
    to_python = inp.replace("^", "['").replace("$","']").replace("(","',[['") \
        .replace(")","']],'").replace("|","'],['").replace("[","(").replace("]",")")
    evaled_inp = eval(to_python)

    adj = defaultdict(set)
    memo = dict()

    to_d = dict(zip("NESW", [(-1, 0), (0, 1), (1, 0), (0, -1)]))
    
    def connect(a, b):
        nonlocal adj
        adj[a].add(b)
        adj[b].add(a)

    def make_adj(cur_position, obj):
        memo_key = (cur_position, obj)
        if memo_key in memo:
            return memo[memo_key]
        
        positions = set([cur_position])

        for part in obj:
            if isinstance(part, str):
                for c in part:
                    new_positions = set()
                    for pos in positions:
                        new_pos = tuple(map(operator.add, pos, to_d[c]))
                        connect(pos, new_pos)
                        new_positions.add(new_pos)
                    positions = new_positions
            else:
                positions = set(
                    thing
                    for pos in positions
                    for option in part
                    for thing in make_adj(pos, option)
                )

        memo[memo_key] = positions
        return positions

    make_adj((0, 0), evaled_inp)

    todo = [(0, 0)]
    to_dist = dict()
    dist = 0
    while todo:
        new_todo = []
        for i in todo:
            if i in to_dist:
                continue
            to_dist[i] = dist
            new_todo.extend(adj[i])
        todo = new_todo
        dist += 1

    print(max(to_dist.values()))
    print(sum(i >= 1000 for i in to_dist.values()))



run_samples_and_actual([
# Part 1
r"""
^WNE$
""",r"""
^ENWWW(NEEE|SSE(EE|N))$
""",r"""
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
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
