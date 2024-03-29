use std::{collections::HashSet, env, fs};

fn main() {
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");
    let lines = contents.lines().collect::<Vec<_>>();

    let part1 = lines
        .iter()
        .map(|line| {
            let count = line.chars().count();

            let left = HashSet::<char>::from_iter(line.chars().take(count / 2));
            let right = HashSet::from_iter(line.chars().skip(count / 2));

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

    assert_eq!(lines.len() % 3, 0, "lines aren't divisible by 3");
    let part2 = lines
        .chunks_exact(3)
        .map(|lines| {
            let &[a, b, c] = lines else {unreachable!("chunks_exact didn't give us three things")};

            let a = HashSet::<char>::from_iter(a.chars());
            let b = HashSet::from_iter(b.chars());
            let c = HashSet::from_iter(c.chars());

            let a_and_b = &a & &b;
            let mut intersection = a_and_b.intersection(&c);
            let out = intersection
                .next()
                .expect("three elves had nothing in common");
            assert_eq!(
                intersection.next(),
                None,
                "three elves had more than one thing in common"
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
    println!("part 2: {}", part2);
}
