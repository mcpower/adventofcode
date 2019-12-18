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

def bfs(
    from_node,
    expand,
    to_node=None
):
    """
    Returns (distances, parents).
    Use path_from_parents(parents, node) to get a path.
    """
    g_values = {from_node: (0, tuple())} 
    todo = [(from_node, tuple())] 
    dist = 0

    while todo:
        new_todo = []
        dist += 1
        for node, keys_needed in todo:
            for new_node, new_keys_needed in expand(node):
                if new_node not in g_values:
                    asd=  keys_needed + new_keys_needed
                    new_todo.append((new_node, asd))
                    g_values[new_node] = (dist, asd)
        todo = new_todo
    
    return g_values

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    grid = lmap(list,inp.splitlines())

    rows = len(grid)
    cols = len(grid[0])

    def expand(state):
        # sprint(state)
        pos = state
        out = []

        for dpos in GRID_DELTA:
            new_pos = padd(dpos, pos)
            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
                other = grid[new_pos[0]][new_pos[1]]
                if other == "#":
                    continue
                if other.isalpha() and other.isupper():
                    out.append((tuple(new_pos), (other,)))
                else:
                    out.append((tuple(new_pos), tuple()))
        
        return out
    
    # find cur pos
    positions = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "@":
                grid[row][col] = "#"
                for drow in [-1, 0, 1]:
                    for dcol in [-1, 0, 1]:
                        new_char = None
                        if drow in [-1, 1] and dcol in [-1, 1]:
                            new_char = "@"
                            positions.append((row+drow, col+dcol))
                        else:
                            new_char = "#"
                        grid[row+drow][col+dcol] = new_char
                break
        else:
            continue
        break
    
    for i, (row, col) in enumerate(positions):
        grid[row][col] = str(i)
    print(positions)
    # return
    # quit()
    
    
    # find keys
    keys = {}
    
    for row in range(rows):
        for col in range(cols):
            thing = grid[row][col]
            if thing.isalpha() and thing.islower():
                keys[thing] = [row, col]
    
    key_to_key = {}
    for key, key_pos in list(keys.items()) + list({str(i): pos for i, pos in enumerate(positions)}.items()):
        key_l = key.lower()
        key_u = key.upper()
        key_pos = tuple(key_pos)

        dists = bfs(key_pos, expand)

        cur_dists = {}
        for other_key, other_key_pos in keys.items():
            if other_key == key:
                continue
            other_key_pos = tuple(other_key_pos)
            if other_key_pos not in dists:
                continue
            dist, keys_needed = dists[other_key_pos]

            cur_dists[other_key] = (dist, frozenset(keys_needed))

        key_to_key[key] = cur_dists
    

    START = (("0", "1", "2", "3"), frozenset())
    GOAL = (("1", "2", "3", "4"), frozenset())
    
    def meta_expand(node):
        current_keys, keys_i_have = node

        if len(keys_i_have) == len(keys):
            return [(0, GOAL)]
        out = []

        # sprint(node)

        for i in range(4):
            key = current_keys[i]
            for other_key, (dist, keys_needed) in key_to_key[key].items():
                # sprint(other_key, dist, keys_needed)
                if other_key in keys_i_have:
                    continue
                if len(keys_needed - keys_i_have) != 0:
                    continue
                new_set = keys_i_have | frozenset({other_key.upper()})
                new_current_keys = list(current_keys)
                new_current_keys[i] = other_key
                new_current_keys = tuple(new_current_keys)
                # sprint(new_set)
                out.append((dist, (new_current_keys, new_set)))
        
        # sprint(out, node)
        assert out, node
        return out
    
    # warning: takes 1m20s to run
    print(a_star(START, GOAL, meta_expand)[0])




    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
""",r"""
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############
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
