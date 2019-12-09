use std::collections::{HashSet, HashMap};
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
    // attempting to set IP to something OOB
    // includes "instruction was successfully executed and the IP now points past the end"
    OOBIPWrite(Int),
    // trying to read a parameter of an instruction OOB
    // example: 1,0,0
    OOBParameterRead(usize),
    // trying to read an argument of an instruction OOB
    // example: 1,100,0,0,99
    OOBArgumentsRead(Int),
    // trying to write an result of an instruction OOB
    // example: 1,0,0,100,99
    OOBResultWrite(Int),
}

type ICResult<T> = Result<T, ICException>;

#[derive(Debug)]
struct ICOutput {
    result: ICResult<ICSuccess>,
    output: Vec<Int>,
    inputs_consumed: usize,
}

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

fn to_usize(i: Int) -> Option<usize> {
    usize::try_from(i).ok()
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
        let out = self
            .get_mem(memory_index);
        let out = match get_mode(full_opcode, i as u32) {
            0 => self.get_mem(to_usize(out).ok_or(Exception(OOBArgumentsRead(out)))?),
            1 => out,
            2 => {
                let blah = to_usize(self.base + out).ok_or(Exception(OOBArgumentsRead(out)))?;
                self.get_mem(blah)
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
        match get_mode(full_opcode, i as u32) {
            0 => {
                let address = self
                    .get_mem(memory_index);
                let idx = to_usize(address).ok_or(Exception(OOBResultWrite(address)))?;
                Ok(self.get_mem_mut(idx))
            }
            1 => Ok(self.get_mem_mut(memory_index)),
            2 => {
                let offset = self
                    .get_mem(memory_index);
                let idx = to_usize(self.base + offset).ok_or(Exception(OOBResultWrite(offset)))?;
                Ok(self.get_mem_mut(idx))
            }
            _ => Err(Exception(UnknownOpcode(full_opcode))),
        }
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
                let new_ip = self.ip + 4;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                *self.get_arg_mut(3)? = self.get_arg(1)? + self.get_arg(2)?;
                self.ip = new_ip;
            }
            // multiply
            2 => {
                let new_ip = self.ip + 4;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                *self.get_arg_mut(3)? = self.get_arg(1)? * self.get_arg(2)?;
                self.ip = new_ip;
            }
            // get input
            3 => {
                let new_ip = self.ip + 2;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                *self.get_arg_mut(1)? = *input.ok_or(NeedInput)?;
                self.ip = new_ip;
                return Ok(InputConsumed);
            }
            // output
            4 => {
                let new_ip = self.ip + 2;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                let out = self.get_arg(1)?;
                self.ip = new_ip;
                return Ok(Output(out));
            }
            // jump if true
            5 => {
                let new_ip = if self.get_arg(1)? != 0 {
                    let new_ip_int = self.get_arg(2)?;
                    to_usize(new_ip_int).ok_or(Exception(OOBIPWrite(new_ip_int)))?
                } else {
                    self.ip + 3
                };
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                self.ip = new_ip;
            }
            // jump if false
            6 => {
                let new_ip = if self.get_arg(1)? == 0 {
                    let new_ip_int = self.get_arg(2)?;
                    to_usize(new_ip_int).ok_or(Exception(OOBIPWrite(new_ip_int)))?
                } else {
                    self.ip + 3
                };
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                self.ip = new_ip;
            }
            // less than
            7 => {
                let new_ip = self.ip + 4;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                *self.get_arg_mut(3)? = (self.get_arg(1)? < self.get_arg(2)?) as Int;
                self.ip = new_ip;
            }
            // equals
            8 => {
                let new_ip = self.ip + 4;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                *self.get_arg_mut(3)? = (self.get_arg(1)? == self.get_arg(2)?) as Int;
                self.ip = new_ip;
            }
            9 => {
                let new_ip = self.ip + 2;
                if new_ip >= self.memory.len() {
                    return Err(Exception(OOBIPWrite(new_ip as Int)));
                }
                self.base += self.get_arg(1)?;
                self.ip = new_ip;
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
        use ICStepSuccess::*;
        use ICStepFailure::*;
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
                        Exception(exception) => Err(exception)
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
        ICProgram {
            memory: nums.to_vec(),
            oob: HashMap::new(),
            ip: 0,
            halted: false,
            base: 0,
        }
    }

    fn from_str(inp: &str) -> ICProgram {
        ICProgram {
            memory: inp.trim().split(',').map(|s| s.parse().unwrap()).collect(),
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
    let mut program = ICProgram::from_str(inp);
    let mut blah = dbg!(program.run_single(1));
    blah.output.pop().unwrap().to_string()
}

#[aoc(day09, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let mut program = ICProgram::from_str(inp);
    let mut blah = dbg!(program.run_single(2));
    blah.output.pop().unwrap().to_string()
}

#[test]
fn day09samples() {
    assert_eq!(ICProgram::new(&[104,1125899906842624,99]).run_no_input().output, &[1125899906842624]);
    assert!(ICProgram::new(&[1102,34915192,34915192,7,4,7,99,0]).run_no_input().output[0] > 1000_0000_0000_0000);
    let quine = &[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99];
    let x = ICProgram::new(quine).run_no_input();
}
