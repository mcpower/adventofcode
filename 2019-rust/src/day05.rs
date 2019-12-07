use std::convert::TryFrom;
use std::iter;

type Int = i64;

fn _run_intcode(nums: &mut Vec<Int>, input: &[Int], input_idx: &mut usize, output: &mut Vec<Int>) -> Option<()> {
    let mut i = 0usize;

    let to_usize = |i: Int| -> Option<usize> {
        usize::try_from(i).ok()
    };

    let _add_to_i = |val: Int| -> Option<()> {
        i = if val.is_negative() {
            i.checked_sub(to_usize(val.checked_abs()?)?)?
        } else {
            i.checked_add(to_usize(val)?)?
        };
        Some(())
    };

    let get_modes = |val: Int| {
        let mut val = val;
        let mut v: Vec<u8> = vec![];
        while val > 0 {
            v.push((val % 10) as u8);
            val /= 10;
        }
        // guaranteed not to terminate
        v.into_iter().chain(iter::repeat(0)).peekable()
    };

    loop {
        let mut opcode = *nums.get(i)?;
        let instruction = opcode % 100;
        opcode /= 100;

        let mut modes_it = get_modes(opcode);

        let mut use_mode = |val: Int| {
            let out = match modes_it.next().unwrap() {
                0 => *nums.get(to_usize(val)?)?,
                1 => val,
                _ => return None,
            };
            Some(out)
        };

        match instruction {
            // add
            1 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = use_mode(lhs)? + use_mode(rhs)?;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // multiply
            2 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = use_mode(lhs)? * use_mode(rhs)?;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // get input
            3 => {
                const VALUES: usize = 2;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, target] = arguments;
                let inp = *input.get(*input_idx)?;
                *input_idx += 1;

                *nums.get_mut(to_usize(target)?)? = inp;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // output
            4 => {
                const VALUES: usize = 2;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, out] = arguments;
                output.push(use_mode(out)?);

                i += VALUES;
            }
            // jump if true
            5 => {
                const VALUES: usize = 3;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, param, dest] = arguments;
                if use_mode(param)? != 0 {
                    i = to_usize(use_mode(dest)?)?;
                } else {
                    i += VALUES;
                }
            }
            // jump if false
            6 => {
                const VALUES: usize = 3;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, param, dest] = arguments;
                if use_mode(param)? == 0 {
                    i = to_usize(use_mode(dest)?)?;
                } else {
                    i += VALUES;
                }
            }
            // less than
            7 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = (use_mode(lhs)? < use_mode(rhs)?) as Int;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // equals
            8 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = (use_mode(lhs)? == use_mode(rhs)?) as Int;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // halt
            99 => {
                break;
            }
            _ => {
                return None;
            }
        }
    }
    Some(())
}

// (halted, inputs_consumed, outputs)
fn run_intcode(nums: &[Int], input: &[Int]) -> (bool, usize, Vec<Int>) {
    let mut output = vec![];
    let mut consumed = 0usize;
    let mut nums = nums.to_vec();
    let result = _run_intcode(&mut nums, input, &mut consumed, &mut output).is_some();
    (result, consumed, output)
}

#[aoc(day05, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let nums: Vec<Int> = inp.split(',')
        .map(|s| s.parse().unwrap())
        .collect();

    let (halted, consumed, mut output) = run_intcode(nums.as_slice(), &[1]);
    assert!(halted);
    assert_eq!(consumed, 1);
    let out = output.pop().unwrap();
    assert!(output.iter().all(|x| *x == 0));
    out.to_string()
}

#[aoc(day05, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let nums: Vec<Int> = inp.split(',')
        .map(|s| s.parse().unwrap())
        .collect();

    let (halted, consumed, mut output) = run_intcode(nums.as_slice(), &[5]);
    assert!(halted);
    assert_eq!(consumed, 1);
    let out = output.pop().unwrap();
    assert!(output.iter().all(|x| *x == 0));
    out.to_string()
}

#[test]
fn day05samples() {
    assert_eq!(run_intcode(&[3,0,4,0,99],&[1]), (true, 1, vec![1]));
    assert_eq!(run_intcode(&[1002,4,3,4,33],&[]), (true, 0, vec![]));
    assert_eq!(run_intcode(&[3,9,8,9,10,9,4,9,99,-1,8],&[8]), (true, 1, vec![1]));
    assert_eq!(run_intcode(&[3,9,8,9,10,9,4,9,99,-1,8],&[9]), (true, 1, vec![0]));
}
