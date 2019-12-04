#[aoc(day04, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let split: Vec<_> = inp.split('-').collect();
    let from: i32 = split[0].parse().unwrap();
    let to: i32 = split[1].parse().unwrap();
    (from..=to)
        .map(|n| n.to_string())
        .filter(|s| {
            s.chars().zip(s.chars().skip(1)).all(|(x, y)| x <= y)
        })
        .filter(|s| {
            s.chars().zip(s.chars().skip(1)).any(|(x, y)| x == y)
        })
        .count()
        .to_string()
}

#[aoc(day04, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let split: Vec<_> = inp.split('-').collect();
    let from: i32 = split[0].parse().unwrap();
    let to: i32 = split[1].parse().unwrap();
    (from..=to)
        .map(|n| n.to_string())
        .filter(|s| {
            s.chars().zip(s.chars().skip(1)).all(|(x, y)| x <= y)
        })
        .filter(|s| {
            let mut out = false;
            let mut streak = 1;
            s.chars().zip(s.chars().skip(1)).for_each(|(x, y)| {
                if x == y {
                    streak += 1;
                } else {
                    if streak == 2 {
                        out = true;
                    }
                    streak = 1;
                }
            });
            out || streak == 2
        })
        .count()
        .to_string()
}

#[test]
fn day04samples() {
assert_eq!(_part1(r#"
111111-111111
"#.trim_matches('\n'), true), "1");
    assert_eq!(_part1(r#"
223450-223450
"#.trim_matches('\n'), true), "0");
    assert_eq!(_part1(r#"
123789-123789
"#.trim_matches('\n'), true), "0");

    assert_eq!(_part2(r#"
112233-112233
"#.trim_matches('\n'), true), "1");
    assert_eq!(_part2(r#"
123444-123444
"#.trim_matches('\n'), true), "0");
    assert_eq!(_part2(r#"
111122-111122
"#.trim_matches('\n'), true), "1");
}
