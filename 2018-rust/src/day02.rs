#[aoc(day02, part1)]
pub fn part1(inp: &str) -> String {
    let (twos, threes) = inp.split_whitespace()
        .map(|s| {
            let mut out = (false, false);
            for i in b'a'..=b'z' {
                match s.matches(i as char).count() {
                    2 => out.0 = true,
                    3 => out.1 = true,
                    _ => (),
                };
            }
            out
        }).fold((0, 0), |acc, x| (acc.0 + x.0 as i32, acc.1 + x.1 as i32));
    (twos * threes).to_string()
}

#[aoc(day02, part2)]
pub fn part2(inp: &str) -> String {
    let strings: Vec<_> = inp.split_whitespace().collect();
    let target_length = strings[0].len() - 1;
    strings.iter()
        .flat_map(|s| std::iter::repeat(s).zip(strings.iter()))
        .map(|(str1, str2)| {
            str1.chars().zip(str2.chars())
                .filter(|(c1, c2)| c1 == c2)
                .map(|(c, _)| c)
                .collect::<String>()
        }).find(|s| s.len() == target_length)
        .expect("Couldn't find an answer")
}

#[test]
fn day02samples() {
assert_eq!(part1(r#"
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"#.trim_start_matches('\n')), "12");

assert_eq!(part2(r#"
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"#.trim_start_matches('\n')), "fgij");
}
