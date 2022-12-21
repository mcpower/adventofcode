use std::collections::HashMap;

use mcpower_aoc::runner::run_samples_and_arg;
use once_cell::unsync::OnceCell;

#[derive(Debug)]
enum Job<'a> {
    Num(i64),
    Add(&'a str, &'a str),
    Sub(&'a str, &'a str),
    Mul(&'a str, &'a str),
    Div(&'a str, &'a str),
}

fn compute_result<'a>(
    monkey: &'a str,
    monkeys: &HashMap<&'a str, Job<'a>>,
    monkey_results: &HashMap<&'a str, OnceCell<i64>>,
) -> i64 {
    *monkey_results.get(monkey).unwrap().get_or_init(|| {
        let job = monkeys.get(monkey).unwrap();
        match *job {
            Job::Num(num) => num,
            Job::Add(a, b) => {
                compute_result(a, monkeys, monkey_results)
                    + compute_result(b, monkeys, monkey_results)
            }
            Job::Sub(a, b) => {
                compute_result(a, monkeys, monkey_results)
                    - compute_result(b, monkeys, monkey_results)
            }
            Job::Mul(a, b) => {
                compute_result(a, monkeys, monkey_results)
                    * compute_result(b, monkeys, monkey_results)
            }
            Job::Div(a, b) => {
                let a = compute_result(a, monkeys, monkey_results);
                let b = compute_result(b, monkeys, monkey_results);
                assert_eq!(a % b, 0, "division resulted in remainder");
                a / b
            }
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
    let monkey_results: HashMap<&str, OnceCell<i64>> = monkeys
        .iter()
        .map(|(k, _v)| (*k, OnceCell::new()))
        .collect();
    let part1 = compute_result("root", &monkeys, &monkey_results);

    let part2 = 0;

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
