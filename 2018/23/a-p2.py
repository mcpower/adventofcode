import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, have utils on the side, collapse regions

use deque for queue: q[0], q.append and q.popleft
use heapq for heap: heapq.heappush, heapq.heappop

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
    robots = []
    boxes = []
    corners = []
    normals = [
        [1, 1, 1],
        [1, -1, 1],
        [-1, 1, 1]
    ]
    normal_values = [
        set(),
        set(),
        set()
    ]
    for line in lines:
        x, y, z, r = ints(line)
        v = tuple([x, y, z])
        robots.append(tuple([v, r]))
        for i, n in enumerate(normals):
            d = pdot(n, v)
            normal_values[i].add(d + r)
            normal_values[i].add(d - r)
        for d in [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]:
            for n in [-1, 1]:
                offset = pmul(r * n, d)
                corner = padd(v, offset)
                corners.append(corner)
    
    def how_many(p):
        return sum(pdist1(p, center) <= r for center, r in robots)
    # print(f"[|{'|'.join(f'{v[0]},{v[1]},{v[2]},{r}'for v, r in robots)}|]")
    # return
    
    # @functools.lru_cache(None)
    # def share(i, j):
    #     v1, r1 = robots[i]
    #     v2, r2 = robots[j]
    #     return abs(v1[0] - v2[0])  + abs(v1[1] - v2[1]) + abs(v1[2] - v2[2])<= r1 + r2
    
    # adj = make_grid(len(robots), len(robots), fill=False)
    # pairs = []
    # for i in range(len(robots)):
    #     for j in range(i+1, len(robots)):
    #         if share(i, j):
    #             adj[i][j] = True
    #             adj[j][i] = True
    #             pairs.append((i, j))

    # target = 0
    # values = []

    # print(lmap(len, normal_values))
    # for i, a in enumerate(normal_values[0]):
    #     for b in normal_values[1]:
    #         for c in normal_values[2]:
    #             # a = x + y + z
    #             # b = x - y + z
    #             # c = -x + y + z
    #             two_y = a - b
    #             if two_y % 2 == 1: continue
    #             y = two_y // 2

    #             # b - c = 2x - 2y
    #             # x = (b - c + 2y) / 2
    #             two_x = b - c + 2 * y
    #             if two_x % 2 == 1: continue
    #             x = two_x // 2
                
    #             z = a - x - y

    #             p = [x, y, z]
    #             many = how_many(p)
    #             if many >= target:
    #                 if many > target:
    #                     values.clear()
    #                 target = many
    #                 values.append(p)
    # shares = set(pairs)
    # while True:
    #     new_shares = set()
    #     for cur_share in shares:
    #         for i in range(cur_share[-1]+1, len(robots)):
    #             if all(adj[i][j] for j in cur_share):
    #                 new_shares.add(cur_share + (i,))
    #     if not new_shares:
    #         break
    #     shares = new_shares
    #     print("!")
    # pprint(shares)
    # return


    
    corners_with = [(how_many(p), p) for p in set(map(tuple,corners))]
    target, cur = max(corners_with)
    print(target)
    out = 9554099099999

    RADIUS = 8
    # print(cur, pdist1(cur))
    while True:
        for dp in itertools.product(range(-RADIUS, RADIUS+1), range(-RADIUS, RADIUS+1), range(-RADIUS, RADIUS+1)):
            new_cur = padd(dp, cur)
            x = how_many(new_cur)
            if x > target:
                target = x
                cur = new_cur
                break
        else:
            break
    print(target)




    x, y, z = cur
    for _ in range(10):
        for offset in [
            [-1 if x > 0 else 1, 0, 0],
            [0, -1 if y > 0 else 1, 0],
            [0, 0, -1 if z > 0 else 1]
        ]:
            new_cur = padd(cur, offset)
            while how_many(new_cur) == target:
                cur = new_cur
                new_cur = padd(cur, offset)
    print(pdist1(cur))
    
    # find one point
    # then keep moving to origin
    # binary search it?

    # find one point.
    

    # overlapping rectangles?
    # top square, left-down length, right-down length, ?-down length
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
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
