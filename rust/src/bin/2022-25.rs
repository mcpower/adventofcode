use mcpower_aoc::runner::run_samples_and_arg;

fn to_snafu(mut cur: i64) -> String {
    // what num would overestimate it?
    // snafu of n digits can go up to 5^n * 3 ish
    let mut out = vec![];

    while cur != 0 {
        out.push(cur % 5);
        cur /= 5;
    }
    out.push(0);
    out.reverse();

    let mut i = 1;
    loop {
        if i >= out.len() {
            break;
        }
        let cur_digit = out[i];
        if cur_digit == 3 || cur_digit == 4 {
            // 3 or 4
            out[i] = -(5 - cur_digit);
            out[i - 1] += 1;
            i -= 1;
        } else {
            i += 1;
        }
    }
    if out[0] == 0 {
        out.remove(0);
    }

    out.iter()
        .map(|x| match *x {
            2 => '2',
            1 => '1',
            0 => '0',
            -1 => '-',
            -2 => '=',
            _ => unreachable!(),
        })
        .collect()
}

fn solve(inp: &str, _is_sample: bool) -> (String, i64) {
    let part1 = inp
        .lines()
        .map(|line| {
            let chars = line.chars().collect::<Vec<_>>();
            chars
                .iter()
                .enumerate()
                .map(|(i, c)| {
                    5i64.pow((chars.len() - i - 1) as u32) * {
                        match *c {
                            '2' => 2,
                            '1' => 1,
                            '0' => 0,
                            '-' => -1,
                            '=' => -2,
                            _ => unreachable!(),
                        }
                    }
                })
                .sum::<i64>()
        })
        .sum::<i64>();
    let part1 = to_snafu(part1);

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[
    r"
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
",
    r"

",
    r"

",
    r"

",
];
