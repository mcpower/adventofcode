use std::{collections::HashSet, env, fs};

#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq)]
struct Point(i64, i64);

impl Point {
    fn norm_inf(&self) -> i64 {
        self.0.abs().max(self.1.abs())
    }
}

impl std::ops::Add<Point> for Point {
    type Output = Point;

    fn add(self, rhs: Point) -> Self::Output {
        Point(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl std::ops::AddAssign<Point> for Point {
    fn add_assign(&mut self, rhs: Point) {
        self.0 += rhs.0;
        self.1 += rhs.1;
    }
}

impl std::ops::Neg for Point {
    type Output = Point;

    fn neg(self) -> Self::Output {
        Point(-self.0, -self.1)
    }
}

impl std::ops::Sub<Point> for Point {
    type Output = Point;

    fn sub(self, rhs: Point) -> Self::Output {
        Point(self.0 - rhs.0, self.1 - rhs.1)
    }
}

fn solve(inp: &str) -> (i64, i64) {
    let mut head = Point(0, 0);
    let mut tail = head;
    let mut tail_positions = HashSet::new();
    tail_positions.insert(tail);

    for line in inp.lines() {
        let (dir, num) = line.split_once(' ').expect("line didn't have space");
        let num = num.parse::<i64>().expect("second part of line wasn't num");
        let dir = match dir {
            "U" => Point(-1, 0),
            "D" => Point(1, 0),
            "L" => Point(0, -1),
            "R" => Point(0, 1),
            _ => unreachable!("dir wasn't UDLR"),
        };
        for _ in 0..num {
            head += dir;

            // update tail
            let delta = head - tail;
            if delta.norm_inf() > 1 {
                let tail_dir = Point(delta.0.signum(), delta.1.signum());
                // dbg!(tail_dir);
                tail += tail_dir;
                tail_positions.insert(tail);
            }
            // dbg!(head, tail);
        }
    }
    let part1 = tail_positions
        .len()
        .try_into()
        .expect("part1 overflowed i64?");

    let part2 = 0;
    (part1, part2)
}

fn main() {
    dbg!(solve(
        r"R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"
    ));
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (part1, part2) = solve(&contents);
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
