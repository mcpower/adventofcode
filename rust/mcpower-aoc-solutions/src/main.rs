use std::{env, fs};

fn main() {
    // 2022 Day 1
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let mut deers = contents
        .split("\n\n")
        .map(|deer| {
            deer.split_whitespace()
                .map(|weight| weight.parse::<i64>().expect("error parsing weight"))
                .sum::<i64>()
        })
        .collect::<Vec<_>>();

    deers.sort();
    deers.reverse();

    println!("part 1: {}", deers.get(0).expect("no deers?"));
    println!("part 2: {}", deers.iter().take(3).sum::<i64>());
}
