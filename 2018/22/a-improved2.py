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
import heapq
def a_star(
    from_node: T,
    to_node: T,
    expand: typing.Callable[[T], typing.Iterable[typing.Tuple[int, T]]],
    heuristic: typing.Optional[typing.Callable[[T], int]] = None,
) -> typing.Tuple[int, typing.List[T]]:
    if heuristic is None:
        heuristic = lambda _: 0
    seen = set()  # type: typing.Set[T]
    g_values = {from_node: 0}  # type: typing.Dict[T, int]
    parents = {}  # type: typing.Dict[T, T]

    # (f, g, n)
    todo = [(0 + heuristic(from_node), 0, from_node)]  # type: typing.List[typing.Tuple[int, int, T]]

    while todo:
        f, g, node = heapq.heappop(todo)

        assert node in g_values
        assert g_values[node] <= g

        if node in seen:
            continue

        assert g_values[node] == g
        if node == to_node:
            break
        seen.add(node)

        for cost, new_node in expand(node):
            new_g = g + cost
            if new_node not in g_values or new_g < g_values[new_node]:
                parents[new_node] = node
                g_values[new_node] = new_g
                heapq.heappush(todo, (new_g + heuristic(new_node), new_g, new_node))
    
    if to_node not in g_values:
        raise Exception("couldn't reach to_node")
    
    # get path
    path = [to_node]
    while path[-1] != from_node:
        path.append(parents[path[-1]])

    return (g_values[to_node], path)

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

    def get_h(x, y, cannot):
        return abs(tx - x) + abs(ty - y) + (0 if cannot == 1 else 7)
    
    def expand(node):
        x,y,cannot = node

        out = []
        for i in range(3):
            if i != cannot and i != risk(x, y):
                out.append( (7, (x,y,i)))
        
        for dx, dy in GRID_DELTA:
            newx = x + dx
            newy = y + dy
            if newx < 0:
                continue

            if newy < 0:
                continue
            if risk(newx, newy) == cannot:
                continue

            out.append( (1, (newx, newy, cannot)))
        return out
        
    def heuristic(node):
        x,y,cannot = node
        return get_h(x,y,cannot)

    
    dist, path = a_star((0, 0, 1), (tx, ty, 1), expand, heuristic)
    print(dist)
    
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
