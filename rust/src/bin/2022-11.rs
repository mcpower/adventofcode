use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;

#[derive(Debug)]
enum Operation {
    Add(i64),
    Mul(i64),
    Square,
}

impl Operation {
    fn apply(&self, old: i64) -> i64 {
        match self {
            Operation::Add(x) => old + x,
            Operation::Mul(x) => old * x,
            Operation::Square => old * old,
        }
    }
}

#[derive(Debug)]
struct Monkey {
    initial_items: Vec<i64>,
    operation: Operation,
    test: i64,
    if_true: usize,
    if_false: usize,
}

impl Monkey {
    /// Returns (new worry level, monkey thrown to).
    /// Does no mutation!
    fn round(&self, item: i64) -> (i64, usize) {
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
}

fn solve(inp: &str) -> (usize, i64) {
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
                .map(|item| item.parse::<i64>().expect("unexpected monkey item"))
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
            assert_ne!(if_true, i, "monkey would throw to itself if true");
            let if_false = if_false
                .strip_prefix("    If false: throw to monkey ")
                .expect("unexpected monkey if true")
                .parse()
                .expect("monkey if true wasn't int");
            assert_ne!(if_false, i, "monkey would throw to itself if false");
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
        let mut ops = monkeys.iter().map(|_| 0).collect::<Vec<_>>();
        for _round in 1..=20 {
            for (i, monkey) in monkeys.iter().enumerate() {
                // need to collect for borrow checker I think
                let new = monkey_items[i]
                    .iter()
                    .map(|item| monkey.round(*item))
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

    let part2 = 0;

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
