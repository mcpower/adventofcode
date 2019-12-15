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
from intcodev1 import *

def a_star2(
    from_node: T,
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
        seen.add(node)

        for cost, new_node in expand(node):
            new_g = g + cost
            if new_node not in g_values or new_g < g_values[new_node]:
                parents[new_node] = node
                g_values[new_node] = new_g
                heapq.heappush(todo, (new_g + heuristic(new_node), new_g, new_node))
    
    return g_values

def bfs2(
    from_node: T,
    expand: typing.Callable[[T], typing.Iterable[T]],
) -> typing.Tuple[int, typing.List[T]]:
    return a_star2(from_node, lambda node: ((1, other) for other in expand(node)))

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    prog = Intcode(ints(lines[0]))

    cur_pos = [0, 0]

    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 3

    UP_D = (-1, 0)
    DOWN_D = (1, 0)
    LEFT_D = (0, -1)
    RIGHT_D = (0, 1)

    # (row, col) -> is_wall
    grid = dict()
    grid[tuple(cur_pos)] = 1

    target = None

    def dfs():
        nonlocal cur_pos, grid, target
        original_pos = deepcopy(cur_pos)
        # print(original_pos)
        # move up
        if tuple(padd(cur_pos, UP_D)) not in grid:
            _, out = prog.run(UP)
            grid[tuple(padd(cur_pos, UP_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, UP_D)
                if out[0] == 2:
                    target = cur_pos
                # we went up
                dfs()
                _, out = prog.run(DOWN)
                assert out[0] != 0
                cur_pos = padd(cur_pos, DOWN_D)
            assert cur_pos == original_pos
        if tuple(padd(cur_pos, DOWN_D)) not in grid:
            _, out = prog.run(DOWN)
            grid[tuple(padd(cur_pos, DOWN_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, DOWN_D)
                if out[0] == 2:
                    target = cur_pos
                dfs()
                _, out = prog.run(UP)
                assert out[0] != 0
                cur_pos = padd(cur_pos, UP_D)
            assert cur_pos == original_pos
        if tuple(padd(cur_pos, LEFT_D)) not in grid:
            _, out = prog.run(LEFT)
            grid[tuple(padd(cur_pos, LEFT_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, LEFT_D)
                if out[0] == 2:
                    target = cur_pos
                dfs()
                _, out = prog.run(RIGHT)
                assert out[0] != 0
                cur_pos = padd(cur_pos, RIGHT_D)
            assert cur_pos == original_pos
        if tuple(padd(cur_pos, RIGHT_D)) not in grid:
            _, out = prog.run(RIGHT)
            grid[tuple(padd(cur_pos, RIGHT_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, RIGHT_D)
                if out[0] == 2:
                    target = cur_pos
                dfs()
                _, out = prog.run(LEFT)
                assert out[0] != 0
                cur_pos = padd(cur_pos, LEFT_D)
            assert cur_pos == original_pos

    dfs()

    assert target is not None
    print(target)

    def expand(p):
        out = []
        row, col = p
        for drow, dcol in GRID_DELTA:
            new_row = row + drow
            new_col = col + dcol
            blah = (new_row, new_col)
            assert blah in grid
            if grid[blah] != 0:
                out.append(blah)
        return out

    # this should be dists = bfs2(tuple(target), expand)
    # and then out = max(dists.values())
    # but I thought
    
    heuristic = lambda _: 0
    from_node = tuple(target)
    seen = set()  # type: typing.Set[T]

    # (f, g, n)
    todo = [(from_node)]  # type: typing.List[typing.Tuple[int, int, T]]
    out = 0

    while todo:
        new_todo = []

        for node in todo:
            seen.add(node)
            for new_node in expand(node):
                if new_node not in seen:
                    new_todo.append(new_node)
        
        todo = new_todo
        if todo:
            out += 1

    print(out)
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""

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
