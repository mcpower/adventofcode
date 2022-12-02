use std::{env, fs};

enum Outcome {
    Loss,
    Tie,
    Win,
}

fn rps(opponent: &char, me: &char) -> Outcome {
    match (opponent, me) {
        (x, y) if x == y => Outcome::Tie,
        ('A', 'B') => Outcome::Win,
        ('B', 'C') => Outcome::Win,
        ('C', 'A') => Outcome::Win,
        _ => Outcome::Loss,
    }
}

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let matches = contents
        .split_terminator('\n')
        .map(|line| (line.chars().next().unwrap(), line.chars().nth(2).unwrap()))
        .collect::<Vec<_>>();

    let part1 = matches
        .iter()
        .map(|(opponent, me)| {
            (
                *opponent,
                match me {
                    'X' => 'A',
                    'Y' => 'B',
                    'Z' => 'C',
                    _ => unreachable!(),
                },
            )
        })
        .map(|(opponent, me)| {
            (match me {
                'A' => 1,
                'B' => 2,
                'C' => 3,
                _ => unreachable!(),
            }) + (match rps(&opponent, &me) {
                Outcome::Loss => 0,
                Outcome::Tie => 3,
                Outcome::Win => 6,
            })
        })
        .sum::<i64>();

    println!("part 1: {}", part1);
}
