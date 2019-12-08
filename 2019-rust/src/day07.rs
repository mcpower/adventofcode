use std::collections::HashSet;
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
    ip: usize,
    halted: bool,
}

fn to_usize(i: Int) -> Option<usize> {
    usize::try_from(i).ok()
}

fn get_mode(full_opcode: Int, i: u32) -> Int {
    (full_opcode / 10i64.pow(i + 2 - 1)) % 10
}

#[allow(dead_code)]
impl ICProgram {
    fn get_arg(&self, i: usize) -> ICStepResult<Int> {
        use ICException::*;
        use ICStepFailure::*;
        let memory_index = self.ip + i;
        let full_opcode = *self.memory.get(self.ip).expect("this should never happen");
        let out = self
            .memory
            .get(memory_index)
            .ok_or(Exception(OOBParameterRead(memory_index)))?;
        let out = match get_mode(full_opcode, i as u32) {
            0 => to_usize(*out)
                .and_then(|idx| self.memory.get(idx))
                .ok_or(Exception(OOBArgumentsRead(*out)))?,
            1 => out,
            _ => return Err(Exception(UnknownOpcode(full_opcode))),
        };
        Ok(*out)
    }

    fn get_arg_mut(&mut self, i: usize) -> ICStepResult<&mut Int> {
        use ICException::*;
        use ICStepFailure::*;
        let memory_index = self.ip + i;
        let full_opcode = *self.memory.get(self.ip).expect("this should never happen");
        match get_mode(full_opcode, i as u32) {
            0 => {
                let &address = self
                    .memory
                    .get(memory_index)
                    .ok_or(Exception(OOBParameterRead(memory_index)))?;
                to_usize(address)
                    .and_then(move |idx| self.memory.get_mut(idx))
                    .ok_or(Exception(OOBResultWrite(address)))
            }
            1 => self
                .memory
                .get_mut(memory_index)
                .ok_or(Exception(OOBParameterRead(memory_index))),
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

        let full_opcode = *self.memory.get(self.ip).expect("this should never happen");

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
            ip: 0,
            halted: false,
        }
    }

    fn from_str(inp: &str) -> ICProgram {
        ICProgram {
            memory: inp.trim().split(',').map(|s| s.parse().unwrap()).collect(),
            ip: 0,
            halted: false,
        }
    }
}

fn try_inputs(nums: &[Int], input: &[Int]) -> Option<Int> {
    let set = input.iter().cloned().collect::<HashSet<Int>>();
    if set.len() != input.len() {
        return None;
    }
    let mut programs: Vec<_> = std::iter::repeat(ICProgram::new(nums)).take(input.len()).collect();
    let mut last = 0;
    for (program, &phase) in programs.iter_mut().zip(input.iter()) {
        let mut output = program.run(&[phase, last]);
        if !output.is_halted() {
            return None;
        }
        last = output.output.pop()?;
    }
    Some(last)
}

#[aoc(day07, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let nums: Vec<Int> = inp.split(',').map(|s| s.parse().unwrap()).collect();
    let mut out = 0;

    for a in 0..=4 {
        for b in 0..=4 {
            for c in 0..=4 {
                for d in 0..=4 {
                    for e in 0..=4 {
                        if let Some(x) = try_inputs(&nums, &[a, b, c, d, e]) {
                            out = out.max(x);
                        }
                    }
                }
            }
        }
    }

    out.to_string()
}

fn try_inputs_2(nums: &[Int], input: &[Int]) -> Option<Int> {
    let set = input.iter().cloned().collect::<HashSet<Int>>();
    if set.len() != input.len() {
        return None;
    }
    // create programs
    let mut programs: Vec<_> = std::iter::repeat(ICProgram::new(nums)).take(input.len()).collect();
    // give them their phases
    for (program, &phase) in programs.iter_mut().zip(input.iter()) {
        let output = program.run_single(phase);
        if !output.is_awaiting_input() {
            return None;
        }
    }
    // loop
    let mut last = 0;
    loop {
        let mut halted = false;
        for program in &mut programs {
            let mut output = program.run_single(last);
            if output.is_error() {
                return None;
            }
            last = output.output.pop()?;
            halted |= output.is_halted();
        }
        if halted {
            return Some(last);
        }
    }
}

#[aoc(day07, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let nums: Vec<Int> = inp.split(',').map(|s| s.parse().unwrap()).collect();
    let mut out = 0;

    for a in 5..=9 {
        for b in 5..=9 {
            for c in 5..=9 {
                for d in 5..=9 {
                    for e in 5..=9 {
                        if let Some(x) = try_inputs_2(&nums, &[a, b, c, d, e]) {
                            out = out.max(x);
                        }
                    }
                }
            }
        }
    }

    out.to_string()
}

#[test]
fn day07samples() {
    assert_eq!(
        _part1(r#"3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"#, true),
        "43210"
    );
    assert_eq!(
        _part1(
            r#"3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"#,
            true
        ),
        "54321"
    );
    assert_eq!(
        _part1(
            r#"3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"#,
            true
        ),
        "65210"
    );

    assert_eq!(
        _part2(
            r#"3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"#,
            true
        ),
        "139629729"
    );
    assert_eq!(
        _part2(
            r#"3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"#,
            true
        ),
        "18216"
    );
}
