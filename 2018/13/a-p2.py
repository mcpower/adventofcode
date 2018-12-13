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

# WARNING: utils.py was modified (the Running section)
def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()

    grid = []
    n = len(lines)
    m = len(lines[1])

    carts = [] # (position, cur direction, L/S/R)

    for i, line in enumerate(lines):
        cur_row = []
        for j, char in enumerate(line):
            if char in "^v<>":
                pos = [j, i]  # x, y
                cur_direction = [0, 0]
                replace = ""
                if char == ">":
                    cur_direction[0] = 1
                    replace = "-"
                elif char == "<":
                    replace = "-"
                    cur_direction[0] = -1
                elif char == "v":
                    replace = "|"
                    cur_direction[1] = 1
                else:
                    replace = "|"
                    cur_direction[1] = -1
                carts.append([pos, cur_direction, 0])
                cur_row.append(replace)
            else:
                cur_row.append(char)
        grid.append(list(cur_row))
    # print(grid[0])
    # print(carts)
    iterations = 0
    # pprint(carts)
    print(len(carts))
    while len(carts) >= 2:
    # for _ in range(2):
        # one iteration
        new_carts = []
        seen_positions = set()
        bad_positions = set()
        for pos, direction, next_int in carts:
            if tuple(pos) in seen_positions:
                bad_positions.add(tuple(pos))
                continue
            x, y = padd(pos, direction)
            if (x, y) in seen_positions:
                bad_positions.add((x, y))
                continue
            if grid[y][x] == '\\':
                # any thing going left = down
                # anything going right = up
                # anything going up = left
                # anything going down = left
                new_direction = [direction[1], direction[0]]
            elif grid[y][x] == '/':
                new_direction = [-direction[1], -direction[0]]
            elif grid[y][x] == "+":
                if next_int == 0:
                    # left
                    new_direction = [direction[1], -direction[0]]
                elif next_int == 1:
                    new_direction = direction
                else:
                    # right
                    new_direction = [-direction[1], direction[0]]
                next_int += 1
                next_int %= 3
            else:
                new_direction = direction
            new_carts.append([[x, y], new_direction, next_int])
            seen_positions.add((x, y))
        
        # OLD CODE TO REMOVE DUPLICATES (did not work)
        # # remove duplicate carts
        # c = dict(Counter(map(tuple,map(fst, new_carts))))
        # # print(c)
        # new_new_carts = []
        # for cart in new_carts:
        #     asd = tuple(cart[0])
        #     # print(asd, c[asd])
        #     if c[asd] >= 2:
        #         continue
        #     new_new_carts.append(cart)
        # carts = new_new_carts
        carts = []
        for cart in new_carts:
            if tuple(cart[0]) in bad_positions:
                continue
            carts.append(cart)
        # this was originally carts.sort(), but it should be sorting y, then x
        # not vice versa! the carts are sparse enough that this probabilistically
        # won't make a difference
        carts.sort(key=lambda s: (s[0][1], s[0][0]))

        # pprint(carts)
        # print(len(carts))

        iterations += 1
    
    print(carts)
    
    c = Counter(map(tuple,map(fst, carts)))
    print(c.most_common(2))
    # quit()
    

    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""",r"""

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
