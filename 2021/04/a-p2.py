import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    numbers, *boards = paras
    sprint(repr(numbers))
    numbers = ints(numbers)

    b = []
    for board in boards:
        b.append([[[x, False]for x in ints(line)] for line in board.splitlines()])
    
    def check(board):
        # sprint(board)
        for line in board:
            # sprint(line)
            if all(c for _, c in line):
                return True
        return False
    
    for number in numbers:
        for board in b:
            for row in board:
                for i in range(5):
                    if row[i][0] == number:
                        row[i][1] = True
        new_b = []            
        for board in b:
            if check(board) or check(list(zip(*board))):
                if len(b) != 1:
                    pass
                else:
                    out = number * sum(x for row in board for x, y in row if not y)
                    print(out)
                    return
            else:
                new_b.append(board)
        b = new_b
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
