use aho_corasick::{AhoCorasick, PatternID};
use mcpower_aoc::runner::run_samples_and_arg;

const NUMBERS: &[&str] = &[
    "one", "1", "two", "2", "three", "3", "four", "4", "five", "5", "six", "6", "seven", "7",
    "eight", "8", "nine", "9",
];

fn pattern_id_to_digit(id: PatternID) -> i64 {
    (id.as_i32() / 2 + 1).into()
}

fn solve(
    #[allow(unused_variables)] inp: &str,
    #[allow(unused_variables)] is_sample: bool,
) -> (i64, i64) {
    let ac = AhoCorasick::new(NUMBERS).unwrap();
    let part1 = inp
        .lines()
        .map(|line| {
            let mut nums = line.chars().filter_map(|c| c.to_digit(10));
            let first = nums.next().unwrap_or(0);
            if !is_sample && first == 0 {
                panic!("real case did not have any numbers");
            }
            let last = nums.last().unwrap_or(first);
            i64::from(first * 10 + last)
        })
        .sum();

    let part2 = inp
        .lines()
        .map(|line| {
            let mut first = (line.len(), 0);
            let mut last = (0, 0);
            for mat in ac.find_overlapping_iter(line) {
                let cur = (mat.start(), pattern_id_to_digit(mat.pattern()));
                first = first.min(cur);
                last = last.max(cur);
            }
            assert_ne!(first.1, 0, "couldn't find first??");
            assert_ne!(last.1, 0, "couldn't find last??");
            first.1 * 10 + last.1
        })
        .sum();

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
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
",
    r"

",
    r"

",
];
