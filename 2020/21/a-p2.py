import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    d = []
    allergens = set()
    allergen_to_things = defaultdict(list)

    for line in lines:
        thing, contains = line.split(" (contains ")
        contains = contains.rstrip(")").split(", ")
        thing = set(thing.split())
        d.append([thing, contains])
        allergens.update(contains)
        for allergen in contains:
            allergen_to_things[allergen].append(thing)
    # sprint(allergen_to_things)
    # sprint(allergens)

    thing_to_allergen = {}
    allergen_to_thing = {}
    good = True
    while good:
        good = False
        for allergen in allergen_to_things:
            if allergen in thing_to_allergen:
                continue
            things = allergen_to_things[allergen]
            possible = functools.reduce(operator.__and__, map(frozenset,things))
            possible -= set(thing_to_allergen)
            # sprint(allergen, things, possible)
            if len(possible) == 1:
                thing_to_allergen[next(iter(possible))] = allergen
                allergen_to_thing[allergen] = next(iter(possible))
                good = True
    
    found = set(thing_to_allergen)
    for allergen in allergen_to_things:
        if allergen in thing_to_allergen:
            continue
        things = allergen_to_things[allergen]
        possible = functools.reduce(operator.__and__, map(frozenset,things))
        possible -= set(thing_to_allergen)
        found.update(possible)
        
    
    
    sprint(thing_to_allergen)
    for thing, contains in d:
        for x in thing:
            if x not in found:
                out+=1
    assert len(thing_to_allergen) == len(allergens)
    blah = [(thing_to_allergen[key], key) for key in thing_to_allergen]
    blah.sort()
    print(",".join(map(snd, blah)))

    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
