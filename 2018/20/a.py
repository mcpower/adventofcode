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

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    inp = inp.replace(" ", "")
    inp = inp[1:-1]

    # parse inp into a list of chars or lists
    pos = 0
    def parse():
        nonlocal pos
        # stop on | or ) or EOF
        out = []
        while pos < len(inp) and inp[pos] not in "|)":
            chunk = parse_chunk()
            sprint("chunk", chunk)
            out.append(chunk)
        # if pos < len(inp):
        #     sprint(pos, inp[pos])
        return tuple(out)

    def parse_chunk():
        # parses either some parentheses, or some characters
        nonlocal pos
        if inp[pos] == "|":
            return ""
        if inp[pos] == ")":
            assert False
        if inp[pos] == "(":
            out = []
            while inp[pos] != ")":
                pos += 1
                out.append(parse())
            pos += 1
            return tuple(out)
        else:
            cur_string = ""
            while pos < len(inp) and inp[pos] not in "(|)":
                cur_string += inp[pos]
                pos += 1
            return cur_string
    
    actual_inp = parse()
    sprint(actual_inp)
    # return

    # actual_inp = inp.replace("^", "['").replace("$","']").replace("(","',[['").replace(")","']],'").replace("|","'],['")
    # # sprint(actual_inp)
    # actual_inp = eval(actual_inp.replace("[","(").replace("]",")"))
    # if isinstance(actual_inp, str):
    #     actual_inp = (actual_inp,)
    sprint(actual_inp)
    adj = defaultdict(set) # (x, y) -> list
    seen = dict()

    to_d = dict(zip("NESW", [(-1, 0), (0, 1), (1, 0), (0, -1)]))
    
    def connect(a, b):
        nonlocal adj
        if b in adj[a]: return
        adj[a].add(b)
        adj[b].add(a)

    
    def f(p, l):
        # returns a LIST OF POSITIONS
        seen_thing = (tuple(p), l)
        if seen_thing in seen:
            return seen[seen_thing]
        
        positions = set([p])

        def make_new_positions(positions, part):
            positions = set(positions)
            if isinstance(part, str):
                new_positions = set()
                for c in part:
                    for pos in positions:
                        new_pos = tuple(padd(pos, to_d[c]))
                        connect(pos, new_pos)
                        new_positions.add(new_pos)
                    positions = new_positions
                    new_positions = set()
            else:
                new_positions = set(thing for pos in positions for option in part for thing in f(pos, option))
                # sprint("asd", new_positions)
                positions = new_positions
            return positions

        for part in l:
            positions = make_new_positions(positions, part)

        seen[seen_thing] = positions
        return positions

    f((0, 0), actual_inp)
    sprint(actual_inp)
    # if sample:
    #     pprint(adj)
    # quit()
    sprint("asdasdasda", adj[(1, -1)])

    seen = set()
    todo = [(0, 0)]
    to_dist = dict()
    c = 0
    while todo:
        new_todo = []
        for i in todo:
            if i in seen:
                continue
            to_dist[i] = c
            seen.add(i)
            new_todo.extend(x for x in adj[i] if x not in seen)
        if not new_todo:
            break
        todo = new_todo
        c += 1
        # sprint(todo)
    # sprint(seen)
    # sprint(set(adj))
    print(c)
    print(sum(i >= 1000 for i in to_dist.values()))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
^WNE$
""",r"""
^ENWWW(NEEE|SSE(EE|N))$
""",r"""
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
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
