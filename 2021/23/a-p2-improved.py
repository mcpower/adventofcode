import sys; sys.dont_write_bytecode = True; from utils import *

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

        # I wrote this line of code first, before doing anything else
        # with the problem.
        cur_waitings, cur_rooms = node

        if all(all(chr(ord('A')+i) == x for x in room) for i, room in enumerate(cur_rooms)):
            return [(0, FINAL_NODE)]
        
        def is_blocked(col_1, col_2):
            if col_1 > col_2:
                col_1, col_2 = col_2, col_1
            for blocked_col in range(col_1+1, col_2):
                # This could really be improved...
                if blocked_col in WAITING_COLS and cur_waitings[WAITING_COLS.index(blocked_col)] != "":
                    return True
            return False
        
        # Move from a room to a waiting spot.
        for room_idx, room in enumerate(cur_rooms):
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

                    new_waitings = list(cur_waitings)
                    new_rooms = list(map(list, cur_rooms))

                    cost = pdist1((to_move_row, ROOM_COLS[room_idx]), (WAITING_ROW, waiting_col)) * COST[to_move]
                    new_waitings[waiting_idx] = to_move
                    new_rooms[room_idx][room_position] = ""
                    out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))
        
        # Move from a waiting spot to a room.
        for waiting_idx, waiting_col in enumerate(WAITING_COLS):
            to_move = cur_waitings[waiting_idx]
            if to_move == "":
                continue

            target_room_idx = ord(to_move) - ord('A')
            target_room = cur_rooms[target_room_idx]

            if target_room[0] == "" and all(x == "" or x == to_move for x in target_room[1:]):
                for room_position in range(len(target_room))[::-1]:
                    if target_room[room_position] != "":
                        continue
                    room_row = room_position + 2
                    break
                else:
                    assert False

                room_col = ROOM_COLS[target_room_idx]
                if is_blocked(waiting_col, room_col):
                    continue
                
                cost = pdist1((room_row, room_col), (WAITING_ROW, waiting_col)) * COST[to_move]

                new_waitings = list(cur_waitings)
                new_rooms = list(map(list, cur_rooms))

                new_waitings[waiting_idx] = ""
                new_rooms[target_room_idx][room_position] = to_move
                out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))

        return out
    

    rooms = []
    PART2 = ["DD", "CB", "BA", "AC"]
    for i,room_col in enumerate(ROOM_COLS):
        a, b = [lines[row][room_col] for row in [2, 3]]

        rooms.append(tuple(a+PART2[i]+b))
        # Replace the above with the below for part 1.
        # This also came in handy for testing my generalised part 2 code
        # to make sure that it works with part 1.
        # rooms.append(tuple(a+b))
    rooms = tuple(rooms)
    print(rooms)
    waitings = ("",)*len(WAITING_COLS)

    # "A*" here is actually "Dijkstra, with a target node".
    # My internal implementation also returns a path from start to finish,
    # but I don't use it here.
    out, _ = a_star((waitings, rooms), expand, FINAL_NODE)

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
