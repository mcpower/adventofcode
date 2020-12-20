from re import L
import sys; sys.dont_write_bytecode = True; from utils import *

MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip("\n").splitlines()

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    # Editor's note: Each tile has four edges:
    #      0
    #    ---->
    #   |     |
    # 2 |     | 3
    #   v     v
    #    ---->
    #      1
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    edge_to_id_and_pos = defaultdict(list)
    id_to_tile = dict()
    id_to_unclean = dict()

    def clean(s):
        return min(s, s[::-1])

    for tile in paras:
        q, *thing = tile.splitlines()
        id = ints(q)[0]
        id_to_tile[id] = thing
        id_to_unclean[id] = []
        id_to_unclean[id].append((thing[0]))
        id_to_unclean[id].append((thing[-1]))
        edge_to_id_and_pos[clean(thing[0])].append((id, 0))
        edge_to_id_and_pos[clean(thing[-1])].append((id, 1))
        
        thing = ["".join(x) for x in zip(*thing)]
        edge_to_id_and_pos[clean(thing[0])].append((id, 2))
        edge_to_id_and_pos[clean(thing[-1])].append((id, 3))
        id_to_unclean[id].append((thing[0]))
        id_to_unclean[id].append((thing[-1]))
    
    thingy = []

    for key in edge_to_id_and_pos:
        asdf = edge_to_id_and_pos[key]
        if len(asdf) == 1:
            thingy.extend(map(fst,asdf))
    
    map_of_tiles = [] # type: list[list[list[str]]]
    
    # randomly pick a corner
    corner_id = collections.Counter(thingy).most_common(1)[0][0]
    corner_tile = id_to_tile[corner_id]
    # randomly pick an orientation for the actual corner
    corner_edges = [(edge, edge_num) for edge_num, edge in enumerate(id_to_unclean[corner_id]) if len(edge_to_id_and_pos[clean(edge)]) == 1]
    # align those two corner edges with 0 and 2

    # rotate + flip
    # rotate to 0 / 2 or 3
    # then flip if necessary

    def rotate_edge_clockwise(a):
        # sprint(a)
        if a == 0:
            return 3
        if a == 3:
            return 1
        if a == 1:
            return 2
        assert a == 2
        return 0
    
    def transpose(tile):
        return ["".join(x) for x in zip(*tile)]

    def rotate_clockwise(tile):
        return [row[::-1] for row in transpose(tile)]
    
    def flip_left_right(tile):
        return [row[::-1] for row in tile]
    
    def flip_up_down(tile):
        return tile[::-1]
    
    done = set()
    del tile
    
    
    while corner_edges[0][1] != 0:
        # print(corner_edges)
        # print("\n".join(corner_tile))
        # print()
        corner_edges = [(edge, rotate_edge_clockwise(num)) for edge, num in corner_edges]
        corner_edges = [(edge[::-1] if num in [2, 3] else edge, num) for edge, num in corner_edges]
        # sprint(corner_edges)
        corner_tile = rotate_clockwise(corner_tile)
    
    if corner_edges[1][1] == 3:
        corner_edges = [corner_edges[0]] + [(corner_edges[1][0], 2)]
        corner_tile = flip_left_right(corner_tile)

    assert corner_edges[1][1] == 2

    # def to_hash(tile):
    #     return "\n".join(tile)

    print(corner_edges)
    # sprint(id_to_tile)

    map_of_tiles.append([])
    map_of_tiles[0].append(corner_tile)
    done.add(corner_id)

    def get_3(tile):
        return "".join(x[-1] for x in tile)
    
    def get_1(tile):
        return tile[-1]
    
    def get_2(tile):
        return "".join(x[0] for x in tile)
    # sprint(rotate_clockwise(["12", "34"]))
    # sprint(map_of_tiles)
    from pprint import pprint
    # pprint(edge_to_id_and_pos)
    def fill_row():
        # fill out current row
        row = map_of_tiles[-1]

        while True:
            cur_three = get_3(row[-1])
            # pprint(row[-1])
            things = edge_to_id_and_pos[clean(cur_three)]
            # pprint(cur_three)
            # sprint("adding")
            if len(things) == 1:
                # sprint("breaking")
                break
            # sprint(done, things)
            for new_id, pos in things:
                if new_id in done:
                    continue
                break
            else:
                assert False
            
            new_tile = id_to_tile[new_id]
            # pprint(new_tile)
            # pprint(pos)

            
            # rotate
            while pos != 2:
                new_tile = rotate_clockwise(new_tile)
                pos = rotate_edge_clockwise(pos)
            # pprint(new_tile)

            receiving_edge = get_2(new_tile)
            if receiving_edge != cur_three:
                receiving_edge = receiving_edge[::-1]
                new_tile = flip_up_down(new_tile)
            assert receiving_edge == cur_three
            row.append(new_tile)
            assert new_id not in done
            done.add(new_id)

    def new_row():
        last = map_of_tiles[-1][0]
        last_1 = get_1(last)
        things = edge_to_id_and_pos[clean(last_1)]
        if len(things) == 1:
            return False
        
        for new_id, pos in things:
            if new_id in done:
                continue
            break
        else:
            assert False
        
        new_tile = id_to_tile[new_id]
        sprint(done, things)

            
        # rotate
        while pos != 0:
            new_tile = rotate_clockwise(new_tile)
            pos = rotate_edge_clockwise(pos)

        receiving_edge = new_tile[0]
        if receiving_edge != last_1:
            receiving_edge = receiving_edge[::-1]
            new_tile = flip_left_right(new_tile)
        assert receiving_edge == last_1
        map_of_tiles.append([new_tile])
        
        assert new_id not in done
        done.add(new_id)
        
        return True
    
    fill_row()
    while new_row():
        fill_row()
    
    assert len(done) == len(paras)


    
    # create the map, strip thingy.
    def strip(tile):
        return [row[1:-1] for row in tile[1:-1]]
    
    stripped = [lmap(strip, row) for row in map_of_tiles]

    def join_row(row_of_tiles):
        return ["".join(x) for x in zip(*row_of_tiles)]
    
    many_rows = lmap(join_row, stripped)
    final = flatten(many_rows)

    def count_monster(big):
        monster_rows = len(MONSTER)
        monster_cols = len(MONSTER[0])
        big_rows = len(big)
        big_cols = len(big[0])
        out = 0
        not_part = [[col == "#" for col in row]for row in big]
        for row in range(big_rows):
            if row + monster_rows > big_rows:
                break
            for col in range(len(big[0])):
                if col + monster_cols > big_cols:
                    break
                
                bad = False
                # try it out
                for monster_row in range(monster_rows):
                    for monster_col in range(monster_cols):
                        in_big = big[row + monster_row][col + monster_col]
                        in_monster = MONSTER[monster_row][monster_col]
                        if in_monster == "#" and in_big != "#":
                            bad = True
                if not bad:
                    out += 1
                    for monster_row in range(monster_rows):
                        for monster_col in range(monster_cols):
                            in_big = big[row + monster_row][col + monster_col]
                            in_monster = MONSTER[monster_row][monster_col]
                            if in_monster == "#":
                                not_part[row + monster_row][col + monster_col] = False
        if out:
            return sum(map(sum, not_part))
        return out
    
    outs = []
    for rotate in range(4):
        flipped = flip_left_right(final)
        outs.append(count_monster(final))
        outs.append(count_monster(flipped))
        final = rotate_clockwise(final)
    print(outs)
    

    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
