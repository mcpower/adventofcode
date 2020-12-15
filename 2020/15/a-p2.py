import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    nums = ints(inp)

    last_seen = {x: i for i, x in enumerate(nums[:-1])}

    while len(nums) != 30000000:
        last = nums[-1]
        if last in last_seen:
            this = last_seen[nums[-1]]
            if this == len(nums) - 1:
                nums.append(0)
            else:
                nums.append(len(nums) - this - 1)
        else:
            nums.append(0)
        last_seen[nums[-2]] = len(nums) - 2
    print(nums[:10])
    print(nums[30000000-1])
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
0,3,6
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
