use std::{collections::HashSet, env, fs};

use itertools::Itertools;

fn solve(inp: &str) -> (i64, i64) {
    let chars = inp.chars().collect::<Vec<_>>();
    let (part1, _first_marker) = chars
        .windows(4)
        .find_position(|window| HashSet::<&char>::from_iter(window.iter()).len() == 4)
        .unwrap();
    let part1 = part1 as i64 + 4;
    let (part2, _first_marker) = chars
        .windows(14)
        .find_position(|window| HashSet::<&char>::from_iter(window.iter()).len() == 14)
        .unwrap();
    let part2 = part2 as i64 + 14;
    (part1, part2)
}

fn main() {
    dbg!(solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb"));
    dbg!(solve("bvwbjplbgvbhsrlpgdmjqwftvncz"));
    dbg!(solve("nppdvjthqldpwncqszvftbrmjlhg"));
    dbg!(solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"));
    dbg!(solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"));

    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (part1, part2) = solve(&contents);
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
