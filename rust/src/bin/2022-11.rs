use std::collections::HashMap;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

const PART3_OPS: u64 = 1_000_000_000 * 60 * 60 * 24;

#[derive(Debug)]
enum Operation {
    Add(u64),
    Mul(u64),
    Square,
}

impl Operation {
    fn apply(&self, old: u64) -> u64 {
        match self {
            Operation::Add(x) => old + x,
            Operation::Mul(x) => old * x,
            Operation::Square => old * old,
        }
    }
}

#[derive(Debug)]
struct Monkey {
    initial_items: Vec<u64>,
    operation: Operation,
    test: u64,
    if_true: u8,
    if_false: u8,
}

impl Monkey {
    /// Returns (new worry level, monkey thrown to).
    /// Does no mutation!
    fn round_part1(&self, item: u64) -> (u64, u8) {
        // inspect
        let item = self.operation.apply(item);
        // bored
        let item = item / 3;
        let recipient = if item % self.test == 0 {
            self.if_true
        } else {
            self.if_false
        };
        (item, recipient)
    }

    fn round_part2(&self, item: u64) -> (u64, u8) {
        // inspect
        let item = self.operation.apply(item);
        let recipient = if item % self.test == 0 {
            self.if_true
        } else {
            self.if_false
        };
        (item, recipient)
    }
}

fn solve(inp: &str) -> (usize, usize) {
    let monkeys = inp
        .split_terminator("\n\n")
        .enumerate()
        .map(|(i, monkey)| {
            let (header, items, operation, test, if_true, if_false) = monkey
                .lines()
                .collect_tuple()
                .expect("monkey note didn't have 5 things");
            assert_eq!(header, format!("Monkey {}:", i));
            let items = items
                .strip_prefix("  Starting items: ")
                .expect("unexpected monkey note second line")
                .split(", ")
                .map(|item| item.parse().expect("unexpected monkey item"))
                .collect::<Vec<_>>();
            let operation = operation
                .strip_prefix("  Operation: new = old ")
                .expect("unexpected moneky note third line");
            let operation = if operation == "* old" {
                Operation::Square
            } else if let Some(x) = operation.strip_prefix("* ") {
                Operation::Mul(x.parse().expect("unexpected * RHS"))
            } else if let Some(x) = operation.strip_prefix("+ ") {
                Operation::Add(x.parse().expect("unexpected + RHS"))
            } else {
                unimplemented!("unexpected operation {}", operation)
            };
            let test = test
                .strip_prefix("  Test: divisible by ")
                .expect("unexpected monkey test")
                .parse()
                .expect("monkey test wasn't int");
            let if_true = if_true
                .strip_prefix("    If true: throw to monkey ")
                .expect("unexpected monkey if true")
                .parse()
                .expect("monkey if true wasn't int");
            assert_ne!(if_true as usize, i, "monkey would throw to itself if true");
            let if_false = if_false
                .strip_prefix("    If false: throw to monkey ")
                .expect("unexpected monkey if true")
                .parse()
                .expect("monkey if true wasn't int");
            assert_ne!(
                if_false as usize, i,
                "monkey would throw to itself if false"
            );
            Monkey {
                initial_items: items,
                operation,
                test,
                if_true,
                if_false,
            }
        })
        .collect::<Vec<_>>();

    let part1 = {
        let mut monkey_items = monkeys
            .iter()
            .map(|monkey| monkey.initial_items.clone())
            .collect::<Vec<_>>();
        let mut ops = vec![0; monkeys.len()];
        for _round in 1..=20 {
            for (i, monkey) in monkeys.iter().enumerate() {
                // need to collect for borrow checker I think
                let new = monkey_items[i]
                    .iter()
                    .map(|item| monkey.round_part1(*item))
                    .collect::<Vec<_>>();
                for (new_worry, new_recepient) in new.iter() {
                    monkey_items[*new_recepient as usize].push(*new_worry);
                }
                monkey_items[i].clear();
                ops[i] += new.len();
            }
        }
        ops.sort_unstable();
        ops.iter().rev().take(2).product()
    };

    // use the fact that everything is (co)prime
    let lcm = monkeys
        .iter()
        .map(|monkey| monkey.test)
        .unique()
        .product::<u64>();

    let part2 = {
        let mut monkey_items = monkeys
            .iter()
            .map(|monkey| monkey.initial_items.clone())
            .collect::<Vec<_>>();
        let mut ops = vec![0; monkeys.len()];
        for _round in 1..=10000 {
            for (i, monkey) in monkeys.iter().enumerate() {
                // need to collect for borrow checker I think
                let new = monkey_items[i]
                    .iter()
                    .map(|item| monkey.round_part2(*item))
                    .collect::<Vec<_>>();
                for (new_worry, new_recepient) in new.iter() {
                    monkey_items[*new_recepient as usize].push(*new_worry % lcm);
                }
                monkey_items[i].clear();
                ops[i] += new.len();
            }
        }
        ops.sort_unstable();
        ops.iter().rev().take(2).product()
    };

    let part3: u64 = {
        // Keep track of items and where they hop to.
        // They should finish within (product of test)s, which is around
        // 10 million ops.
        let mut ops = monkeys
            .iter()
            .enumerate()
            .flat_map(|(i, monkey)| monkey.initial_items.iter().map(move |item| (i, item)))
            .map(|(i, item)| {
                let mut cur_monkey = i as u8;
                let mut cur_item = *item as u64;
                // vec of "what monkeys threw this item during this 0-indexed round"
                // as a vector of bitsets
                let mut monkey_history = vec![];
                let mut history = HashMap::<(u64, u8), usize>::new();
                let loop_start = loop {
                    let entry = history.entry((cur_item, cur_monkey));
                    match entry {
                        std::collections::hash_map::Entry::Occupied(o) => {
                            break *o.get();
                        }
                        std::collections::hash_map::Entry::Vacant(v) => {
                            v.insert(monkey_history.len());
                        }
                    };
                    let mut monkey_history_entry = 0u8;
                    loop {
                        monkey_history_entry |= 1 << cur_monkey;
                        let old_cur_monkey = cur_monkey;
                        (cur_item, cur_monkey) = monkeys[cur_monkey as usize].round_part2(cur_item);
                        cur_item %= lcm;
                        if cur_monkey < old_cur_monkey {
                            break;
                        }
                    }
                    monkey_history.push(monkey_history_entry);
                };
                let loop_length = monkey_history.len() - loop_start;
                let mut loop_ops = vec![0u64; monkeys.len()];
                for i in &monkey_history[loop_start..] {
                    for (bit, x) in loop_ops.iter_mut().enumerate() {
                        *x += ((i >> bit) & 1) as u64;
                    }
                }
                let mut out = vec![0u64; monkeys.len()];
                let first_part = PART3_OPS.min(loop_start as u64) as usize;
                let loop_part = PART3_OPS - (first_part as u64);
                let totals = loop_part / loop_length as u64;
                let remainder = loop_part % loop_length as u64;
                for i in &monkey_history[..first_part] {
                    for (bit, x) in out.iter_mut().enumerate() {
                        *x += ((i >> bit) & 1) as u64;
                    }
                }
                for (i, x) in loop_ops.iter().enumerate() {
                    out[i] += *x * totals;
                }
                for i in &monkey_history[loop_start..][..remainder as usize] {
                    for (bit, x) in out.iter_mut().enumerate() {
                        *x += ((i >> bit) & 1) as u64;
                    }
                }
                out
            })
            .fold(vec![0u64; monkeys.len()], |a, b| {
                a.into_iter()
                    .zip(b.into_iter())
                    .map(|(x, y)| x + y)
                    .collect()
            });
        ops.sort_unstable();
        ops.iter().rev().take(2).sum()
    };
    dbg!(part3);

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"];
