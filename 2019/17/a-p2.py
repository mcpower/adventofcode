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
def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    prog = Intcode(ints(lines[0]))
    prog[0] = 2

    # def dfs():
    #     nonlocal cur_pos, cur_direction, seen, commands
    #     # ALWAYS stay up
    #     assert cur_direction == CHAR_TO_DELTA["U"]
    #     old_pos = list(cur_pos)
    #     grid[cur_pos[0]][cur_pos[1]] = "."

    #     repeated = set()

    #     for rotated in range(4):
    #         # try moving in that direction
    #         new_direction = list(cur_direction)
    #         for moves in range(rotated):
    #             new_direction = turn_left(new_direction)
    #         new_pos = padd(cur_pos, new_direction)
    #         assert tuple(new_pos) not in repeated
    #         repeated.add(tuple(new_pos))
    #         new_row, new_col = new_pos
    #         if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] == "#":
    #             for moves in range(rotated):
    #                 commands.append("b")
    #                 cur_direction = turn_left(cur_direction)
    #             assert new_direction == cur_direction
    #             commands.append("a")
    #             cur_pos = padd(cur_pos, cur_direction)
    #             for moves in range(rotated):
    #                 commands.append("c")
    #                 cur_direction = turn_right(cur_direction)
    #             assert cur_direction == CHAR_TO_DELTA["U"]
    #             # print("doing dfs,", cur_pos, cur_direction)
    #             dfs()
    #             # print("done dfs,", cur_pos, cur_direction)
    #             assert cur_direction == CHAR_TO_DELTA["U"]

    #             # turn left 2+rotated times
    #             for moves in range(2+rotated):
    #                 commands.append("b")
    #                 cur_direction = turn_left(cur_direction)
    #             # move forward
    #             commands.append("a")
    #             cur_pos = padd(cur_pos, cur_direction)
    #             # then turn right 2+rotated times
    #             for moves in range(2+rotated):
    #                 commands.append("c")
    #                 cur_direction = turn_right(cur_direction)

    #             assert cur_pos == old_pos, (cur_pos, old_pos)
    #             assert cur_direction == CHAR_TO_DELTA["U"], cur_direction

    # def run_with(commands):
    #     nonlocal prog
    #     outputs = []
    #     to_run = ",".join(commands)
    #     for c in to_run:
    #         halted, output = prog.run(ord(c))
    #         outputs.extend(output)
    #         if halted:
    #             print("wtf")
    #             return halted, output
    #         # assert output == []
    #     halted, output = prog.run(10)

    #     return halted, output

    _, out = Intcode(ints(lines[0])).run()
    grid = lmap(list, "".join(map(chr, out)).split())
    # print("".join(map(chr, out)))

    rows = len(grid)
    cols = len(grid[0])
    

    cur_pos = None
    cur_direction = CHAR_TO_DELTA["U"]
    for row in range(0, rows):
        for col in range(0, cols):
            if grid[row][col] == "^":
                cur_pos = [row, col]
    
    seen = make_grid(rows, cols, False)
    grid[cur_pos[0]][cur_pos[1]] = "#"

    commands = []


    while True:
        left_r, left_c = padd(cur_pos, turn_left(cur_direction))
        right_r, right_c = padd(cur_pos, turn_right(cur_direction))

        if 0 <= left_r < rows and 0 <= left_c < cols and grid[left_r][left_c] == "#":
            cur_direction = turn_left(cur_direction)
            commands.append("L")
        elif 0 <= right_r < rows and 0 <= right_c < cols and grid[right_r][right_c] == "#":
            cur_direction = turn_right(cur_direction)
            commands.append("R")
        else:
            break
        moved = 0
        new_r, new_c = padd(cur_pos, cur_direction)
        while 0 <= new_r < rows and 0 <= new_c < cols and grid[new_r][new_c] == "#":
            cur_pos = [new_r, new_c]
            moved += 1
            new_r, new_c = padd([new_r, new_c], cur_direction)
        # print(cur_pos)
        commands.append(str(moved))

    for char in "A,B,A,C,B,C,B,A,C,B\nL,10,L,6,R,10\nR,6,R,8,R,8,L,6,R,8\nL,10,R,8,R,8,L,10\nn\n":
        _, out = prog.run(ord(char))
        if out:
            print(out[-10:])
    
    # print(out[:10])
    
    
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
