use mc_aoc::{Day, Runner};

pub fn part1(inp: &str, sample: bool) -> String {
    let nums: Vec<i64> = if sample {
        inp.split(", ").map(|i| i.parse().unwrap()).collect()
    } else {
        inp.lines().map(|i| i.parse().unwrap()).collect()
    };
    nums.iter().sum::<i64>().to_string()
}

pub fn setup(r: &mut Runner) {
    let day = Day::new(2018, 1);
    r.add_solution(day, 1, &part1);
    r.add_samples(
        day,
        1,
        r#"
=-=-=-=-=-=-=-=-=-
+1, +1, +1
\/-\/-OUTPUT-\/-\/
3
=-=-=-=-=-=-=-=-=-
+1, +1, -2
\/-\/-OUTPUT-\/-\/
0
=-=-=-=-=-=-=-=-=-
-1, -2, -3
\/-\/-OUTPUT-\/-\/
-6
=-=-=-=-=-=-=-=-=-
"#,
    );
}
