use itertools::Itertools;
use std::{env, fs};

fn interval_to_pair(interval: &str) -> (i64, i64) {
    interval
        .split('-')
        .map(|num| num.parse::<i64>().expect("didn't get number"))
        .collect_tuple()
        .expect("didn't get 2 nums")
}

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");
    let lines = contents.lines().collect::<Vec<_>>();

    let assignments = lines
        .iter()
        .map(|line| {
            line.split('.')
                .map(interval_to_pair)
                .collect_tuple()
                .expect("didn't get two intervals")
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
