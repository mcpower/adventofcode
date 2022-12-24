use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashMap, HashSet},
};

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

    type SearchNode = (i64, Vec2);
    let mut cache = HashMap::<i64, HashSet<Vec2>>::new();
    let start = Vec2(-1, 0);
    let goal = Vec2(inner_rows, inner_cols - 1);
    let f = |(time, pos): SearchNode, goal: Vec2| time + (pos - goal).norm_1();

    let mut a_star = |start_node: SearchNode, goal: Vec2| {
        let mut open = BinaryHeap::<Reverse<(i64, SearchNode)>>::new();
        let first_node = Reverse((f(start_node, goal), start_node));
        open.push(first_node);
        let mut seen = HashSet::<SearchNode>::new();
        seen.insert(start_node);
        while let Some(Reverse((_f_value, popped @ (time, pos)))) = open.pop() {
            if popped.1 == goal {
                return popped.0;
            }
            // In-lined expand function to save a collect-into-Vec / clone due
            // to FnMut silliness. Saves ~10ms run time.
            let children = {
                let blizzards = cache.entry(time).or_insert_with(|| {
                    initial_blizzards
                        .iter()
                        .map(|&(initial_pos, delta)| {
                            let mut out = initial_pos + ((time + 1) * delta);
                            out.0 = out.0.rem_euclid(inner_rows);
                            out.1 = out.1.rem_euclid(inner_cols);
                            out
                        })
                        .collect()
                });
                FOUR_ADJ
                    .iter()
                    .map(move |delta| pos + *delta)
                    .filter(move |new_pos| {
                        *new_pos == goal
                            || 0 <= new_pos.1
                                && new_pos.1 < inner_cols
                                && 0 <= new_pos.0
                                && new_pos.0 < inner_rows
                    })
                    .chain(std::iter::once(pos))
                    .filter(move |new_pos| !blizzards.contains(new_pos))
            };
            for child in children {
                let new_search_node = (popped.0 + 1, child);
                if !seen.contains(&new_search_node) {
                    open.push(Reverse((f(new_search_node, goal), new_search_node)));
                    seen.insert(new_search_node);
                }
            }
        }
        unreachable!()
    };

    let part1 = a_star((0, start), goal);
    let part1point5 = a_star((part1, goal), start);
    let part2 = a_star((part1point5, start), goal);

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
