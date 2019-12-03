fn _run_intcode(mut nums: Vec<usize>) -> Option<usize> {
    let mut i = 0;
    loop {
        match nums.get(i)? {
            // add
            1 => {
                const VALUES: usize = 4;

                let mut arguments = [0usize; VALUES];
                // guaranteed not to panic in copy_from_slice
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;

                *nums.get_mut(target)? = nums.get(lhs)? + nums.get(rhs)?;
                i += VALUES;
            },
            // multiply
            2 => {
                const VALUES: usize = 4;

                let mut arguments = [0usize; VALUES];
                arguments.copy_from_slice(nums.get(i..i+VALUES)?);
                let [_, lhs, rhs, target] = arguments;
                
                *nums.get_mut(target)? = nums.get(lhs)? * nums.get(rhs)?;
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

fn run_intcode(nums: &[usize]) -> Option<usize> {
    _run_intcode(nums.to_vec())
}

fn run_intcode_with_input(nums: &[usize], noun: usize, verb: usize) -> Option<usize> {
    let mut nums = nums.to_vec();
    if nums.len() <= 0 {
        dbg!(&nums);
    }
    *nums.get_mut(1)? = noun;
    *nums.get_mut(2)? = verb;
    _run_intcode(nums)
}

#[aoc(day02, part1)]
pub fn part1(inp: &str) -> String {
    let nums: Vec<usize> = inp.trim().split(',')
        .map(|s| s.parse().unwrap())
        .collect();

    run_intcode_with_input(&nums[..], 12, 2).unwrap().to_string()
}

#[aoc(day02, part2)]
pub fn part2(inp: &str) -> String {
    let nums: Vec<usize> = inp.trim().split(',')
        .map(|s| s.parse().unwrap())
        .collect();
    
    const TARGET: usize = 19690720;

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
    assert_eq!(run_intcode(&[1,0,0,0,99]), Some(2));
    assert_eq!(run_intcode(&[2,3,0,3,99]), Some(2));
    assert_eq!(run_intcode(&[2,4,4,5,99,0]), Some(2));
    assert_eq!(run_intcode(&[1,1,1,4,99,5,6,0,99]), Some(30));
}
