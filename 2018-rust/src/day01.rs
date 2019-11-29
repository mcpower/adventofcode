use std::collections::HashSet;
use std::iter;

#[aoc(day01, part1)]
pub fn part1(inp: &str) -> String {
    inp.split_whitespace()
        .map(|num| num.parse::<i64>().expect("num parse failed"))
        .sum::<i64>()
        .to_string()
}

#[aoc(day01, part2)]
pub fn part2(inp: &str) -> String {
    // this doesn't contain the starting value of 0
    let frequencies = inp
        .split_whitespace()
        .map(|num| num.parse::<i64>().expect("num parse failed"))
        .cycle()
        .scan(0i64, |state, i| {
            *state += i;
            Some(*state)
        });

    let mut seen = HashSet::new();
    iter::once(0i64)
        .chain(frequencies)
        .find(|i| {
            if seen.contains(i) {
                true
            } else {
                seen.insert(i.clone());
                false
            }
        })
        .expect("this can never happen")
        .to_string()
}

#[test]
fn day01samples() {
assert_eq!(part1(r#"
+1
-2
+3
+1
"#.trim_start_matches('\n')), "3");

assert_eq!(part1(r#"
+1
+1
+1
"#.trim_start_matches('\n')), "3");

assert_eq!(part1(r#"
+1
+1
-2
"#.trim_start_matches('\n')), "0");

assert_eq!(part1(r#"
-1
-2
-3
"#.trim_start_matches('\n')), "-6");



assert_eq!(part2(r#"
+1
-2
+3
+1
"#.trim_start_matches('\n')), "2");

assert_eq!(part2(r#"
+1
-1
"#.trim_start_matches('\n')), "0");

assert_eq!(part2(r#"
+3
+3
+4
-2
-4
"#.trim_start_matches('\n')), "10");

assert_eq!(part2(r#"
-6
+3
+8
+5
-6
"#.trim_start_matches('\n')), "5");

assert_eq!(part2(r#"
+7
+7
-2
-7
-4
"#.trim_start_matches('\n')), "14");
}
