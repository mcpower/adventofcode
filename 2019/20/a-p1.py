import sys; sys.dont_write_bytecode = True; from utils import *
"""
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words

Data structures:
Linked, UnionFind
dict: d.keys(), d.values(), d.items()
deque: q[0], q.append and q.popleft

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp
"""

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    grid = lmap(list, inp.splitlines())
    # print(inp)

    done_words = set()

    portals_name_pair = defaultdict(list)

    start = None
    end = None


    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if (row, col) in done_words:
                continue
            this = grid[row][col]
            if this.isalpha():
                done_words.add((row, col))
                # find matching one
                # right and down
                left = (row, col)
                other = None
                if grid[row+1][col].isalpha():
                    right = (row+1, col)
                    other = grid[row+1][col]
                elif grid[row][col+1].isalpha():
                    right = (row, col+1)
                    other = grid[row][col+1]
                else:
                    print(grid[row][col], grid[row+1][col], grid[row][col+1], grid[row-1][col], grid[row][col-1])
                    assert False
                done_words.add(right)

                # find a dot right/down of right,
                right_row, right_col = right

                portal_pos = None

                if right_row < rows - 1 and grid[right_row+1][right_col] == '.':
                    portal_pos = right
                    dot = (right_row+1, right_col)
                elif right_col < cols - 1 and grid[right_row][right_col+1] == '.':
                    portal_pos = right
                    dot = (right_row, right_col+1)
                # find a dot left/up of row col
                # watch out for negatives
                elif row >= 1 and grid[row-1][col] == '.':
                    portal_pos = left
                    dot = (row-1, col)
                elif col >= 1 and grid[row][col-1] == '.':
                    portal_pos = left
                    dot = (row, col-1)
                else:
                    assert False

                name = this + other
                if name == "AA":
                    start = dot
                if name == "ZZ":
                    end = dot
                
                portals_name_pair[name].append((portal_pos, dot))
    
    portals_from_to = {} # pos: to
    for key, value in portals_name_pair.items():
        if len(value) != 2:
            assert key in ("AA", "ZZ")
            continue
        # all tuples
        (a, a_dot), (b, b_dot) = value
        portals_from_to[a] = b_dot
        portals_from_to[b] = a_dot
    # sprint(portals_from_to)
    def expand(node):
        out = []
        
            # return out
        for dpos in GRID_DELTA:
            new_row, new_col = padd(node, dpos)

            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] not in "# ":
                    new_thing = (new_row, new_col)
                    out.append(new_thing)
                    if new_thing in portals_from_to:
                        out.append(portals_from_to[new_thing])
        return out
    
    dist, _ = bfs_single(start, end, expand)
    print(dist)


    # get the things
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
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
