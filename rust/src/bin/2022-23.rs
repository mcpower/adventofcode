use std::collections::{HashMap, HashSet};

use itertools::Itertools;
use mcpower_aoc::{runner::run_samples_and_arg, vector::Vec2};

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let initial_positions = inp
        .lines()
        .enumerate()
        .flat_map(|(i, line)| {
            line.chars()
                .enumerate()
                .filter(|(_, c)| *c == '#')
                .map(move |(j, _)| Vec2(i as i64, j as i64))
        })
        .collect::<HashSet<_>>();
    let north = Vec2(-1, 0);
    let east = Vec2(0, 1);
    let south = Vec2(1, 0);
    let west = Vec2(0, -1);
    let directions = [
        (north, [north, north + east, north + west]),
        (south, [south, south + east, south + west]),
        (west, [west, west + north, west + south]),
        (east, [east, east + north, east + south]),
    ];

    let mut part1 = None;
    let mut part2 = None;

    let mut positions = initial_positions;
    let mut round = 0;
    while part1.is_none() || part2.is_none() {
        let mut proposed = HashMap::<Vec2, Vec2>::new();
        let mut moved = false;
        for position in positions.iter() {
            if (-1..=1)
                .cartesian_product(-1..=1)
                .filter(|x| *x != (0, 0))
                .map(|(a, b)| Vec2(a, b))
                .all(|v| !positions.contains(&(v + *position)))
            {
                continue;
            }
            for step in 0..4 {
                let (dir, check) = directions[(round + step) % 4];
                if check
                    .iter()
                    .all(|check_dir| !positions.contains(&(*check_dir + *position)))
                {
                    assert!(proposed.insert(*position, *position + dir).is_none());
                    break;
                }
            }
        }
        let collisions = proposed
            .values()
            .duplicates()
            .cloned()
            .collect::<HashSet<_>>();
        for (start, end) in proposed {
            if !collisions.contains(&end) {
                assert!(positions.remove(&start));
                assert!(positions.insert(end));
                moved = true;
            }
        }
        round += 1;
        if round == 10 {
            let (minx, maxx) = positions
                .iter()
                .map(|v| v.0)
                .minmax()
                .into_option()
                .unwrap();
            let (miny, maxy) = positions
                .iter()
                .map(|v| v.1)
                .minmax()
                .into_option()
                .unwrap();
            part1 = Some((maxy - miny + 1) * (maxx - minx + 1) - (positions.len() as i64));
        }
        if !moved && part2.is_none() {
            part2 = Some(round as i64);
        }
    }

    (part1.unwrap(), part2.unwrap())
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"];
