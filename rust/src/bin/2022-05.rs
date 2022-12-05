use itertools::Itertools;
use regex::Regex;
use std::{env, fs};

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (stacks_str, operations) = contents
        .split("\n\n")
        .map(|para| para.lines().collect::<Vec<_>>())
        .collect_tuple()
        .expect("got more than two paras");

    // Eric is nice enough to add trailing spaces to the input :D
    let (numbers, stacks_str) = stacks_str.split_last().expect("stack was empty?");
    assert_eq!(
        (numbers.chars().count()) % 4,
        3,
        "length of stack row wasn't 3 mod 4"
    );
    let num_stacks = (numbers.chars().count() + 1) / 4;
    let mut stacks: Vec<Vec<char>> = std::iter::repeat_with(Vec::new).take(num_stacks).collect();
    for line in stacks_str {
        for (i, x) in line.chars().skip(1).step_by(4).enumerate() {
            if x.is_alphabetic() {
                stacks[i].push(x);
            }
        }
    }
    // The top of the stack is the first char we saw.
    stacks.iter_mut().for_each(|v| v.reverse());
    let re = Regex::new(r"^move (\d+) from (\d+) to (\d+)$").unwrap();

    for operation in operations {
        let (num, from, to) = re
            .captures(operation)
            .expect("operation didn't match regex")
            .iter()
            .skip(1) // first one is always the entire match
            .map(|opt| {
                opt.expect("capturing group didn't capture?")
                    .as_str()
                    .parse::<usize>()
                    .expect("capture wasn't number?")
            })
            .collect_tuple()
            .expect("didn't get 3 things from regex capture?");
        for _ in 0..num {
            let popped = stacks[from - 1].pop().expect("move made a stack empty");
            stacks[to - 1].push(popped);
        }
    }

    let part1 = stacks
        .iter()
        .map(|stack| stack.last().expect("end result had empty stacks?"))
        .join("");
    println!("part 1: {}", part1);

    let part2 = 0;
    println!("part 2: {}", part2);
}
