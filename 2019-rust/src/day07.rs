use std::convert::TryFrom;
use std::iter;
use std::collections::HashSet;

type Int = i64;

fn _run_intcode(
    nums: &mut Vec<Int>,
    nums_idx: &mut usize,
    input: &[Int],
    input_idx: &mut usize,
    output: &mut Vec<Int>,
) -> Option<()> {
    let mut i = *nums_idx;

    let to_usize = |i: Int| -> Option<usize> { usize::try_from(i).ok() };

    let _add_to_i = |val: Int| -> Option<()> {
        i = if val.is_negative() {
            i.checked_sub(to_usize(val.checked_abs()?)?)?
        } else {
            i.checked_add(to_usize(val)?)?
        };
        *nums_idx = i;
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
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = use_mode(lhs)? + use_mode(rhs)?;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // multiply
            2 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = use_mode(lhs)? * use_mode(rhs)?;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // get input
            3 => {
                const VALUES: usize = 2;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
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
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
                let [_, out] = arguments;
                output.push(use_mode(out)?);

                i += VALUES;
            }
            // jump if true
            5 => {
                const VALUES: usize = 3;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
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
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
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
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = (use_mode(lhs)? < use_mode(rhs)?) as Int;
                assert_eq!(*modes_it.peek().unwrap(), 0);
                i += VALUES;
            }
            // equals
            8 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                arguments.copy_from_slice(nums.get(i..i + VALUES)?);
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
        *nums_idx = i;
    }
    Some(())
}

// (halted, inputs_consumed, outputs)
fn run_intcode(nums: &[Int], input: &[Int]) -> (bool, usize, Vec<Int>, Vec<Int>) {
    let mut output = vec![];
    let mut consumed = 0usize;
    let mut nums = nums.to_vec();
    let mut nums_idx = 0usize;
    let result = _run_intcode(&mut nums, &mut nums_idx, input, &mut consumed, &mut output).is_some();
    (result, nums_idx, nums, output)
}

fn run_intcode_with_i(nums: &[Int], i: usize, input: &[Int]) -> (bool, usize, Vec<Int>, Vec<Int>) {
    let mut output = vec![];
    let mut consumed = 0usize;
    let mut nums = nums.to_vec();
    let mut nums_idx = i;
    let result = _run_intcode(&mut nums, &mut nums_idx, input, &mut consumed, &mut output).is_some();
    (result, nums_idx, nums, output)
}

fn try_inputs(nums: &[Int], input: &[Int]) -> Option<Int> {
    if let &[a, b, c, d, e] = input {
        let set = [a, b, c, d, e].iter().cloned().collect::<HashSet<Int>>();
        if set.len() != 5 {
            return None;
        }
        let a_res = run_intcode(nums, &[a, 0]).3.pop()?;
        let b_res = run_intcode(nums, &[b, a_res]).3.pop()?;
        let c_res = run_intcode(nums, &[c, b_res]).3.pop()?;
        let d_res = run_intcode(nums, &[d, c_res]).3.pop()?;
        let e_res = run_intcode(nums, &[e, d_res]).3.pop()?;
        Some(e_res)
    } else {
        None
    }
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
                        if let Some(x) = try_inputs(nums.as_slice(), &[a,b,c,d,e]) {
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
    if let &[a, b, c, d, e] = input {
        let set = [a, b, c, d, e].iter().cloned().collect::<HashSet<Int>>();
        if set.len() != 5 {
            return None;
        }
        let mut a_prog = run_intcode(nums, &[a]);
        let mut b_prog = run_intcode(nums, &[b]);
        let mut c_prog = run_intcode(nums, &[c]);
        let mut d_prog = run_intcode(nums, &[d]);
        let mut e_prog = run_intcode(nums, &[e]);
        let mut last = 0;
        loop {
            a_prog = run_intcode_with_i(a_prog.2.as_slice(), a_prog.1, &[last]); last = a_prog.3.pop()?;
            b_prog = run_intcode_with_i(b_prog.2.as_slice(), b_prog.1, &[last]); last = b_prog.3.pop()?;
            c_prog = run_intcode_with_i(c_prog.2.as_slice(), c_prog.1, &[last]); last = c_prog.3.pop()?;
            d_prog = run_intcode_with_i(d_prog.2.as_slice(), d_prog.1, &[last]); last = d_prog.3.pop()?;
            e_prog = run_intcode_with_i(e_prog.2.as_slice(), e_prog.1, &[last]); last = e_prog.3.pop()?;
            if a_prog.0 || b_prog.0 || c_prog.0 || d_prog.0 || e_prog.0{
                break
            }
        }
        Some(last)
    } else {
        None
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
                        if let Some(x) = try_inputs_2(nums.as_slice(), &[a,b,c,d,e]) {
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
assert_eq!(_part1(r#"
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
"#.trim_matches('\n'), true), "43210");
    assert_eq!(_part1(r#"
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
"#.trim_matches('\n'), true), "54321");
    assert_eq!(_part1(r#"
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
"#.trim_matches('\n'), true), "65210");

assert_eq!(_part2(r#"
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
"#.trim_matches('\n'), true), "139629729");
    assert_eq!(_part2(r#"
3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
"#.trim_matches('\n'), true), "18216");
}
