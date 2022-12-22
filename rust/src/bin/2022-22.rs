use mcpower_aoc::{runner::run_samples_and_arg, utils::slice_shift_char, vector::Vec2};

#[derive(Debug)]
enum Move {
    Forward(u64),
    Left,
    Right,
}

#[derive(Debug, Clone, Copy)]
enum Facing {
    Right = 0,
    Down = 1,
    Left = 2,
    Up = 3,
}

impl Facing {
    fn turn_left(&self) -> Facing {
        match *self {
            Facing::Right => Facing::Up,
            Facing::Down => Facing::Right,
            Facing::Left => Facing::Down,
            Facing::Up => Facing::Left,
        }
    }

    fn turn_right(&self) -> Facing {
        match *self {
            Facing::Right => Facing::Down,
            Facing::Down => Facing::Left,
            Facing::Left => Facing::Up,
            Facing::Up => Facing::Right,
        }
    }

    fn vec(&self) -> Vec2 {
        match *self {
            Facing::Right => Vec2(0, 1),
            Facing::Down => Vec2(1, 0),
            Facing::Left => Vec2(0, -1),
            Facing::Up => Vec2(-1, 0),
        }
    }
}

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let (map, path) = inp.split_once("\n\n").unwrap();
    let map: Vec<Vec<Option<bool>>> = map
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| match c {
                    '.' => Some(false),
                    '#' => Some(true),
                    ' ' => None,
                    _ => unreachable!(),
                })
                .collect()
        })
        .collect();
    let path = {
        let mut out = vec![];
        let mut path = path.trim();
        loop {
            let Some(idx) = path.find(['L', 'R']) else {
                break;
            };
            let num;
            (num, path) = path.split_at(idx);
            out.push(Move::Forward(num.parse().unwrap()));
            let l_or_r;
            (l_or_r, path) = slice_shift_char(path).unwrap();
            out.push(match l_or_r {
                'L' => Move::Left,
                'R' => Move::Right,
                _ => unreachable!(),
            });
        }
        if !path.is_empty() {
            out.push(Move::Forward(path.parse().unwrap()));
        }
        out
    };
    let start_pos = Vec2(
        0,
        map.first()
            .unwrap()
            .iter()
            .position(Option::is_some)
            .unwrap() as i64,
    );
    let start_dir = Facing::Right;
    let part1 = {
        let mut pos = start_pos;
        let mut dir = start_dir;

        for m in path {
            match m {
                Move::Forward(steps) => {
                    let delta = dir.vec();
                    for _ in 0..steps {
                        let Vec2(r, c) = pos + delta;
                        if 0 <= r {
                            let r = r as usize;
                            if let Some(row) = map.get(r) {
                                if 0 <= c {
                                    let c = c as usize;
                                    if let Some(thing) = row.get(c) {
                                        // hooray!
                                        match *thing {
                                            Some(true) => {
                                                // hit a wall, do nothing
                                                break;
                                            }
                                            Some(false) => {
                                                // new place found
                                                pos = Vec2(r as i64, c as i64);
                                                continue;
                                            }
                                            None => {
                                                // do nothing, as this means
                                                // that we hit empty space
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        // we didn't find something good...
                        // look in the direction opposite of your current
                        // facing as far as you can until you find the
                        // opposite edge of the board, then reappear there.
                        let new_pos = {
                            let mut old = pos;
                            let mut new = pos - delta;
                            loop {
                                let Vec2(r, c) = new;
                                if 0 <= r {
                                    let r = r as usize;
                                    if let Some(row) = map.get(r) {
                                        if 0 <= c {
                                            let c = c as usize;
                                            if let Some(thing) = row.get(c) {
                                                // hooray!
                                                if thing.is_some() {
                                                    old = new;
                                                    new = old - delta;
                                                    continue;
                                                }
                                                // do nothing, as this means
                                                // that we hit empty space
                                            }
                                        }
                                    }
                                }
                                break old;
                            }
                        };
                        // see whether we can move now
                        if map
                            .get(new_pos.0 as usize)
                            .unwrap()
                            .get(new_pos.1 as usize)
                            .unwrap()
                            .unwrap()
                        {
                            // hit a wall
                            break;
                        } else {
                            // new place found
                            pos = new_pos;
                        }
                    }
                }
                Move::Left => {
                    dir = dir.turn_left();
                }
                Move::Right => {
                    dir = dir.turn_right();
                }
            }
        }

        let Vec2(r, c) = pos;
        1000 * (1 + r) + 4 * (1 + c) + (dir as i64)
    };

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"];
