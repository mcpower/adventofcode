use std::{collections::HashSet, env, fs};

use mcpower_aoc::vector::Point;

fn solve(inp: &str) -> (i64, i64) {
    let mut tails = [Point(0, 0); 10];
    let mut part1_seen = HashSet::new();
    let mut part2_seen = HashSet::new();
    part1_seen.insert(tails[1]);
    part2_seen.insert(tails[9]);

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
            tails[0] += dir;
            let mut head = tails[0];
            for tail in tails.iter_mut().skip(0) {
                let delta = head - *tail;
                if delta.norm_inf() > 1 {
                    let tail_dir = Point(delta.0.signum(), delta.1.signum());
                    *tail += tail_dir;
                }
                head = *tail;
            }

            part1_seen.insert(tails[1]);
            part2_seen.insert(tails[9]);
        }
    }
    let part1 = part1_seen.len().try_into().expect("part1 overflowed i64?");
    let part2 = part2_seen.len().try_into().expect("part2 overflowed i64?");
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
    dbg!(solve(
        r"R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"
    ));
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (part1, part2) = solve(&contents);
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
