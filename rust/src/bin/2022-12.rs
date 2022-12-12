use std::collections::VecDeque;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

const DELTA_4: &[(i64, i64)] = &[(-1, 0), (0, 1), (1, 0), (0, -1)];

fn solve(inp: &str) -> (i64, i64) {
    let grid: Vec<Vec<char>> = inp.lines().map(|line| line.chars().collect()).collect();

    let start = grid
        .iter()
        .enumerate()
        .flat_map(|(i, row)| row.iter().enumerate().map(move |(j, c)| (i, j, c)))
        .filter(|(_i, _j, c)| **c == 'S')
        .map(|(i, j, _c)| (i, j))
        .collect_tuple::<(_,)>()
        .expect("not 1 start?")
        .0;

    let end = grid
        .iter()
        .enumerate()
        .flat_map(|(i, row)| row.iter().enumerate().map(move |(j, c)| (i, j, c)))
        .filter(|(_i, _j, c)| **c == 'E')
        .map(|(i, j, _c)| (i, j))
        .collect_tuple::<(_,)>()
        .expect("not 1 start?")
        .0;

    let elevations: Vec<Vec<u8>> = grid
        .iter()
        .map(|row| {
            row.iter()
                .map(|c| match *c {
                    'S' => 0,
                    'E' => 25,
                    other => ((other as u64) - ('a' as u64))
                        .try_into()
                        .expect("can't elevation into size?"),
                })
                .collect()
        })
        .collect();

    let elevations_ref = &elevations;
    let expand = |(row, col): (usize, usize)| {
        let cur_elevation = elevations[row][col];
        DELTA_4.iter().filter_map(move |(drow, dcol)| {
            let new_row = (TryInto::<i64>::try_into(row).ok()? + *drow) as usize;
            let new_col = (TryInto::<i64>::try_into(col).ok()? + *dcol) as usize;
            let elevation = *elevations_ref.get(new_row)?.get(new_col)?;
            if elevation <= cur_elevation + 1 {
                Some((new_row, new_col))
            } else {
                None
            }
        })
    };

    let part1 = {
        let mut queue = VecDeque::new();
        // TODO: use once_cell? lol
        let mut distances: Vec<Vec<Option<i64>>> =
            elevations.iter().map(|row| vec![None; row.len()]).collect();
        queue.push_back(start);
        let (start_row, start_col) = start;
        distances[start_row][start_col] = Some(0);
        while let Some(popped) = queue.pop_front() {
            if popped == end {
                break;
            }
            let (popped_row, popped_col) = popped;
            let cur_dist = distances[popped_row][popped_col].unwrap();
            let new_dist = cur_dist + 1;
            for successor in expand(popped) {
                let (successor_row, successor_col) = successor;
                if let Some(existing) = distances[successor_row][successor_col] {
                    if existing <= new_dist {
                        continue;
                    }
                }
                distances[successor_row][successor_col] = Some(new_dist);
                queue.push_back(successor);
            }
        }
        let (end_row, end_col) = end;
        distances[end_row][end_col].expect("didn't hit the end?")
    };

    let expand_part2 = |(row, col): (usize, usize)| {
        let cur_elevation = elevations[row][col];
        DELTA_4.iter().filter_map(move |(drow, dcol)| {
            let new_row = (TryInto::<i64>::try_into(row).ok()? + *drow) as usize;
            let new_col = (TryInto::<i64>::try_into(col).ok()? + *dcol) as usize;
            let elevation = *elevations_ref.get(new_row)?.get(new_col)?;
            if cur_elevation <= elevation + 1 {
                Some((new_row, new_col))
            } else {
                None
            }
        })
    };

    let part2 = {
        let mut queue = VecDeque::new();
        // TODO: use once_cell? lol
        let mut distances: Vec<Vec<Option<i64>>> =
            elevations.iter().map(|row| vec![None; row.len()]).collect();
        queue.push_back(end);
        let (end_row, end_col) = end;
        distances[end_row][end_col] = Some(0);
        let mut ans = None;
        while let Some(popped) = queue.pop_front() {
            let (popped_row, popped_col) = popped;
            let elevation = elevations[popped_row][popped_col];
            let cur_dist = distances[popped_row][popped_col].unwrap();
            if elevation == 0 {
                ans = Some(cur_dist);
                break;
            }
            let new_dist = cur_dist + 1;
            for successor in expand_part2(popped) {
                let (successor_row, successor_col) = successor;
                if let Some(existing) = distances[successor_row][successor_col] {
                    if existing <= new_dist {
                        continue;
                    }
                }
                distances[successor_row][successor_col] = Some(new_dist);
                queue.push_back(successor);
            }
        }
        ans.expect("didn't hit the end?")
    };

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"];
