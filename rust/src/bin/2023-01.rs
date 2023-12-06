use mcpower_aoc::runner::run_samples_and_arg;

fn solve(
    #[allow(unused_variables)] inp: &str,
    #[allow(unused_variables)] is_sample: bool,
) -> (i64, i64) {
    let part1 = inp
        .lines()
        .map(|line| {
            let mut nums = line.chars().filter_map(|c| c.to_digit(10));
            let first = nums.next().expect("line doesn't have digit");
            let last = nums.last().unwrap_or(first);
            i64::from(first * 10 + last)
        })
        .sum();

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[
    r"
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
",
    r"

",
    r"

",
    r"

",
];
