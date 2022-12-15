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

fn solve(inp: &str, is_sample: bool) -> (i64, i64) {
    let target_row = if is_sample { 10 } else { 2000000 };
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
                let dist_on_target_row = dist - (sensor.1 - target_row).abs();
                if dist_on_target_row < 0 {
                    None
                } else {
                    Some(dbg!(Range::new(
                        sensor.0 - dist_on_target_row,
                        sensor.0 + dist_on_target_row + 1,
                    )))
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
            .filter(|beacon| beacon.1 == target_row)
            .map(|beacon| beacon.0)
            .unique()
            .count();

        visible - (beacons as i64)
    };

    let part2 = 0;

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
