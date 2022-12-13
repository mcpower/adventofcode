use std::cmp::Ordering;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

#[derive(Debug)]
enum Packet {
    Integer(i64),
    List(Vec<Packet>),
}

fn compare_iterable<'a, T, U>(left: T, right: U) -> Option<Ordering>
where
    T: Iterator<Item = &'a Packet>,
    U: Iterator<Item = &'a Packet>,
{
    left.zip(right)
        .map(|(x, y)| compare(x, y))
        .find(|c| *c != Ordering::Equal)
}

fn compare(left: &Packet, right: &Packet) -> Ordering {
    match (left, right) {
        (Packet::Integer(a), Packet::Integer(b)) => a.cmp(b),
        (a @ Packet::Integer(_), Packet::List(b)) => {
            match compare_iterable(Some(a).into_iter(), b.iter()) {
                Some(o) => o,
                None => 1.cmp(&b.len()),
            }
        }
        (a @ Packet::List(_), b @ Packet::Integer(_)) => compare(b, a).reverse(),
        (Packet::List(a), Packet::List(b)) => match compare_iterable(a.iter(), b.iter()) {
            Some(o) => o,
            None => a.len().cmp(&b.len()),
        },
    }
}

// from https://github.com/rust-lang/rust/issues/48731#issuecomment-370235493
fn slice_shift_char(a: &str) -> Option<(char, &str)> {
    let mut chars = a.chars();
    chars.next().map(|c| (c, chars.as_str()))
}

fn parse_partial(line: &str) -> (Packet, &str) {
    let (head, tail) = slice_shift_char(line).expect("tried to parse empty string");
    match head {
        '[' => {
            let mut tail = tail;
            let mut packets = vec![];
            loop {
                let (new_head, new_tail) = slice_shift_char(tail).expect("reached EOF before ]");
                match new_head {
                    ']' => {
                        tail = new_tail;
                        break;
                    }
                    ',' => {
                        tail = new_tail;
                        continue;
                    }
                    _ => {
                        let child_packet;
                        (child_packet, tail) = parse_partial(tail);
                        packets.push(child_packet);
                    }
                }
            }
            (Packet::List(packets), tail)
        }
        digit if digit.is_numeric() => {
            let (digits, tail) = line.split_at(
                line.chars()
                    .take_while(|char| char.is_numeric())
                    .map(|char| char.len_utf8())
                    .sum(),
            );
            (
                Packet::Integer(
                    digits
                        .parse()
                        .expect("numeric string can't be parsed as i64??"),
                ),
                tail,
            )
        }
        _ => unreachable!("first char of packet was not [ or a digit: {}", head),
    }
}

fn parse(line: &str) -> Packet {
    let (parsed, rest) = parse_partial(line);
    assert_eq!(rest, "", "didn't fully parse line");
    parsed
}

fn solve(inp: &str) -> (usize, i64) {
    let pairs = inp
        .split_terminator("\n\n")
        .map(|pair| {
            pair.lines()
                .map(parse)
                .collect_tuple::<(_, _)>()
                .expect("para didn't have two lines")
        })
        .collect::<Vec<_>>();
    let part1 = pairs
        .iter()
        .enumerate()
        .filter(|(_i, (a, b))| compare(a, b) == Ordering::Less)
        .map(|(i, _pair)| i + 1)
        .sum();

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"];
