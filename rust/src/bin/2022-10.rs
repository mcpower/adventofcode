use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

fn solve(inp: &str, _is_sample: bool) -> (i64, String) {
    let mut last = 1;
    // at the END of this 1-indexed (!) cycle, x was...
    // OR: DURING this 0-indexed cycle, x was...
    let mut history: Vec<i64> = vec![last];
    for line in inp.lines() {
        if line == "noop" {
            history.push(last);
        } else if let Some(("addx", n)) = line.split_once(' ') {
            let n = n.parse::<i64>().expect("addx arg wasn't int");
            history.push(last);
            last += n;
            history.push(last);
        }
    }
    let part1 = history
        .iter()
        .enumerate()
        .skip(20)
        .step_by(40)
        .map(|(i, x)| (TryInto::<i64>::try_into(i).expect("size overflowed i64??")) * x)
        .sum();

    let part2 = history
        .iter()
        .enumerate()
        .map(|(i, x)| {
            x - 1 <= (TryInto::<i64>::try_into(i).unwrap() % 40)
                && (TryInto::<i64>::try_into(i).unwrap() % 40) <= x + 1
        })
        .map(|x| if x { '#' } else { '.' })
        .chunks(40)
        .into_iter()
        .map(|chunk| chunk.collect::<String>())
        .join("\n");
    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[
    r"
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
",
    r"
noop
addx 3
addx -5
",
    r"

",
    r"

",
];
