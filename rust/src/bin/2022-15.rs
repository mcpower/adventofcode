use itertools::Itertools;
use mcpower_aoc::{runner::run_samples_and_arg, vector::Vec2};

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Range {
    /// Inclusive start.
    start: i64,
    /// Exclusive end.
    end: i64,
}

impl Range {
    fn new(start: i64, end: i64) -> Self {
        Self { start, end }
    }
}

const TUNING_X_MUL: i64 = 4000000;

fn solve(inp: &str, is_sample: bool) -> (i64, i64) {
    let part1_target_row = if is_sample { 10 } else { 2000000 };
    let part2_range = if is_sample { 20 } else { 4000000 };
    let sensors_beacons: Vec<(Vec2, Vec2)> = inp
        .lines()
        .map(|line| {
            let (sensor, beacon) = line.split_once(": ").expect("line didn't have ': '");
            let sensor = sensor
                .strip_prefix("Sensor at ")
                .expect("line didn't start with 'Sensor at'");
            let beacon = beacon
                .strip_prefix("closest beacon is at ")
                .expect("second part of line didn't start with 'closest beacon is at'");
            [sensor, beacon]
                .into_iter()
                .map(|s| {
                    let (x, y) = s.split_once(", ").expect("point didn't have ', '");
                    let x = x
                        .strip_prefix("x=")
                        .expect("first part of point didn't start with x=")
                        .parse()
                        .expect("couldn't parse x");
                    let y = y
                        .strip_prefix("y=")
                        .expect("second part of point didn't start with y=")
                        .parse()
                        .expect("couldn't parse y");
                    Vec2(x, y)
                })
                .collect_tuple()
                .expect("this should never happen")
        })
        .collect();
    let part1 = 'part1: {
        let mut ranges = sensors_beacons
            .iter()
            .filter_map(|(sensor, beacon)| {
                // [from, to)
                let dist = (*beacon - *sensor).norm_1();
                let dist_on_target_row = dist - (sensor.1 - part1_target_row).abs();
                if dist_on_target_row < 0 {
                    None
                } else {
                    Some(Range::new(
                        sensor.0 - dist_on_target_row,
                        sensor.0 + dist_on_target_row + 1,
                    ))
                }
            })
            .sorted();

        let mut visible = 0;
        let Some(mut cur_range) = ranges.next() else {
            break 'part1 0;
        };

        for range in ranges {
            if range.start > cur_range.end {
                visible += cur_range.end - cur_range.start;
                cur_range = range;
            } else {
                cur_range.end = range.end.max(cur_range.end);
            }
        }
        visible += cur_range.end - cur_range.start;

        let beacons = sensors_beacons
            .iter()
            .map(|(_sensor, beacon)| beacon)
            .filter(|beacon| beacon.1 == part1_target_row)
            .map(|beacon| beacon.0)
            .unique()
            .count();

        visible - (beacons as i64)
    };

    let part2 = 'part2: {
        for y in 0..=part2_range {
            let mut ranges = sensors_beacons
                .iter()
                .filter_map(|(sensor, beacon)| {
                    // [from, to)
                    let dist = (*beacon - *sensor).norm_1();
                    let dist_on_target_row = dist - (sensor.1 - y).abs();
                    if dist_on_target_row < 0 {
                        None
                    } else {
                        Some(Range::new(
                            (sensor.0 - dist_on_target_row).max(0),
                            (sensor.0 + dist_on_target_row + 1).min(part2_range + 1),
                        ))
                    }
                })
                .sorted();

            let mut cur_range = ranges.next().expect("found no range for whole row");
            if cur_range.start != 0 {
                assert_eq!(cur_range.start, 1);
                break 'part2 y;
            }

            for range in ranges {
                if range.start > cur_range.end {
                    assert_eq!(cur_range.end + 1, range.start);
                    break 'part2 cur_range.end * TUNING_X_MUL + y;
                } else {
                    cur_range.end = range.end.max(cur_range.end);
                }
            }

            // I forgot this in my initial code (but didn't forget the x=0 case!)
            if cur_range.end != part2_range + 1 {
                assert_eq!(cur_range.end, part2_range);
                break 'part2 cur_range.end * TUNING_X_MUL + y;
            }
        }
        unreachable!("couldn't find missing point")
    };

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"];
