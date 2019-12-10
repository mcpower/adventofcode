use std::collections::HashMap;
use std::convert::TryFrom;

type Int = i64;

// an instruction was successfully executed
#[derive(PartialEq, Eq, Debug)]
enum ICStepSuccess {
    // input was read
    InputConsumed,
    // something was output
    Output(Int),
    // program was halted
    Halted,
    // everything is normal, can continue executing
    Success,
}

// an instruction was NOT executed
// memory and ip are guaranteed to not change
#[derive(PartialEq, Eq, Debug)]
enum ICStepFailure {
    // program needs more input
    NeedInput,
    Exception(ICException),
}

type ICStepResult<T> = Result<T, ICStepFailure>;

// many instructions were successfully executed
#[derive(PartialEq, Eq, Debug)]
enum ICSuccess {
    // currently waiting for more input
    AwaitingInput,
    // we halted
    Halt,
}

// something bad happened - state of program is now right before this exception
#[derive(PartialEq, Eq, Debug)]
enum ICException {
    // program was already halted before run() was called
    AlreadyHalted,
    // includes invalid addressing modes
    UnknownOpcode(Int),
    // attempting to set IP to something negative
    NegativeIPWrite(Int),
    // trying to read an argument from a negative index
    // example: 1,-1,0,0,99
    NegativeArgumentsRead(Int),
    // trying to write a result to a negative index
    // example: 1,0,0,-1,99
    NegativeResultWrite(Int),
}

type ICResult<T> = Result<T, ICException>;

#[derive(Debug)]
struct ICOutput {
    result: ICResult<ICSuccess>,
    output: Vec<Int>,
    inputs_consumed: usize,
}

#[allow(dead_code)]
impl ICOutput {
    fn is_halted(&self) -> bool {
        self.result == Ok(ICSuccess::Halt)
    }

    fn is_awaiting_input(&self) -> bool {
        self.result == Ok(ICSuccess::AwaitingInput)
    }

    fn is_error(&self) -> bool {
        match self.result {
            Err(_) => true,
            _ => false,
        }
    }
}

#[derive(Clone, Debug)]
struct ICProgram {
    memory: Vec<Int>,
    oob: HashMap<usize, Int>,
    ip: usize,
    halted: bool,
    base: Int,
}

#[allow(dead_code)]
fn to_usize(i: Int) -> Option<usize> {
    usize::try_from(i).ok()
}

fn to_usize_err(i: Int, err: impl Fn(Int) -> ICException) -> ICStepResult<usize> {
    usize::try_from(i).map_err(|_| ICStepFailure::Exception(err(i)))
}

fn get_mode(full_opcode: Int, i: u32) -> Int {
    (full_opcode / 10i64.pow(i + 2 - 1)) % 10
}

#[allow(dead_code)]
impl ICProgram {
    fn get_mem(&self, i: usize) -> Int {
        if let Some(x) = self.memory.get(i) {
            *x
        } else if let Some(x) = self.oob.get(&i) {
            *x
        } else {
            0
        }
    }

    fn get_mem_mut(&mut self, i: usize) -> &mut Int {
        if let Some(x) = self.memory.get_mut(i) {
            x
        } else {
            self.oob.entry(i).or_insert(0)
        }
    }

    fn get_arg(&self, i: usize) -> ICStepResult<Int> {
        use ICException::*;
        use ICStepFailure::*;
        let memory_index = self.ip + i;
        let full_opcode = self.get_mem(self.ip);
        let value = self.get_mem(memory_index);
        let out = match get_mode(full_opcode, i as u32) {
            0 => {
                let idx = to_usize_err(value, NegativeArgumentsRead)?;
                self.get_mem(idx)
            }
            1 => value,
            2 => {
                let address = self.base + value;
                let idx = to_usize_err(address, NegativeArgumentsRead)?;
                self.get_mem(idx)
            }
            _ => return Err(Exception(UnknownOpcode(full_opcode))),
        };
        Ok(out)
    }

    fn get_arg_mut(&mut self, i: usize) -> ICStepResult<&mut Int> {
        use ICException::*;
        use ICStepFailure::*;
        let memory_index = self.ip + i;
        let full_opcode = self.get_mem(self.ip);
        let out = match get_mode(full_opcode, i as u32) {
            0 => {
                let address = self.get_mem(memory_index);
                let idx = to_usize_err(address, NegativeResultWrite)?;
                self.get_mem_mut(idx)
            }
            1 => self.get_mem_mut(memory_index),
            2 => {
                let address = self.base + self.get_mem(memory_index);
                let idx = to_usize_err(address, NegativeResultWrite)?;
                self.get_mem_mut(idx)
            }
            _ => return Err(Exception(UnknownOpcode(full_opcode))),
        };
        Ok(out)
    }

    fn step(&mut self, input: Option<&Int>) -> ICStepResult<ICStepSuccess> {
        use ICException::*;
        use ICStepFailure::*;
        use ICStepSuccess::*;

        if self.halted {
            return Err(Exception(AlreadyHalted));
        }

        let full_opcode = self.get_mem(self.ip);

        match full_opcode % 100 {
            // add
            1 => {
                *self.get_arg_mut(3)? = self.get_arg(1)? + self.get_arg(2)?;
                self.ip += 4;
            }
            // multiply
            2 => {
                *self.get_arg_mut(3)? = self.get_arg(1)? * self.get_arg(2)?;
                self.ip += 4;
            }
            // get input
            3 => {
                *self.get_arg_mut(1)? = *input.ok_or(NeedInput)?;
                self.ip += 2;
                return Ok(InputConsumed);
            }
            // output
            4 => {
                let out = self.get_arg(1)?;
                self.ip += 2;
                return Ok(Output(out));
            }
            // jump if true
            5 => {
                self.ip = if self.get_arg(1)? != 0 {
                    to_usize_err(self.get_arg(2)?, NegativeIPWrite)?
                } else {
                    self.ip + 3
                };
            }
            // jump if false
            6 => {
                self.ip = if self.get_arg(1)? == 0 {
                    to_usize_err(self.get_arg(2)?, NegativeIPWrite)?
                } else {
                    self.ip + 3
                };
            }
            // less than
            7 => {
                *self.get_arg_mut(3)? = (self.get_arg(1)? < self.get_arg(2)?) as Int;
                self.ip += 4;
            }
            // equals
            8 => {
                *self.get_arg_mut(3)? = (self.get_arg(1)? == self.get_arg(2)?) as Int;
                self.ip += 4;
            }
            9 => {
                self.base += self.get_arg(1)?;
                self.ip += 2;
            }
            // halt
            99 => {
                self.halted = true;
                return Ok(Halted);
            }
            _ => {
                return Err(Exception(UnknownOpcode(full_opcode)));
            }
        }
        Ok(Success)
    }

    fn run(&mut self, input: &[Int]) -> ICOutput {
        use ICStepFailure::*;
        use ICStepSuccess::*;
        use ICSuccess::*;

        let mut output = vec![];
        let mut inputs_consumed = 0usize;

        loop {
            let step_result = self.step(input.get(inputs_consumed));
            match step_result {
                Ok(success) => match success {
                    InputConsumed => {
                        inputs_consumed += 1;
                    }
                    Output(out_value) => {
                        output.push(out_value);
                    }
                    Halted => {
                        return ICOutput {
                            result: Ok(Halt),
                            output,
                            inputs_consumed,
                        };
                    }
                    Success => {}
                },
                Err(failure) => {
                    let result = match failure {
                        NeedInput => Ok(AwaitingInput),
                        Exception(exception) => Err(exception),
                    };
                    return ICOutput {
                        result,
                        output,
                        inputs_consumed,
                    };
                }
            }
        }
    }

    fn run_single(&mut self, input: Int) -> ICOutput {
        self.run(&[input])
    }

    fn run_no_input(&mut self) -> ICOutput {
        self.run(&[])
    }

    fn new(nums: &[Int]) -> ICProgram {
        ICProgram::from_vec(nums.to_vec())
    }

    fn from_str(inp: &str) -> ICProgram {
        ICProgram::from_vec(inp.trim().split(',').map(|s| s.parse().unwrap()).collect())
    }

    fn from_vec(mut memory: Vec<Int>) -> ICProgram {
        memory.extend(std::iter::repeat(0).take(memory.len()));
        ICProgram {
            memory,
            oob: HashMap::new(),
            ip: 0,
            halted: false,
            base: 0,
        }
    }
}

#[aoc(day09, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    ICProgram::from_str(inp)
        .run_single(1)
        .output
        .pop()
        .unwrap()
        .to_string()
}

#[aoc(day09, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    ICProgram::from_str(inp)
        .run_single(2)
        .output
        .pop()
        .unwrap()
        .to_string()
}

#[test]
fn day09samples() {
    assert_eq!(
        ICProgram::new(&[104, 1_125_899_906_842_624, 99])
            .run_no_input()
            .output,
        &[1_125_899_906_842_624]
    );
    assert!(
        ICProgram::new(&[1102, 34_915_192, 34_915_192, 7, 4, 7, 99, 0])
            .run_no_input()
            .output[0]
            > 1000_0000_0000_0000
    );
    let quine = &[
        109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99,
    ];
    assert_eq!(ICProgram::new(quine).run_no_input().output, quine);
}
