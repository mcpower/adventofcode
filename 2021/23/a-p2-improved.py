import sys; sys.dont_write_bytecode = True; from utils import *

WAITING_AREAS = [
    (1, x)
    for x in [1, 2, 4, 6, 8, 10, 11]
]

WAITING_ROW = 1
WAITING_COLS = [1, 2, 4, 6, 8, 10, 11]
COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

ROOM_COLS = [3,5,7,9]

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    FINAL_NODE = tuple()


    def expand(node):
        # (weight, node)
        out = []

        # node should store waiting areas + rooms
        cur_waitings, cur_rooms = node

        if all(all(chr(ord('A')+i) == x for x in room) for i, room in enumerate(cur_rooms)):
            return [(0, FINAL_NODE)]
        
        def is_blocked(col_1, col_2):
            if col_1 > col_2:
                col_1, col_2 = col_2, col_1
            for blocked_col in range(col_1+1, col_2):
                if blocked_col in WAITING_COLS and cur_waitings[WAITING_COLS.index(blocked_col)] != "":
                    return True
            return False
        
        for room_idx, room in enumerate(cur_rooms):
            # find the thing to move
            for room_position, to_move in enumerate(room):
                if to_move == "":
                    continue
                to_move_row = 2+room_position
                break
            else:
                continue
            for waiting_idx, waiting_col in enumerate(WAITING_COLS):
                if cur_waitings[waiting_idx] == "":
                    if is_blocked(waiting_col, ROOM_COLS[room_idx]):
                        continue

                    # have this person move over there
                    new_waitings = list(cur_waitings)
                    new_rooms = list(map(list, cur_rooms))

                    cost = pdist1((to_move_row, ROOM_COLS[room_idx]), (WAITING_ROW, waiting_col)) * COST[to_move]
                    new_waitings[waiting_idx] = to_move
                    new_rooms[room_idx][room_position] = ""
                    out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))
        
        # move from waiting to room
        for waiting_idx, waiting_col in enumerate(WAITING_COLS):
            # find the thing to move
            to_move = cur_waitings[waiting_idx]
            if to_move == "":
                continue
            target_room_idx = ord(to_move) - ord('A')
            target_room = cur_rooms[target_room_idx]
            # NEED to there
            if target_room[0] == "" and all(x == "" or x == to_move for x in target_room[1:]):
                # move in
                room_col = ROOM_COLS[target_room_idx]
                # go back
                for room_position in range(len(target_room))[::-1]:
                    if target_room[room_position] != "":
                        continue
                    room_row = room_position + 2
                    break
                else:
                    assert False

                if is_blocked(waiting_col, room_col):
                    continue
                
                cost = pdist1((room_row, room_col), (WAITING_ROW, waiting_col)) * COST[to_move]

                new_waitings = list(cur_waitings)
                new_rooms = lmap(list, cur_rooms)

                new_waitings[waiting_idx] = ""
                new_rooms[target_room_idx][room_position] = to_move
                # out.append((cost, (new_waitings, new_rooms)))
                out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))

        return out
    

    # extract words
    rooms = []
    PART2 = ["DD", "CB", "BA", "AC"]
    for i,room_col in enumerate(ROOM_COLS):
        a, b = [lines[row][room_col] for row in [2, 3]]

        rooms.append(tuple(a+PART2[i]+b))
        # rooms.append(tuple(a+b))
    rooms = tuple(rooms)
    print(rooms)
    waitings = ("",)*len(WAITING_AREAS)

    out, _ =a_star((waitings, rooms), expand, FINAL_NODE)

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
