use std::collections::HashMap;

use mcpower_aoc::{runner::run_samples_and_arg, utils::slice_shift_char, vector::Vec2};

// Part 2: Imagine the outside of a cube defined as:
//
// height (going up outside the page, NOT into the page)
//     _
//    |\
//      \
//       +-----> col
//       |
//       |
//       |
//       v
//      row
//
// starting at (0, 0, 0) and ending at (1, 1, 1).
// (r, c, h) forms a right-handed basis, albeit in a weird way. Try rotating the
// above 90 degrees counter-clockwise to get a more familiar (x, y, z)
// co-ordinate system.
// We define faces of the cube to be when {r, c, h} = {0, 1}, and we define
// "seams" of the cube to be combinations of these with different variables -
// for example, there isn't a seam from r = 0 to r = 1, but there is a seam from
// r = 0 to c = 0 (the "height" arrow in the above diagram).
// For each seam, we associate two tuples of
//   (face, which edge (UDLR) in map)
// to it. We shouldn't? need to worry about the direction of the seam - if we
// assume everything is facing inwards into the cube, we shouldn't need to do
// any "reflections", just "rotations".
//
// (some coding later)
//
// Turns out that we do need to worry about the direction of the seam...
// Ignore everything - just keep track of what's up/down/left/right of me.

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum Move {
    Forward(u64),
    Left,
    Right,
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum Facing {
    Right = 0,
    Down = 1,
    Left = 2,
    Up = 3,
}

impl Facing {
    /// Also "counterclockwise".
    fn turn_left(self) -> Facing {
        match self {
            Facing::Right => Facing::Up,
            Facing::Down => Facing::Right,
            Facing::Left => Facing::Down,
            Facing::Up => Facing::Left,
        }
    }

    /// Also "clockwise".
    fn turn_right(self) -> Facing {
        match self {
            Facing::Right => Facing::Down,
            Facing::Down => Facing::Left,
            Facing::Left => Facing::Up,
            Facing::Up => Facing::Right,
        }
    }

    fn turn_around(self) -> Facing {
        match self {
            Facing::Right => Facing::Left,
            Facing::Down => Facing::Up,
            Facing::Left => Facing::Right,
            Facing::Up => Facing::Down,
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

    // Returns (right, down, left, up).
    fn values() -> &'static [Facing; 4] {
        static VALUES: [Facing; 4] = [Facing::Right, Facing::Down, Facing::Left, Facing::Up];
        &VALUES
    }
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum Dimension {
    Row,
    Col,
    Height,
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum ZeroOne {
    Zero,
    One,
}

impl ZeroOne {
    fn flip(&self) -> Self {
        match *self {
            Self::Zero => Self::One,
            Self::One => Self::Zero,
        }
    }
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
struct Face {
    dimension: Dimension,
    value: ZeroOne,
}

impl Face {
    fn flip(&self) -> Self {
        Self {
            dimension: self.dimension,
            value: self.value.flip(),
        }
    }
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
struct Neighbours {
    right: Face,
    down: Face,
    left: Face,
    up: Face,
}

impl Neighbours {
    fn get_face(&self, facing: Facing) -> Face {
        match facing {
            Facing::Right => self.right,
            Facing::Down => self.down,
            Facing::Left => self.left,
            Facing::Up => self.up,
        }
    }
}

fn solve(inp: &str, is_sample: bool) -> (i64, i64) {
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

    let cube_size = if is_sample { 4 } else { 50 };
    let is_valid_cube_pos = |Vec2(row, col): Vec2| {
        (|| {
            *map.get(usize::try_from(row).ok()? * cube_size)?
                .get(usize::try_from(col).ok()? * cube_size)?
        })()
        .is_some()
    };
    let start_cube_pos = start_pos / (cube_size as i64);
    assert!(is_valid_cube_pos(start_cube_pos));
    // assign height=0 to start_cube_pos
    let first = Face {
        dimension: Dimension::Height,
        value: ZeroOne::Zero,
    };

    let mut cube_pos_assignments = HashMap::<Vec2, Face>::new();
    let mut inv_cube_pos_assignments = HashMap::<Face, Vec2>::new();
    cube_pos_assignments.insert(start_cube_pos, first);
    inv_cube_pos_assignments.insert(first, start_cube_pos);
    let mut face_neighbours = HashMap::<Face, Neighbours>::new();
    face_neighbours.insert(
        first,
        Neighbours {
            right: Face {
                dimension: Dimension::Col,
                value: ZeroOne::One,
            },
            down: Face {
                dimension: Dimension::Row,
                value: ZeroOne::One,
            },
            left: Face {
                dimension: Dimension::Col,
                value: ZeroOne::Zero,
            },
            up: Face {
                dimension: Dimension::Row,
                value: ZeroOne::Zero,
            },
        },
    );

    // establish all map connections
    let mut stack = vec![start_cube_pos];
    while let Some(popped_cube_pos) = stack.pop() {
        let face = *cube_pos_assignments.get(&popped_cube_pos).unwrap();
        let neighbours = *face_neighbours.get(&face).unwrap();
        for dir in Facing::values() {
            let new_cube_pos = popped_cube_pos + dir.vec();
            if !is_valid_cube_pos(new_cube_pos) || cube_pos_assignments.contains_key(&new_cube_pos)
            {
                continue;
            }
            let new_face = neighbours.get_face(*dir);
            assert!(!face_neighbours.contains_key(&new_face));
            let new_neighbours = {
                let mut out = neighbours;
                match *dir {
                    Facing::Right => {
                        // left is now old, right is now old flipped
                        out.left = face;
                        out.right = face.flip();
                    }
                    Facing::Down => {
                        out.up = face;
                        out.down = face.flip();
                    }
                    Facing::Left => {
                        out.right = face;
                        out.left = face.flip();
                    }
                    Facing::Up => {
                        out.down = face;
                        out.up = face.flip();
                    }
                }
                out
            };
            cube_pos_assignments.insert(new_cube_pos, new_face);
            inv_cube_pos_assignments.insert(new_face, new_cube_pos);
            face_neighbours.insert(new_face, new_neighbours);
            stack.push(new_cube_pos);
        }
    }

    let solve = |part_2: bool| {
        let mut pos = start_pos;
        let mut dir = start_dir;

        for &m in &path {
            match m {
                Move::Forward(steps) => {
                    for _ in 0..steps {
                        let Vec2(r, c) = pos + dir.vec();
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
                        let (new_pos, new_dir) = if part_2 {
                            // we didn't find something good...
                            // which cube pos are we currently in?
                            let cube_pos = pos / (cube_size as i64);
                            assert!(is_valid_cube_pos(cube_pos));
                            let face = *cube_pos_assignments.get(&cube_pos).unwrap();
                            let neighbours = *face_neighbours.get(&face).unwrap();

                            // which cube pos
                            let target_face = neighbours.get_face(dir);
                            let target_cube_pos =
                                *inv_cube_pos_assignments.get(&target_face).unwrap();

                            // which side of the target did we come from?
                            let target_face_side = {
                                let target_face_neighbours =
                                    face_neighbours.get(&target_face).unwrap();
                                if face == target_face_neighbours.right {
                                    Facing::Right
                                } else if face == target_face_neighbours.down {
                                    Facing::Down
                                } else if face == target_face_neighbours.left {
                                    Facing::Left
                                } else {
                                    assert_eq!(face, target_face_neighbours.up);
                                    Facing::Up
                                }
                            };

                            // which direction should we be facing?
                            let new_dir = target_face_side.turn_around();

                            // where were we on the edge?
                            // (going clockwise, 0 to cube_size-1)
                            let start_edge_pos = match dir {
                                Facing::Right => {
                                    // only interested in row
                                    pos.0 - cube_pos.0 * (cube_size as i64)
                                }
                                Facing::Down => {
                                    // inverted!
                                    // only interested in col
                                    (cube_size as i64 - 1)
                                        - (pos.1 - cube_pos.1 * (cube_size as i64))
                                }
                                Facing::Left => {
                                    // inverted!
                                    // only interested in row
                                    (cube_size as i64 - 1)
                                        - (pos.0 - cube_pos.0 * (cube_size as i64))
                                }
                                Facing::Up => {
                                    // only interested in col
                                    pos.1 - cube_pos.1 * (cube_size as i64)
                                }
                            };
                            // where should we be on the new edge?
                            let end_edge_pos = (cube_size as i64 - 1) - start_edge_pos;
                            let new_pos = {
                                let top_left = target_cube_pos * (cube_size as i64);
                                let pos_in_cube_side = match target_face_side {
                                    Facing::Right => Vec2(end_edge_pos, cube_size as i64 - 1),
                                    Facing::Down => Vec2(
                                        cube_size as i64 - 1,
                                        cube_size as i64 - 1 - end_edge_pos,
                                    ),
                                    Facing::Left => Vec2((cube_size as i64 - 1) - end_edge_pos, 0),
                                    Facing::Up => Vec2(0, end_edge_pos),
                                };
                                top_left + pos_in_cube_side
                            };
                            (new_pos, new_dir)
                        } else {
                            let mut old = pos;
                            let mut new = pos - dir.vec();
                            let new_pos = loop {
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
                                                    new = old - dir.vec();
                                                    continue;
                                                }
                                                // do nothing, as this means
                                                // that we hit empty space
                                            }
                                        }
                                    }
                                }
                                break old;
                            };
                            (new_pos, dir)
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
                            dir = new_dir;
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

    (solve(false), solve(true))
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
