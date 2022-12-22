use std::cmp::Ordering;

use itertools::Itertools;
use mcpower_aoc::{runner::run_samples_and_arg, utils::slice_shift_char};

#[derive(Debug)]
enum Packet {
    Integer(i64),
    List(Vec<Packet>),
}

impl PartialEq for Packet {
    fn eq(&self, other: &Self) -> bool {
        self.cmp(other).is_eq()
    }
}

impl Eq for Packet {}

impl PartialOrd for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn compare_iterable<'a, T, U>(left: T, right: U) -> Option<Ordering>
where
    T: Iterator<Item = &'a Packet>,
    U: Iterator<Item = &'a Packet>,
{
    left.zip(right)
        .map(|(x, y)| x.cmp(y))
        .find(|c| *c != Ordering::Equal)
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Packet::Integer(a), Packet::Integer(b)) => a.cmp(b),
            (a @ Packet::Integer(_), Packet::List(b)) => {
                match compare_iterable(Some(a).into_iter(), b.iter()) {
                    Some(o) => o,
                    None => 1.cmp(&b.len()),
                }
            }
            (a @ Packet::List(_), b @ Packet::Integer(_)) => b.cmp(a).reverse(),
            (Packet::List(a), Packet::List(b)) => match compare_iterable(a.iter(), b.iter()) {
                Some(o) => o,
                None => a.len().cmp(&b.len()),
            },
        }
    }
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

fn solve(inp: &str, _is_sample: bool) -> (usize, usize) {
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
        .filter(|(_i, (a, b))| a < b)
        .map(|(i, _pair)| i + 1)
        .sum();

    let divider_1 = Packet::List(vec![Packet::List(vec![Packet::Integer(2)])]);
    let divider_2 = Packet::List(vec![Packet::List(vec![Packet::Integer(6)])]);

    let part2 = pairs
        .iter()
        .flat_map(|(a, b)| [a, b])
        .chain([&divider_1, &divider_2])
        .sorted()
        .enumerate()
        .filter(|(_i, packet)| **packet == divider_1 || **packet == divider_2)
        .map(|(i, _packet)| i + 1)
        .product();

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
