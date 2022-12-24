use std::{collections::HashSet, mem::swap};

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

    let part1 = {
        // "what positions could you be in after every single move?"
        let mut blizzards = initial_blizzards.clone();
        let mut out = 0;
        let mut cur_positions = HashSet::new();
        cur_positions.insert(Vec2(-1, 0));
        let target = Vec2(inner_rows, inner_cols - 1);
        let mut new_cur_positions = HashSet::new();
        while !cur_positions.contains(&target) {
            for blizzard in &mut blizzards {
                blizzard.0 += blizzard.1;
                blizzard.0 .0 = blizzard.0 .0.rem_euclid(inner_rows);
                blizzard.0 .1 = blizzard.0 .1.rem_euclid(inner_cols);
            }
            for &position in &cur_positions {
                for adj in FOUR_ADJ {
                    let new_position = position + adj;
                    if new_position == target
                        || (0 <= new_position.1
                            && new_position.1 < inner_cols
                            && 0 <= new_position.0
                            && new_position.0 < inner_rows)
                    {
                        if !blizzards
                            .iter()
                            .any(|(blizzard_pos, _)| *blizzard_pos == new_position)
                        {
                            new_cur_positions.insert(new_position);
                        }
                    }
                }
                if !blizzards
                    .iter()
                    .any(|(blizzard_pos, _)| *blizzard_pos == position)
                {
                    new_cur_positions.insert(position);
                }
            }
            swap(&mut cur_positions, &mut new_cur_positions);
            new_cur_positions.clear();
            out += 1;
        }
        out
    };

    let part2 = {
        // just run it three times lol
        let mut blizzards = initial_blizzards;
        let mut out = 0;
        let mut cur_positions = HashSet::new();
        cur_positions.insert(Vec2(-1, 0));
        let target = Vec2(inner_rows, inner_cols - 1);
        let mut new_cur_positions = HashSet::new();
        while !cur_positions.contains(&target) {
            for blizzard in &mut blizzards {
                blizzard.0 += blizzard.1;
                blizzard.0 .0 = blizzard.0 .0.rem_euclid(inner_rows);
                blizzard.0 .1 = blizzard.0 .1.rem_euclid(inner_cols);
            }
            for &position in &cur_positions {
                for adj in FOUR_ADJ {
                    let new_position = position + adj;
                    if new_position == target
                        || (0 <= new_position.1
                            && new_position.1 < inner_cols
                            && 0 <= new_position.0
                            && new_position.0 < inner_rows)
                    {
                        if !blizzards
                            .iter()
                            .any(|(blizzard_pos, _)| *blizzard_pos == new_position)
                        {
                            new_cur_positions.insert(new_position);
                        }
                    }
                }
                if !blizzards
                    .iter()
                    .any(|(blizzard_pos, _)| *blizzard_pos == position)
                {
                    new_cur_positions.insert(position);
                }
            }
            swap(&mut cur_positions, &mut new_cur_positions);
            new_cur_positions.clear();
            out += 1;
        }
        cur_positions.clear();
        cur_positions.insert(target);
        let target = Vec2(-1, 0);
        while !cur_positions.contains(&target) {
            for blizzard in &mut blizzards {
                blizzard.0 += blizzard.1;
                blizzard.0 .0 = blizzard.0 .0.rem_euclid(inner_rows);
                blizzard.0 .1 = blizzard.0 .1.rem_euclid(inner_cols);
            }
            for &position in &cur_positions {
                for adj in FOUR_ADJ {
                    let new_position = position + adj;
                    if new_position == target
                        || (0 <= new_position.1
                            && new_position.1 < inner_cols
                            && 0 <= new_position.0
                            && new_position.0 < inner_rows)
                    {
                        if !blizzards
                            .iter()
                            .any(|(blizzard_pos, _)| *blizzard_pos == new_position)
                        {
                            new_cur_positions.insert(new_position);
                        }
                    }
                }
                if !blizzards
                    .iter()
                    .any(|(blizzard_pos, _)| *blizzard_pos == position)
                {
                    new_cur_positions.insert(position);
                }
            }
            swap(&mut cur_positions, &mut new_cur_positions);
            new_cur_positions.clear();
            out += 1;
        }
        cur_positions.clear();
        cur_positions.insert(target);
        let target = Vec2(inner_rows, inner_cols - 1);
        while !cur_positions.contains(&target) {
            for blizzard in &mut blizzards {
                blizzard.0 += blizzard.1;
                blizzard.0 .0 = blizzard.0 .0.rem_euclid(inner_rows);
                blizzard.0 .1 = blizzard.0 .1.rem_euclid(inner_cols);
            }
            for &position in &cur_positions {
                for adj in FOUR_ADJ {
                    let new_position = position + adj;
                    if new_position == target
                        || (0 <= new_position.1
                            && new_position.1 < inner_cols
                            && 0 <= new_position.0
                            && new_position.0 < inner_rows)
                    {
                        if !blizzards
                            .iter()
                            .any(|(blizzard_pos, _)| *blizzard_pos == new_position)
                        {
                            new_cur_positions.insert(new_position);
                        }
                    }
                }
                if !blizzards
                    .iter()
                    .any(|(blizzard_pos, _)| *blizzard_pos == position)
                {
                    new_cur_positions.insert(position);
                }
            }
            swap(&mut cur_positions, &mut new_cur_positions);
            new_cur_positions.clear();
            out += 1;
        }
        out
    };

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"];
