#[aoc(day01, part1)]
pub fn real_part1(inp: &str) -> String {
    part1(inp, false)
}

fn part1(inp: &str, _sample: bool) -> String {
    inp.lines()
        .map(|s| s.parse::<i64>().unwrap())
        .map(|i| (i / 3) - 2)
        .sum::<i64>()
        .to_string()
}

#[aoc(day01, part2)]
pub fn real_part2(inp: &str) -> String {
    part2(inp, false)
}

fn part2(inp: &str, _sample: bool) -> String {
    inp.lines()
        .map(|s| s.parse::<i64>().unwrap())
        .map(|i| {
            let mut i = i;
            let mut out = 0i64;
            while i != 0 {
                i = ((i / 3) - 2).max(0);
                out += i;
            }
            out
        })
        .sum::<i64>()
        .to_string()
}

#[rustfmt::skip]
#[test]
fn day01samples() {
assert_eq!(part1(r#"
100756
"#.trim_matches('\n'), true), "33583");

assert_eq!(part2(r#"
100756
"#.trim_matches('\n'), true), "50346");
}
