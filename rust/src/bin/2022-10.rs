use std::{env, fs};

fn solve(inp: &str) -> (i64, i64) {
    // at the end of this cycle, x was...
    let mut history: Vec<i64> = vec![];
    let mut last = 1;
    for line in inp.lines() {
        if line == "noop" {
            history.push(last);
        } else if let Some(("addx", n)) = line.split_once(' ') {
            let n = n.parse::<i64>().expect("addx arg wasn't int");
            history.push(last);
            last += n;
            history.push(last);
        }
    }
    let part1 = history
        .iter()
        .enumerate()
        .skip(19)
        .step_by(40)
        .map(|(i, x)| (TryInto::<i64>::try_into(i).expect("size overflowed i64??") + 1) * x)
        .sum();
    let part2 = 0;
    (part1, part2)
}

fn main() {
    dbg!(solve(
        r"
noop
addx 3
addx -5
"
        .trim_start()
    ));
    dbg!(solve(
        r"
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop

"
        .trim_start()
    ));
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (part1, part2) = solve(&contents);
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}