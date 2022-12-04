use std::{env, fs};

fn interval_to_pair(interval: &str) -> (i64, i64) {
    let mut nums = interval.split('-');
    let first = nums.next().expect("no nums");
    let second = nums.next().expect("only one num");
    assert_eq!(nums.next(), None, "more than two nums");
    (
        first.parse::<i64>().expect("first wasn't num"),
        second.parse::<i64>().expect("second wasn't num"),
    )
}

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");
    let lines = contents.lines().collect::<Vec<_>>();

    let assignments = lines
        .iter()
        .map(|line| {
            let mut intervals = line.split(',');
            let first = intervals.next().expect("no interval");
            let second = intervals.next().expect("only one interval");
            assert_eq!(intervals.next(), None, "more than two intervals");
            (interval_to_pair(first), interval_to_pair(second))
        })
        .collect::<Vec<_>>();

    let part1 = assignments
        .iter()
        .map(|((a, b), (c, d))| ((a <= c && b >= d) || (a >= c && b <= d)) as i64)
        .sum::<i64>();
    println!("part 1: {}", part1);

    let part2 = assignments
        .iter()
        .map(|((a, b), (c, d))| !((b < c) || (d < a)) as i64)
        .sum::<i64>();
    println!("part 2: {}", part2);
}
