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

import concurrent.futures

relevant_attacks = [4]
for i in range(5,202):
    if (200+i-1) // i == (200+relevant_attacks[-1]-1) // relevant_attacks[-1]:
        continue
    relevant_attacks.append(i)

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()

    def get_result(cur_power, actual=False):

        # goblin = ((row, column), G/E, health, attack)
        people = []
        # grid[row][col]
        # if occupied, #
        grid = []
        for row, line in enumerate(lines):
            to_add = []
            for col, x in enumerate(line):
                if x in "GE":
                    asd = [[row, col], x, 200, 3 if x == "G" else cur_power]
                    people.append(asd)
                    to_add.append("#")
                else:
                    to_add.append(x)
            grid.append(to_add)
        
        n = len(grid)
        m = len(grid[0])
        # grid[n][m]
        
        rounds = 0

        def near(pos):
            out = ""
            for d in GRID_DELTA:
                try:
                    new = padd(pos, d)
                    out+=grid[new[0]][new[1]]
                except Exception:
                    pass
            return out
        
        def is_reachable(pos, me_type):
            # returns index of people
            i = 0
            out = []
            for x, y, h, _ in people:
                if psub(pos, x) in GRID_DELTA and me_type != y and h > 0:
                    out.append((h, x, i))
                i += 1
            if not out:
                return None
            return min(out)[2]
        
        def is_wall(pos):
            x,y=pos
            return grid[x][y] == '#'

        def get_direction(pos, me_type):
            # BFS
            # seen = {pos} # set of tuples
            pos = tuple(pos)
            to_go = [pos]
            parents = defaultdict(set)
            lengths = {pos: 0}
            
            while to_go:
                new_to_go = []
                good = []
                for old in to_go:
                    new_length = lengths[old] + 1
                    for d in GRID_DELTA:
                        new = tuple(padd(old, d))
                        already_in = new in lengths
                        if not already_in:
                            lengths[new] = new_length
                        else:
                            if lengths[new] < new_length:
                                # nope
                                continue
                            assert lengths[new] == new_length
                        if not is_wall(new):
                            parents[new].add(old)

                        if not already_in:
                            if not is_wall(new) and is_reachable(new, me_type) is not None:
                                good.append(new)
                            if not is_wall(new):
                                new_to_go.append(new)
                if good:
                    # !!!
                    good.sort()
                    cur_asd = [good[0]]
                    while True:
                        potential_returns = []
                        new_asd = []
                        for x in cur_asd:
                            if lengths[x] != 1:
                                new_asd.extend(parents[x])
                            else:
                                potential_returns.append(x)
                        if potential_returns:
                            potential_returns.sort()
                            return list(potential_returns[0])
                                
                        cur_asd = list(set(new_asd))
                to_go = new_to_go
            
            return None
        
        # print(get_direction((1, 2), "E"))
        # quit()
        
        POSITION = 0
        ME_TYPE = 1
        HEALTH = 2
        ATTACK = 3

        

        while True:
            people = [x for x in people if x[HEALTH] > 0]
            # print(people)
            people.sort()
            # print(rounds)
            # for i in range(n):
            #     s = ""
            #     for j in range(m):
            #         asd = [x[ME_TYPE] for x in people if x[POSITION] == [i, j]]
            #         if not asd:
            #             s+=grid[i][j]
            #         else:
            #             s+=asd[0]
            #     print(s)
            # for person in people:
            #     print(person)
            # print("="*10)
            
            for i, (pos, me_type, health, attack) in enumerate(people):

                if health <= 0:
                    continue
                if not any(x[HEALTH] > 0 and x[ME_TYPE] != me_type for x in people):
                    # if me_type == "G":
                    #     return None
                    # print("done")
                    # print(pos, me_type, health, attack)
                    # remaining
                    fin = sum(x[HEALTH] for x in people if x[HEALTH] > 0)
                    if actual:
                        print(*people,sep="\n")
                    # print(rounds, fin)
                    # print(rounds*fin)
                    # quit()
                    return rounds*fin
                
                reachable = is_reachable(pos, me_type)
                if reachable is not None:
                    # attack
                    people[reachable][HEALTH] -= attack
                    if people[reachable][HEALTH] <= 0:
                        if me_type == "G":
                            return
                        dead_pos = people[reachable][POSITION]
                        grid[dead_pos[0]][dead_pos[1]] = "."
                    continue
                new_pos = get_direction(pos, me_type)
                if new_pos is None:
                    continue
                people[i][POSITION] = new_pos
                grid[new_pos[0]][new_pos[1]] = "#"
                grid[pos[0]][pos[1]] = "."
                reachable = is_reachable(new_pos, me_type)
                if reachable is not None:
                    # attack
                    people[reachable][HEALTH] -= attack
                    if people[reachable][HEALTH] <= 0:
                        if me_type == "G":
                            return
                        dead_pos = people[reachable][POSITION]
                        grid[dead_pos[0]][dead_pos[1]] = "."
                    continue
            
            # if rounds % 100 == 0:
            #     print(people)
            rounds += 1
    
    print("Testing monotonicity:")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, a in enumerate(executor.map(get_result, relevant_attacks)):
            print(".X"[bool(a)], end="")
        print()
    
    asd = binary_search(get_result, 4)
    # print(asd)
    print(get_result(asd, True))
    # print(get_result(3))
    # print(get_result(3))
    # print(get_result(3))

    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD

# do_case("""#######
# #.....#
# #...E.#
# #.#.#.#
# #..G#E#
# #.....#
# #######""")
# do_case(
# """
# #######
# #.E...#
# #...?.#
# #..?G?#
# #######
# """.strip()
# )

run_samples_and_actual([
# Part 1
r"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""",r"""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""",r"""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""",r"""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""",r"""
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
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
