use std::collections::HashSet;

use mcpower_aoc::{
    runner::run_samples_and_arg,
    vector::{Vec2, FOUR_ADJ},
};

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let lines = inp.lines().collect::<Vec<_>>();
    let inner_rows = lines.len() as i64 - 2;
    let inner_cols = lines.first().unwrap().len() as i64 - 2;
    // assume ASCII
    let initial_blizzards = lines[1..lines.len() - 1]
        .iter()
        .enumerate()
        .flat_map(|(row_i, row)| {
            row[1..row.len() - 1]
                .chars()
                .enumerate()
                .filter_map(move |(col_i, c)| {
                    Some((
                        Vec2(row_i as i64, col_i as i64),
                        match c {
                            '^' => Vec2(-1, 0),
                            '>' => Vec2(0, 1),
                            'v' => Vec2(1, 0),
                            '<' => Vec2(0, -1),
                            '.' => {
                                return None;
                            }
                            _ => unreachable!(),
                        },
                    ))
                })
        })
        .collect::<Vec<_>>();

    let start = Vec2(-1, 0);
    let goal = Vec2(inner_rows, inner_cols - 1);

    let solve = |start: Vec2, start_time: i64, goal: Vec2| {
        let mut blizzards = initial_blizzards
            .iter()
            .map(|&(initial_pos, delta)| {
                let mut out = initial_pos + (start_time * delta);
                out.0 = out.0.rem_euclid(inner_rows);
                out.1 = out.1.rem_euclid(inner_cols);
                (out, delta)
            })
            .collect::<Vec<_>>();
        let mut out = start_time;
        let mut cur_positions = HashSet::new();
        cur_positions.insert(start);
        while !cur_positions.contains(&goal) {
            for blizzard in &mut blizzards {
                blizzard.0 += blizzard.1;
                blizzard.0 .0 = blizzard.0 .0.rem_euclid(inner_rows);
                blizzard.0 .1 = blizzard.0 .1.rem_euclid(inner_cols);
            }
            cur_positions = cur_positions
                .drain()
                .flat_map(|pos| {
                    FOUR_ADJ
                        .iter()
                        .map(move |delta| pos + *delta)
                        .filter(|new_pos| {
                            *new_pos == goal
                                || 0 <= new_pos.1
                                    && new_pos.1 < inner_cols
                                    && 0 <= new_pos.0
                                    && new_pos.0 < inner_rows
                        })
                        .chain(std::iter::once(pos))
                        .filter(|new_pos| {
                            blizzards
                                .iter()
                                .all(|(blizzard_pos, _)| *blizzard_pos != *new_pos)
                        })
                })
                .collect();
            out += 1;
        }
        out
    };

    let part1 = solve(start, 0, goal);
    let part1point5 = solve(goal, part1, start);
    let part2 = solve(start, part1point5, goal);

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[
    r"
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
",
    r"
#.##
#..#
#..#
##.#
",
];
