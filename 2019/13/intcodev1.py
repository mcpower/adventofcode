from collections import defaultdict
from typing import DefaultDict, List, Optional, Tuple
import operator

class Intcode:
    memory: DefaultDict[int, int]
    ip: int
    base: int
    halted: bool

    BIN_OPS = {
        1: operator.add,
        2: operator.mul,
        7: lambda a, b: int(a < b),
        8: lambda a, b: int(a == b),
    }

    JUMP_OPS = {
        5: bool,
        6: operator.not_,
    }

    def __init__(self, memory: List[int]) -> None:
        self.memory = defaultdict(int, enumerate(memory))
        self.ip = 0
        self.base = 0
        self.halted = False
    
    def debug_negative_index(self, i: int) -> None:
        print("debug memory addresses:")
        print(self.memory[self.ip])
        print(self.memory[self.ip+1])
        print(self.memory[self.ip+2])
        print(self.memory[self.ip+3])
        print("debug index:")
        print(i)
    
    def __getitem__(self, i: int) -> int:
        if i < 0:
            self.debug_negative_index(i)
            raise IndexError("negative index")
        return self.memory[i]
    
    def __setitem__(self, i: int, item: int) -> int:
        if i < 0:
            self.debug_negative_index(i)
            raise IndexError("negative index")
        self.memory[i] = item
    
    def addr(self, param: int) -> int:
        out = self.ip + param
        mode = (self.memory[self.ip] // pow(10, param + 2 - 1)) % 10
        if mode == 0:
            out = self[out]
        elif mode == 1:
            pass
        elif mode == 2:
            out = self[out] + self.base
        else:
            raise Exception("bad mode")
        return out
    
    def run(self, inp: Optional[int] = None) -> Tuple[bool, List[int]]:
        if self.halted:
            raise Exception("already halted")
        out = []
        while True:
            op = self.memory[self.ip] % 100
            if op in Intcode.BIN_OPS:
                self[self.addr(3)] = Intcode.BIN_OPS[op](self[self.addr(1)], self[self.addr(2)])
                self.ip += 4
            elif op == 3:
                if inp is None:
                    return (False, out)
                self[self.addr(1)] = inp
                inp = None
                self.ip += 2
            elif op == 4:
                out.append(self[self.addr(1)])
                self.ip += 2
            elif op in Intcode.JUMP_OPS:
                if Intcode.JUMP_OPS[op](self[self.addr(1)]):
                    self.ip = self[self.addr(2)]
                else:
                    self.ip += 3
            elif op == 9:
                self.base += self[self.addr(1)]
                self.ip += 2
            elif op == 99:
                self.halted = True
                return (True, out)
            else:
                raise Exception("invalid opcode " + str(op))
