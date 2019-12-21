import sys; sys.dont_write_bytecode = True; from utils import *
from intcodev1 import *
def do_case(inp: str, sample=False):
    def sprint(*a, **k): sample and print(*a, **k)
    prog = Intcode(ints(inp))

    MY_PROG = """
NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
NOT D T
NOT T T
AND T J
NOT E T
NOT T T
OR H T
AND T J
RUN
""".strip()
    halted, output = prog.run_ascii(MY_PROG)
    Intcode.print_output(output)

run_samples_and_actual([],[], do_case)
