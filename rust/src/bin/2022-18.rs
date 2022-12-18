use std::collections::HashSet;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

fn solve(inp: &str, _is_sample: bool) -> (usize, i64) {
    let part1 = {
        let set: HashSet<(i64, i64, i64)> = inp
            .lines()
            .map(|line| {
                line.split(',')
                    .map(|x| x.parse().unwrap())
                    .collect_tuple()
                    .unwrap()
            })
            .collect();
        set.len() * 6
            - set
                .iter()
                .map(|&(x, y, z)| {
                    let mut out = 0;
                    for d in [-1, 1] {
                        out += set.contains(&(x + d, y, z)) as usize;
                        out += set.contains(&(x, y + d, z)) as usize;
                        out += set.contains(&(x, y, z + d)) as usize;
                    }
                    out
                })
                .sum::<usize>()
    };

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[
    r"
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
",
    r"
1,1,1
2,1,1
",
    r"

",
    r"

",
];
