#[aoc(day02, part1)]
pub fn part1(inp: &str) -> String {
    let mut nums: Vec<usize> = inp.trim().split(',')
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
    
    let mut i = 0usize;
    
    nums[1] = 12;
    nums[2] = 2;

    loop {
        match nums[i] {
            1 => {
                let y = nums[i+3];
                nums[y] = nums[nums[i+2]] + nums[nums[i+1]]
            },
            2 => {
                let y = nums[i+3];
                nums[y] = nums[nums[i+2]] * nums[nums[i+1]]
            },
            99 => break,
            _ => break
        }
        i += 4;
    }

    // dbg!(&nums);

    nums[0].to_string()
}

#[aoc(day02, part2)]
pub fn part2(inp: &str) -> String {
    let orig_nums: Vec<usize> = inp.trim().split(',')
        .map(|s| s.parse::<usize>().unwrap())
        .collect();

    let target = 19690720usize;

    for noun in 0..200 {
        for verb in 0..200 {
            let mut nums = orig_nums.to_vec();
            nums[1] = noun;
            nums[2] = verb;
            let mut i = 0usize;
            loop {
                if i >= nums.len() {
                    nums[0] = 0;
                    break;
                }
                if nums[i] == 99 {
                    break;
                }
                if i + 3 >= nums.len() {
                    nums[0] = 0;
                    break;
                }
                match nums[i] {
                    1 => {
                        let y = nums[i+3];
                        if std::cmp::max(y, std::cmp::max(nums[i+2], nums[i+1])) >= nums.len() {
                            nums[0] = 0;
                            break;
                        }
                        nums[y] = nums[nums[i+2]] + nums[nums[i+1]]
                    },
                    2 => {
                        let y = nums[i+3];
                        if std::cmp::max(y, std::cmp::max(nums[i+2], nums[i+1])) >= nums.len() {
                            nums[0] = 0;
                            break;
                        }
                        nums[y] = nums[nums[i+2]] * nums[nums[i+1]]
                    },
                    _ => break
                }
                i += 4;
            }
            if nums[0] == target {
                return (noun * 100 + verb).to_string();
            }
        }
    };
    "-1".to_string()
}

#[test]
fn day02samples() {
// assert_eq!(part1(r#"
// 1,0,0,0,99
// "#.trim_start_matches('\n')), "2");

// assert_eq!(part2(r#"
// "#.trim_start_matches('\n')), "");
}
