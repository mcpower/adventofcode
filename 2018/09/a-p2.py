import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, and have utils on the side

Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

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

def do_old(players, last_marble):
    

    marbles = [0]
    scores = [0] * players

    remaining = set(range(1, last_marble+1))

    cur_player = 0
    cur_index = 0
    # while remaining:
    #     to_add = min(remaining)
        # remaining.remove(to_add)
    # blah = []
    for to_add in range(1, last_marble + 1):
        if to_add % 23 == 0:
            scores[cur_player] += to_add
            to_remove = (cur_index - 7) % len(marbles)
            scores[cur_player] += marbles[to_remove]
            
            print(to_add, marbles[to_remove])
            # blah.append(marbles[to_remove])
            del marbles[to_remove]
            cur_index = to_remove
            
            
        else:
            insert_pos = (cur_index + 2) % len(marbles)
            marbles.insert(insert_pos, to_add)
            cur_index = insert_pos

        # sprint(marbles, cur_index)
        cur_player += 1
        if cur_player == players:
            cur_player = 0
    # print(blah)
    return max(scores)

class Linked:
    def __init__(self, val):
        self.val = val
        self.before = self
        self.after = self

# def do_new(players, last_marble):
#     scores = [0] * players
#     for i in range(1, last_marble + 1):
#         cur_player = i % players
#         to_add = i + i - 4
#         scores[cur_player] += to_add
#     return max(scores)

def do_new(players, last_marble):
    marbles = Linked(0)
    scores = [0] * players

    cur_player = 0
    cur_index = 0
    # while remaining:
    #     to_add = min(remaining)
        # remaining.remove(to_add)
    # blah = []
    for to_add in range(1, last_marble + 1):
        if to_add % 23 == 0:
            scores[cur_player] += to_add
            for _ in range(7):
                marbles = marbles.before
            
            scores[cur_player] += marbles.val
            # print(to_add, marbles.val)
            # print(to_add, marbles[to_remove])
            # blah.append(marbles[to_remove])
            to_delete = marbles
            marbles = marbles.after
            marbles.before = to_delete.before
            marbles.before.after = marbles
            del to_delete
        else:
            # insert_pos = (cur_index + 2) % len(marbles)
            # marbles.insert(insert_pos, to_add)
            # cur_index = insert_pos
            # move two forward
            marbles = marbles.after
            marbles = marbles.after
            asd = Linked(to_add)

            asd.before, asd.after = marbles.before, marbles
            asd.before.after = asd
            asd.after.before = asd
            marbles = asd

        # sprint(marbles, cur_index)
        cur_player += 1
        if cur_player == players:
            cur_player = 0
    # print(blah)
    return max(scores)

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    players, last_marble = ints(inp)
    
    # print(do_old(players, last_marble))
    print(do_new(players, last_marble))
    # quit()
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD


# q = [19, 42, 65, 88, 111, 134, 157, 180, 203, 226, 249, 272, 295, 318, 341, 364, 387, 410, 433, 456, 479, 502, 525, 548, 571, 594, 617, 640, 663, 686, 709, 732, 755, 778, 801, 824, 847, 870, 893, 916, 939, 962, 985, 1008, 1031, 1054, 1077, 1100, 1123, 1146, 1169, 1192, 1215, 1238, 1261, 1284, 1307, 1330, 1353, 1376, 1399, 1422, 1445, 1468, 1491, 1514, 1537, 1560, 1583, 1606, 1629, 1652, 1675, 1698, 1721, 1744, 1767, 1790, 1813, 1836, 1859, 1882, 1905, 1928, 1951, 1974, 1997, 2020, 2043, 2066, 2089, 2112, 2135, 2158, 2181, 2204, 2227, 2250, 2273, 2296, 2319, 2342, 2365, 2388, 2411, 2434, 2457, 2480, 2503, 2526, 2549, 2572, 2595, 2618, 2641, 2664, 2687, 2710, 2733, 2756, 2779, 2802, 2825, 2848, 2871, 2894, 2917, 2940, 2963, 2986, 3009, 3032, 3055, 3078, 3101, 3124, 3147, 3170, 3193, 3216, 3239, 3262, 3285, 3308, 3331, 3354, 3377, 3400, 3423, 3446, 3469, 3492, 3515, 3538, 3561, 3584, 3607, 3630, 3653, 3676, 3699, 3722, 3745, 3768, 3791, 3814, 3837, 3860, 3883, 3906, 3929, 3952, 3975, 3998, 4021, 4044, 4067, 4090, 4113, 4136, 4159, 4182, 4205, 4228, 4251, 4274, 4297, 4320, 4343, 4366, 4389, 4412, 4435, 4458, 4481, 4504, 4527, 4550, 4573, 4596, 4619, 4642, 4665, 4688, 4711, 4734, 4757, 4780, 4803, 4826, 4849, 4872, 4895, 4918, 4941, 4964, 4987, 5010, 5033, 5056, 5079, 5102, 5125, 5148, 5171, 5194, 5217, 5240, 5263, 5286, 5309, 5332, 5355, 5378, 5401, 5424, 5447, 5470, 5493, 5516, 5539, 5562, 5585, 5608, 5631, 5654, 5677, 5700, 5723, 5746, 5769, 5792]

# quit()


run_samples_and_actual([
# Part 1
r"""
9 100
""",
r"""
10 players; last marble is worth 1618 points
""",r"""
13 players; last marble is worth 7999 points
""",r"""
17 players; last marble is worth 1104 points
""",r"""
21 players; last marble is worth 6111 points
""",r"""
30 players; last marble is worth 5807 points
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
