use std::{env, fs};

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let matches = contents
        .split_terminator('\n')
        .map(|line| (line.chars().next().unwrap(), line.chars().nth(2).unwrap()))
        .map(|(opponent, me)| (opponent as i64 - 'A' as i64, me as i64 - 'X' as i64))
        .collect::<Vec<_>>();

    let part1 = matches
        .iter()
        .map(|(opponent, me)| {
            // me - opponent = 0 if tie, 1 win, 2 if loss
            me + 1 + (me - opponent + 1).rem_euclid(3) * 3
        })
        .sum::<i64>();

    println!("part 1: {}", part1);
}
