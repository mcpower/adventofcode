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
    
    def doit(boost):
        lines = inp.splitlines()
        immune, infection = inp.split("\n\n")

        teams = []

        REGEX = re.compile(r"(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)")

        UNITS, HP, DAMAGE, DTYPE, FAST, IMMUNE, WEAK = range(7)

        blah = boost
        for inps in [immune, infection]:
            lines = inps.splitlines()[1:]
            team = []
            for line in lines:
                s = REGEX.match(line)
                # print(s.groups())
                units, hp, extra, damage, dtype, fast = s.groups()
                immune = []
                weak = []
                if extra:
                    extra = extra.rstrip(" )").lstrip("(")
                    for s in extra.split("; "):
                        if s.startswith("weak to "):
                            weak = s[len("weak to "):].split(", ")
                            # print(weak)
                            # quit()
                        elif s.startswith("immune to "):
                            immune = s[len("immune to "):].split(", ")
                        else:
                            assert False
                u = [int(units), int(hp), int(damage) + blah, dtype, int(fast), set(immune), set(weak)]
                # print(u)
                team.append(u)
            teams.append(team)
            blah = 0
        
        def power(t):
            return t[UNITS] * t[DAMAGE]
        

        def damage(attacking, defending):
            mod = 1
            if attacking[DTYPE] in defending[IMMUNE]:
                mod = 0
            elif attacking[DTYPE] in defending[WEAK]:
                mod = 2
            return power(attacking) * mod
        
        def sort_key(attacking, defending):
            return (damage(attacking, defending), power(defending), defending[FAST])
        
        while all(not all(u[UNITS] <= 0 for u in team) for team in teams):
            # for x in teams:
            #     print([u[UNITS] for u in x])
            # if sample:
            #     pprint(teams)
            # new_teams = []

            teams[0].sort(key=power, reverse=True)
            teams[1].sort(key=power, reverse=True)

            targets = []

            # target selection
            for team_i in range(2):
                other_team_i = 1 - team_i
                team = teams[team_i]
                other_team = teams[other_team_i]

                remaining_targets = set(i for i in range(len(other_team)) if other_team[i][UNITS] > 0)
                my_targets = [None] * len(team)

                for i, t in enumerate(team):
                    if not remaining_targets:
                        break
                    best_target = max(remaining_targets, key= lambda i: sort_key(t, other_team[i]))
                    enemy = other_team[best_target]
                    if damage(t, enemy) == 0:
                        continue
                    my_targets[i] = best_target
                    remaining_targets.remove(best_target)
                targets.append(my_targets)
            
            # attacking
            attack_sequence = [(0, i) for i in range(len(teams[0]))] + [(1, i) for i in range(len(teams[1]))]
            attack_sequence.sort(key=lambda x: teams[x[0]][x[1]][FAST], reverse=True)
            did_damage = False
            for team_i, index in attack_sequence:
                to_attack = targets[team_i][index]
                if to_attack is None:
                    continue
                me = teams[team_i][index]
                other = teams[1-team_i][to_attack]

                d = damage(me, other)
                d //= other[HP]

                if teams[1-team_i][to_attack][UNITS] > 0 and d > 0:
                    did_damage = True

                teams[1-team_i][to_attack][UNITS] -= d
                teams[1-team_i][to_attack][UNITS] = max(teams[1-team_i][to_attack][UNITS], 0)
            if not did_damage:
                return None
                
            # teams = new_teams
        asd = sum([u[UNITS] for u in teams[0]])
        if asd == 0:
            return None
        else:
            return asd
    # I did a manual binary search, submitted the right answer, then added in did_damage.
    # WARNING: "doit" is not guaranteed to be monotonic!
    # print(doit(33))
    # return
    maybe = binary_search(doit)
    print(maybe)
    print(doit(maybe))

    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
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
