import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    cards = 119315717514047
    repeats = 101741582076661

    def inv(n):
        # gets the modular inverse of n
        # as cards is prime, use Euler's theorem
        return pow(n, cards-2, cards)
    def get(offset, increment, i):
        # gets the ith number in a given sequence
        return (offset + i * increment) % cards
    
    # increment = 1 = the difference between two adjacent numbers
    # doing the process will multiply increment by increment_mul.
    increment_mul = 1
    # offset = 0 = the first number in the sequence.
    # doing the process will increment this by offset_diff * (the increment before the process started).
    offset_diff = 0
    for line in inp.splitlines():
        if line == "deal into new stack":
            # reverse sequence.
            # instead of going up, go down.
            increment_mul *= -1
            increment_mul %= cards
            # then shift 1 left
            offset_diff += increment_mul
            offset_diff %= cards
        elif line.startswith("cut"):
            q, *_ = ints(line)
            # shift q left
            offset_diff += q * increment_mul
            offset_diff %= cards
        elif line.startswith("deal with increment "):
            q, *_ = ints(line)
            # difference between two adjacent numbers is multiplied by the
            # inverse of the increment.
            increment_mul *= inv(q)
            increment_mul %= cards

    def get_sequence(iterations):
        # calculate (increment, offset) for the number of iterations of the process
        # increment = increment_mul^iterations
        increment = pow(increment_mul, iterations, cards)
        # offset = 0 + offset_diff * (1 + increment_mul + increment_mul^2 + ... + increment_mul^iterations)
        # use geometric series.
        offset = offset_diff * (1 - increment) * inv((1 - increment_mul) % cards)
        offset %= cards
        return increment, offset

    increment, offset = get_sequence(repeats)
    print(get(offset, increment, 2020))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([], [], do_case)
