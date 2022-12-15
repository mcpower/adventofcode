use std::collections::BTreeMap;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

#[derive(Debug, Clone, Copy)]
enum NonAir {
    Rock,
    Sand,
}

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let rock: Vec<Vec<(i64, i64)>> = inp
        .lines()
        .map(|line| {
            line.split(" -> ")
                .map(|point| {
                    point
                        .split(',')
                        .map(|n| n.parse().expect("num wasn't i64"))
                        .collect_tuple()
                        .expect("point didn't have comma")
                })
                .collect()
        })
        .collect();

    let mut non_air_points: BTreeMap<i64, BTreeMap<i64, NonAir>> = BTreeMap::new();
    for line in rock {
        for ((mut sx, mut sy), (mut ex, mut ey)) in line.iter().tuple_windows() {
            if sy > ey {
                (sy, ey) = (ey, sy);
            }
            if sx > ex {
                (sx, ex) = (ex, sx);
            }
            if sx == ex {
                for y in sy..=ey {
                    non_air_points
                        .entry(sx)
                        .or_insert_with(BTreeMap::new)
                        .insert(y, NonAir::Rock);
                }
            } else if sy == ey {
                for x in sx..=ex {
                    non_air_points
                        .entry(x)
                        .or_insert_with(BTreeMap::new)
                        .insert(sy, NonAir::Rock);
                }
            } else {
                unreachable!("lines aren't horizontal/vertical")
            }
        }
    }
    let non_air_points = non_air_points;

    let part1 = {
        let mut out = 0;
        let mut non_air_points = non_air_points.clone();

        'l: loop {
            let mut cx = 500;
            let mut cy = 0;
            'o: loop {
                let Some(cur_column) = non_air_points.get(&cx) else {
                    break 'l;
                };
                // minus one to get our landing spot
                cy = match cur_column.range((cy + 1)..).next() {
                    Some((new_y, _)) => *new_y - 1,
                    None => break 'l,
                };
                // below me is definitely solid
                // try left
                if non_air_points
                    .get(&(cx - 1))
                    .and_then(|col| col.get(&(cy + 1)))
                    .is_none()
                {
                    cx -= 1;
                    cy += 1;
                } else if non_air_points
                    .get(&(cx + 1))
                    .and_then(|col| col.get(&(cy + 1)))
                    .is_none()
                {
                    cx += 1;
                    cy += 1;
                } else {
                    // settled
                    non_air_points
                        .get_mut(&cx)
                        .expect("cx lookup failed after it succeeded?")
                        .insert(cy, NonAir::Sand);
                    out += 1;
                    break 'o;
                }
            }
        }

        out
    };

    let part2 = {
        let mut out = 0;
        let mut non_air_points = non_air_points;
        let floor = non_air_points
            .iter()
            .flat_map(|(_x, tree)| tree.iter().map(|(y, _)| y))
            .max()
            .expect("couldn't find highest y")
            + 2;

        for column in non_air_points.values_mut() {
            column.insert(floor, NonAir::Rock);
        }

        'l: loop {
            let mut cx = 500;
            let mut cy = 0;
            'o: loop {
                let cur_column = non_air_points
                    .entry(cx)
                    .or_insert_with(|| BTreeMap::from([(floor, NonAir::Rock)]));
                // minus one to get our landing spot
                cy = match cur_column.range(cy..).next() {
                    Some((&new_y, _)) => {
                        if new_y == cy {
                            break 'l;
                        }
                        new_y - 1
                    }
                    None => {
                        unreachable!("???");
                    }
                };
                // below me is definitely solid
                // try left
                if non_air_points
                    .entry(cx - 1)
                    .or_insert_with(|| BTreeMap::from([(floor, NonAir::Rock)]))
                    .get(&(cy + 1))
                    .is_none()
                {
                    cx -= 1;
                    cy += 1;
                } else if non_air_points
                    .entry(cx + 1)
                    .or_insert_with(|| BTreeMap::from([(floor, NonAir::Rock)]))
                    .get(&(cy + 1))
                    .is_none()
                {
                    cx += 1;
                    cy += 1;
                } else {
                    // settled
                    non_air_points
                        .get_mut(&cx)
                        .expect("cx lookup failed after it succeeded?")
                        .insert(cy, NonAir::Sand);
                    out += 1;
                    break 'o;
                }
            }
        }

        out
    };

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"];
