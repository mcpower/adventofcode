import sys; sys.dont_write_bytecode = True; from utils import *

TARGET = r"""#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""

WAITING_AREAS = [
    (1, x)
    for x in [1, 2, 4, 6, 8, 10, 11]
]

WTF = [1, 2, 4, 6, 8, 10, 11]

ROOM_COLS = [3,5,7,9]

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    FINAL_NODE = tuple()

    COST={"A":1,"B":10,"C":100,"D":1000}

    def expand(node):
        # (weight, node)
        out = []

        # node should store waiting areas + rooms
        cur_waitings, cur_rooms = node

        # waitings is a list of None or string
        if cur_rooms == (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")):
            return [(0, FINAL_NODE)]
        
        for i, room in enumerate(cur_rooms):
            # find the thing to move
            # sprint(room)
            first, second = room
            if first == "":
                if second == "":
                    continue
                else:
                    to_move = second
                    to_move_coord = (3, ROOM_COLS[i])
                    room_idx = 1
            else:
                to_move = first
                to_move_coord = (2, ROOM_COLS[i])
                room_idx = 0
            for j, waiting_area in enumerate(WAITING_AREAS):
                if cur_waitings[j] == "":
                    # CHECK IF BLOCKED OFF.
                    c1, c2 = waiting_area[1], to_move_coord[1]
                    if c1 > c2:
                        c1, c2 = c2, c1
                    bad = False
                    for col in range(c1+1, c2):
                        if col in WTF and cur_waitings[WTF.index(col)] != "":
                            bad = True
                            break
                    if bad:
                        continue

                    # have this person move over there
                    new_waitings = list(cur_waitings)
                    new_rooms = lmap(list, cur_rooms)

                    cost = pdist1(to_move_coord, waiting_area) * COST[to_move]
                    new_waitings[j] = to_move
                    new_rooms[i][room_idx] = ""
                    out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))
        
        # move from waiting to room
        for j, waiting_area in enumerate(WAITING_AREAS):
            to_move = cur_waitings[j]
            if to_move == "":
                continue
            target_room = ord(to_move) - ord('A')
            target_room_actual = cur_rooms[target_room]
            # first, then second
            if target_room_actual[0] == "" and (target_room_actual[1] == "" or target_room_actual[1] == to_move):
                # move in
                col = ROOM_COLS[target_room]
                if target_room_actual[1] == "":
                    # move to second
                    row = 3
                    room_idx = 1
                else:
                    row = 2
                    room_idx = 0

                # CHECK IF BLOCKED OFF.
                c1, c2 = waiting_area[1], col
                if c1 > c2:
                    c1, c2 = c2, c1
                bad = False
                for col2 in range(c1+1, c2):
                    if col2 in WTF and cur_waitings[WTF.index(col2)] != "":
                        bad = True
                        break
                if bad:
                    continue
                
                cost = pdist1((row, col), waiting_area) * COST[to_move]

                new_waitings = list(cur_waitings)
                new_rooms = lmap(list, cur_rooms)

                new_waitings[j] = ""
                new_rooms[target_room][room_idx] = to_move
                # out.append((cost, (new_waitings, new_rooms)))
                out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))



        return out
    

    # extract words
    rooms = []
    for room_col in ROOM_COLS:
        rooms.append(tuple(lines[row][room_col] for row in [2, 3]))
    rooms = tuple(rooms)
    print(rooms)
    waitings = ("",)*len(WAITING_AREAS)

    out, path=a_star((waitings, rooms), expand, FINAL_NODE)
    for p in path:
        pprint(p)

    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
