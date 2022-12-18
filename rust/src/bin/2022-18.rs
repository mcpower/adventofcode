use std::collections::HashSet;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

fn solve(inp: &str, _is_sample: bool) -> (usize, usize) {
    let set: HashSet<(i64, i64, i64)> = inp
        .lines()
        .map(|line| {
            line.split(',')
                .map(|x| x.parse().unwrap())
                .collect_tuple()
                .unwrap()
        })
        .collect();
    let part1 = {
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
    let mut inverse = HashSet::<(i64, i64, i64)>::new();
    let (x_min, x_max) = set.iter().map(|p| p.0).minmax().into_option().unwrap();
    let (y_min, y_max) = set.iter().map(|p| p.1).minmax().into_option().unwrap();
    let (z_min, z_max) = set.iter().map(|p| p.2).minmax().into_option().unwrap();

    let start = (x_min - 1, y_min - 1, z_min - 1);
    inverse.insert(start);
    let mut todo = vec![start];
    while let Some((x, y, z)) = todo.pop() {
        for d in [-1, 1] {
            for other @ (ox, oy, oz) in [(x + d, y, z), (x, y + d, z), (x, y, z + d)] {
                if !(x_min - 1 <= ox
                    && ox <= x_max + 1
                    && y_min - 1 <= oy
                    && oy <= y_max + 1
                    && z_min - 1 <= oz
                    && oz <= z_max + 1)
                {
                    continue;
                }
                if inverse.contains(&other) || set.contains(&other) {
                    continue;
                }
                todo.push(other);
                inverse.insert(other);
            }
        }
    }
    let x_dist = x_max + 1 - (x_min - 1) + 1;
    let y_dist = y_max + 1 - (y_min - 1) + 1;
    let z_dist = z_max + 1 - (z_min - 1) + 1;

    let part2 = {
        let outer_area = 2 * (x_dist * y_dist + y_dist * z_dist + z_dist * x_dist);
        inverse.len() * 6
            - inverse
                .iter()
                .map(|&(x, y, z)| {
                    let mut out = 0;
                    for d in [-1, 1] {
                        out += inverse.contains(&(x + d, y, z)) as usize;
                        out += inverse.contains(&(x, y + d, z)) as usize;
                        out += inverse.contains(&(x, y, z + d)) as usize;
                    }
                    out
                })
                .sum::<usize>()
            - (outer_area as usize)
    };

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
