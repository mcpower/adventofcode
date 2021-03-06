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
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    depth = ints(lines[0])[0]
    tx, ty = tuple(ints(lines[1]))

    @functools.lru_cache(None)
    def erosion(x, y):
        if (x, y) == (tx, ty):
            return 0
        if (x, y) == (0, 0):
            return 0
        geo = None
        if y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            geo = erosion(x-1, y) * erosion(x, y-1)
        return (geo + depth) % 20183
    
    def risk(x, y):
        return erosion(x, y) % 3

    print(sum(risk(x, y) for x in range(tx+1) for y in range(ty+1)))

    def get_h(x, y):
        # TODO: add "cannot" into this calculation
        return abs(tx - x) + abs(ty - y)

    # torch = 1
    import heapq
    queue = [(get_h(0, 0), 0, 0, 0, 1)] # (f, minutes, x, y, cannot)
    seen = set() # (x, y, cannot) : minutes

    target = (tx, ty, 1)
    while queue:
        f, minutes, x, y, cannot = heapq.heappop(queue)
        seen_key = (x, y, cannot)
        if seen_key in seen:
            continue
        seen.add(seen_key)
        if seen_key == target:
            print(minutes)
            return
        for i in range(3):
            if i != cannot and i != risk(x, y):
                heapq.heappush(queue, (f + 7, minutes + 7, x, y, i))
        
        # try going up down left right
        for dx, dy in GRID_DELTA:
            newx = x + dx
            newy = y + dy
            if newx < 0:
                continue

            if newy < 0:
                continue
            if risk(newx, newy) == cannot:
                continue
            heapq.heappush(queue, (minutes + 1 + get_h(newx, newy), minutes + 1, newx, newy, cannot))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
depth: 510
target: 10,10
""",r"""
depth: 3558
target: 15,740
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
