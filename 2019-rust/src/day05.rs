use std::convert::TryFrom;
use std::iter;

type Int = i64;

fn run_intcode_vec(mut nums: Vec<Int>, mut input: Vec<Int>, output: &mut Vec<Int>) -> Option<Int> {
    let mut i = 0usize;

    let to_usize = |i: Int| -> Option<usize> {
        usize::try_from(i).ok()
    };

    input.reverse();

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
        v.iter().cloned().chain(iter::repeat(0)).take(10).collect::<Vec<_>>()
    };

    loop {
        let mut opcode = *nums.get(i)?;
        let instruction = opcode % 100;
        opcode /= 100;
        match instruction {
            // add
            1 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                let modes = get_modes(opcode);

                let lhs_val = match modes[0] {
                    0 => *nums.get(to_usize(lhs)?)?,
                    1 => lhs,
                    _ => return None,
                };

                let rhs_val = match modes[1] {
                    0 => *nums.get(to_usize(rhs)?)?,
                    1 => rhs,
                    _ => return None,
                };

                *nums.get_mut(to_usize(target)?)? = lhs_val + rhs_val;
                i += VALUES;
            }
            // multiply
            2 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                let modes = get_modes(opcode);

                let lhs_val = match modes[0] {
                    0 => *nums.get(to_usize(lhs)?)?,
                    1 => lhs,
                    _ => return None,
                };

                let rhs_val = match modes[1] {
                    0 => *nums.get(to_usize(rhs)?)?,
                    1 => rhs,
                    _ => return None,
                };

                *nums.get_mut(to_usize(target)?)? = lhs_val * rhs_val;
                i += VALUES;
            }
            // get input
            3 => {
                const VALUES: usize = 2;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, target] = arguments;
                let inp = input.pop()?;

                *nums.get_mut(to_usize(target)?)? = inp;
                i += VALUES;
            }
            // output
            4 => {
                const VALUES: usize = 2;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, out] = arguments;
                let modes = get_modes(opcode);
                let out_val = match modes[0] {
                    0 => *nums.get(to_usize(out)?)?,
                    1 => out,
                    _ => return None,
                };
                output.push(out_val);

                i += VALUES;
            }
            // jump if true
            5 => {
                const VALUES: usize = 3;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, param, dest] = arguments;
                let modes = get_modes(opcode);
                let param_val = match modes[0] {
                    0 => *nums.get(to_usize(param)?)?,
                    1 => param,
                    _ => return None,
                };
                let dest_val = match modes[1] {
                    0 => *nums.get(to_usize(dest)?)?,
                    1 => dest,
                    _ => return None,
                };
                if param_val != 0 {
                    i = to_usize(dest_val)?;
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
                let modes = get_modes(opcode);
                let param_val = match modes[0] {
                    0 => *nums.get(to_usize(param)?)?,
                    1 => param,
                    _ => return None,
                };
                let dest_val = match modes[1] {
                    0 => *nums.get(to_usize(dest)?)?,
                    1 => dest,
                    _ => return None,
                };
                if param_val == 0 {
                    i = to_usize(dest_val)?;
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
                let modes = get_modes(opcode);
                let lhs_val = match modes[0] {
                    0 => *nums.get(to_usize(lhs)?)?,
                    1 => lhs,
                    _ => return None,
                };

                let rhs_val = match modes[1] {
                    0 => *nums.get(to_usize(rhs)?)?,
                    1 => rhs,
                    _ => return None,
                };
                *nums.get_mut(to_usize(target)?)? = (lhs_val < rhs_val) as Int;

                i += VALUES;
            }
            // equals
            8 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;
                let modes = get_modes(opcode);
                let lhs_val = match modes[0] {
                    0 => *nums.get(to_usize(lhs)?)?,
                    1 => lhs,
                    _ => return None,
                };

                let rhs_val = match modes[1] {
                    0 => *nums.get(to_usize(rhs)?)?,
                    1 => rhs,
                    _ => return None,
                };
                *nums.get_mut(to_usize(target)?)? = (lhs_val == rhs_val) as Int;

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
    Some(nums.get(0)?.clone())
}

#[aoc(day05, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let nums: Vec<Int> = inp.split(',')
        .map(|s| s.parse().unwrap())
        .collect();

    let input: Vec<Int> = vec![1];
    let mut output: Vec<Int> = vec![];
    let _returned = run_intcode_vec(nums, input, &mut output);
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

    let input: Vec<Int> = vec![5];
    let mut output: Vec<Int> = vec![];
    let _returned = run_intcode_vec(nums, input, &mut output);
    let out = output.pop().unwrap();
    assert!(output.iter().all(|x| *x == 0));
    out.to_string()
}

#[test]
fn day05samples() {
    let mut output: Vec<Int> = vec![];
    run_intcode_vec(vec![3,0,4,0,99],vec![1], &mut output);
    assert_eq!(output, vec![1]);
    output.clear();
    assert_eq!(run_intcode_vec(vec![1002,4,3,4,33],vec![1], &mut output), Some(1002));
    run_intcode_vec(vec![3,9,8,9,10,9,4,9,99,-1,8],vec![8], &mut output);
    assert_eq!(output, vec![1]);
    output.clear();
    run_intcode_vec(vec![3,9,8,9,10,9,4,9,99,-1,8],vec![9], &mut output);
    assert_eq!(output, vec![0]);
    output.clear();
}
