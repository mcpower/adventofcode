use std::{collections::HashSet, env, fs};

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");
    let lines = contents.lines();

    let part1 = lines
        .map(|line| {
            let count = line.chars().count();

            let mut left = HashSet::new();
            left.extend(line.chars().take(count / 2));
            let mut right = HashSet::new();
            right.extend(line.chars().skip(count / 2));

            let mut intersection = left.intersection(&right);
            let out = intersection
                .next()
                .expect("two rucksacks had nothing in common");
            assert_eq!(
                intersection.next(),
                None,
                "two rucksacks had more than one thing in common"
            );
            *out
        })
        .map(|common| {
            (common as i64)
                + match common {
                    'a'..='z' => 1 - 'a' as i64,
                    'A'..='Z' => 27 - 'A' as i64,
                    _ => unreachable!("common thing was not alphabetical"),
                }
        })
        .sum::<i64>();
    println!("part 1: {}", part1);
    let part2 = 0;
    println!("part 2: {}", part2);
}
