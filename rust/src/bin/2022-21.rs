use std::{cmp::Ordering, collections::HashMap};

use mcpower_aoc::runner::run_samples_and_arg;

#[derive(Debug, Clone)]
enum Job<'a> {
    Num(i64),
    Add(&'a str, &'a str),
    Sub(&'a str, &'a str),
    Mul(&'a str, &'a str),
    Div(&'a str, &'a str),
}

fn compute_result<'a>(monkey: &'a str, monkeys: &HashMap<&'a str, Job<'a>>) -> i64 {
    match *monkeys.get(monkey).unwrap() {
        Job::Num(num) => num,
        Job::Add(a, b) => compute_result(a, monkeys) + compute_result(b, monkeys),
        Job::Sub(a, b) => compute_result(a, monkeys) - compute_result(b, monkeys),
        Job::Mul(a, b) => compute_result(a, monkeys) * compute_result(b, monkeys),
        Job::Div(a, b) => {
            let a = compute_result(a, monkeys);
            let b = compute_result(b, monkeys);
            assert_eq!(a % b, 0, "division resulted in remainder");
            a / b
        }
    }
}

fn compute_result_part2<'a>(
    monkey: &'a str,
    monkeys: &HashMap<&'a str, Job<'a>>,
    me: i64,
) -> Option<i64> {
    let job = if monkey == "humn" {
        return Some(me);
    } else {
        monkeys.get(monkey).unwrap()
    };
    Some(match *job {
        Job::Num(num) => num,
        Job::Add(a, b) => {
            compute_result_part2(a, monkeys, me)? + compute_result_part2(b, monkeys, me)?
        }
        Job::Sub(a, b) => {
            compute_result_part2(a, monkeys, me)? - compute_result_part2(b, monkeys, me)?
        }
        Job::Mul(a, b) => {
            compute_result_part2(a, monkeys, me)? * compute_result_part2(b, monkeys, me)?
        }
        Job::Div(a, b) => {
            let a = compute_result_part2(a, monkeys, me)?;
            let b = compute_result_part2(b, monkeys, me)?;
            if a % b != 0 {
                return None;
            }
            a / b
        }
    })
}

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let monkeys: HashMap<&str, Job> = {
        inp.lines()
            .map(|line| {
                let (name, job) = line.split_once(": ").unwrap();
                let job = match *job.split_whitespace().collect::<Vec<_>>().as_slice() {
                    [num] => Job::Num(num.parse().unwrap()),
                    [left, "+", right] => Job::Add(left, right),
                    [left, "-", right] => Job::Sub(left, right),
                    [left, "*", right] => Job::Mul(left, right),
                    [left, "/", right] => Job::Div(left, right),
                    _ => unreachable!(),
                };
                (name, job)
            })
            .collect()
    };
    // TODO: assert tree and not dag
    let part1 = compute_result("root", &monkeys);

    let part2 = {
        let (left, right) = match *monkeys.get("root").unwrap() {
            Job::Num(_) => unreachable!(),
            Job::Add(a, b) => (a, b),
            Job::Sub(a, b) => (a, b),
            Job::Mul(a, b) => (a, b),
            Job::Div(a, b) => (a, b),
        };
        let mut is_possibly_good_cache = HashMap::new();
        // as we know we have a dag, we can do a binary search :)
        // we should probably cache this...
        let mut is_possibly_good = |me: i64| {
            *is_possibly_good_cache.entry(me).or_insert_with(|| {
                Some(
                    compute_result_part2(left, &monkeys, me)?
                        .cmp(&compute_result_part2(right, &monkeys, me)?),
                )
            })
        };
        let mut is_good = |me: i64| {
            let mut left_me = me;
            let mut left = is_possibly_good(left_me);
            while left.is_none() {
                left_me -= 1;
                left = is_possibly_good(left_me);
            }
            let left = left.unwrap();

            let mut right_me = me;
            let mut right = is_possibly_good(right_me);
            while right.is_none() {
                right_me += 1;
                right = is_possibly_good(right_me);
            }
            let right = right.unwrap();

            match (left, right) {
                (Ordering::Equal, Ordering::Equal) => Ordering::Equal,
                (a, Ordering::Equal) => a,
                (Ordering::Equal, b) => b,
                (Ordering::Less, Ordering::Less) => Ordering::Less,
                (Ordering::Less, Ordering::Greater) => {
                    unreachable!("discontinuity and couldn't find equal")
                }
                (Ordering::Greater, Ordering::Less) => {
                    unreachable!("inverse discontinuity? this should never happen")
                }
                (Ordering::Greater, Ordering::Greater) => Ordering::Greater,
            }
        };
        // meta: we know AoC answers are always positive

        let lo_ordering = is_good(0);
        if lo_ordering.is_eq() {
            0
        } else {
            let mut lo = 0;
            let mut hi = 1;
            while is_good(hi) == lo_ordering {
                lo = hi;
                hi *= 2;
            }
            while hi - lo > 1 {
                let mid = lo + (hi - lo) / 2;
                let result = is_good(mid);
                if result == lo_ordering {
                    lo = mid;
                } else {
                    hi = mid;
                    if result.is_eq() {
                        break;
                    }
                }
            }
            assert!(is_good(hi).is_eq());

            hi
        }
    };

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"];
