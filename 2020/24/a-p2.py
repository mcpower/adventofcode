import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    flipped = set()

    EVEN_ROW = {
        "e": (1, 0),
        "w": (-1, 0),
        "se": (0, 1),
        "sw": (-1, 1),
        "ne": (0, -1),
        "nw": (-1, -1),
    }

    ODD_ROW = {
        "e": (1, 0),
        "w": (-1, 0),
        "se": (+1, +1),
        "sw": (0, 1),
        "ne": (1, -1),
        "nw": (0, -1),
    }

    for line in lines:
        point = (0, 0)

        i = 0
        while i < len(line):
            c = line[i]
            if c == "s" or c == "n":
                c += line[i+1]
                i += 1
            
            if point[1] % 2 == 0:
                point = padd(point, EVEN_ROW[c])
            else:
                point = padd(point, ODD_ROW[c])


            i += 1
        
        assert i == len(line)

        point = tuple(point)
        if point in flipped:
            flipped.remove(point)
            # sprint("removed")
        else:
            flipped.add(point)
    

    def get_adj(point):
        if point[1] % 2 == 0:
            blah = EVEN_ROW
        else:
            blah = ODD_ROW
        out = []
        for delta in blah.values():
            out.append(tuple(padd(point, delta)))
        return out
    
    for _ in range(100):
        point_to_neighbours = defaultdict(int)

        for point in flipped:
            point_to_neighbours[point]
            for adj in get_adj(point):
                point_to_neighbours[adj] += 1
        
        new_flipped = set()
        
        for point in point_to_neighbours:
            neigh = point_to_neighbours[point]

            if point in flipped:
                if neigh == 0 or neigh > 2:
                    ...
                else:
                    new_flipped.add(point)
            else:
                if neigh == 2:
                    new_flipped.add(point)
        
        flipped = new_flipped
        

    
    out = len(flipped)
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
