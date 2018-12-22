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

    dp = make_grid(tx+1000, ty+1000, None)
    dp[0][0] = 0
    dp[tx][ty] = 0
    def erosion(x, y):
        if dp[x][y] is not None:
            return dp[x][y]
        geo = None
        if y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            geo = erosion(x-1, y) * erosion(x, y-1)
        dp[x][y] = (geo + depth) % 20183
        return dp[x][y]
    
    def risk(x, y):
        return erosion(x, y) % 3
    

    
    print(sum(erosion(x, y) % 3 for x in range(tx+1) for y in range(ty+1)))

    # torch = 1
    import heapq
    queue = [(0, 0, 0, 1)] # (minutes, x, y, cannot)
    best = dict() # (x, y, cannot) : minutes

    target = (tx, ty, 1)
    while queue:
        minutes, x, y, cannot = heapq.heappop(queue)
        best_key = (x, y, cannot)
        if best_key in best and best[best_key] <= minutes:
            continue
        best[best_key] = minutes
        if best_key == target:
            print(minutes)
            print(best_key)
            return
        for i in range(3):
            if i != cannot and i != risk(x, y):
                heapq.heappush(queue, (minutes + 7, x, y, i))
        
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
            heapq.heappush(queue, (minutes + 1, newx, newy, cannot))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
depth: 510
target: 10,10
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
