use std::convert::TryFrom;

type Int = i64;

fn run_intcode_vec(mut nums: Vec<Int>) -> Option<Int> {
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
    
    loop {
        match nums.get(i)? {
            // add
            1 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                // guaranteed not to panic in copy_from_slice
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = nums.get(to_usize(lhs)?)? + nums.get(to_usize(rhs)?)?;
                i += VALUES;
            },
            // multiply
            2 => {
                const VALUES: usize = 4;

                let mut arguments = [0; VALUES];
                // guaranteed not to panic in copy_from_slice
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(to_usize(target)?)? = nums.get(to_usize(lhs)?)? * nums.get(to_usize(rhs)?)?;
                i += VALUES;
            },
            // halt
            99 => {
                break;
            },
            _ => {
                return None;
            }
        }
    }
    Some(nums.get(0)?.clone())
}

fn _run_intcode(nums: &[Int]) -> Option<Int> {
    run_intcode_vec(nums.to_vec())
}

fn run_intcode_with_input(nums: &[Int], noun: Int, verb: Int) -> Option<Int> {
    let mut nums = nums.to_vec();
    if nums.len() <= 0 {
        dbg!(&nums);
    }
    *nums.get_mut(1)? = noun;
    *nums.get_mut(2)? = verb;
    run_intcode_vec(nums)
}

#[aoc(day02, part1)]
pub fn part1(inp: &str) -> String {
    let nums: Vec<Int> = inp.split(',')
        .map(|s| s.parse().unwrap())
        .collect();
    
    run_intcode_with_input(&nums[..], 12, 2).unwrap().to_string()
}

#[aoc(day02, part2)]
pub fn part2(inp: &str) -> String {
    let nums: Vec<Int> = inp.split(',')
        .map(|s| s.parse().unwrap())
        .collect();
    
    const TARGET: Int = 19690720;

    for noun in 0..=99 {
        for verb in 0..=99 {
            if run_intcode_with_input(&nums[..], noun, verb) == Some(TARGET) {
                return ((100 * noun) + verb).to_string();
            }
        }
    }
    "-1".to_string()
}

#[test]
fn day02samples() {
    assert_eq!(_run_intcode(&[1,0,0,0,99]), Some(2));
    assert_eq!(_run_intcode(&[2,3,0,3,99]), Some(2));
    assert_eq!(_run_intcode(&[2,4,4,5,99,0]), Some(2));
    assert_eq!(_run_intcode(&[1,1,1,4,99,5,6,0,99]), Some(30));
}
