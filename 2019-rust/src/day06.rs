use std::collections::HashMap;

#[aoc(day06, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let mut parents: HashMap<String, String> = HashMap::new();
    let mut children: HashMap<String, Vec<String>> = HashMap::new();
    for s in inp.lines() {
        let mut it = s.split(')');
        let from = it.next().unwrap().to_string();
        let to = it.next().unwrap().to_string();

        children.entry(from.clone()).or_insert_with(Vec::new).push(to.clone());
        parents.insert(to, from);
    }

    let orbits = |s: String| {
        let mut s = s;
        let mut o = 0;
        while s != "COM" {
            s = parents.get(&s).unwrap().clone();
            o += 1
        }
        o
    };
    parents.keys().map(|s| orbits(s.clone())).sum::<i32>().to_string()
}

#[aoc(day06, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let mut parents: HashMap<String, String> = HashMap::new();
    let mut children: HashMap<String, Vec<String>> = HashMap::new();
    for s in inp.lines() {
        let mut it = s.split(')');
        let from = it.next().unwrap().to_string();
        let to = it.next().unwrap().to_string();

        children.entry(from.clone()).or_insert_with(Vec::new).push(to.clone());
        parents.insert(to, from);
    }

    let orbits = |s: String| {
        let mut s = s;
        let mut out = vec![];
        while s != "COM" {
            out.push(s.clone());
            s = parents.get(&s).unwrap().clone();
        }
        out
    };

    let out = |a: String, b: String| {
        let mut x = orbits(a);
        x.reverse();
        let mut y = orbits(b);
        y.reverse();
        let mut i = 0usize;
        while i < x.len().min(y.len()) && x[i] == y[i] {
            i += 1;
        }
        x.len() + y.len() - 2*(i) - 2
    };

    out("YOU".to_string(), "SAN".to_string()).to_string()
}

#[test]
fn day06samples() {
assert_eq!(_part1(r#"
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"#.trim_matches('\n'), true), "42");

assert_eq!(_part2(r#"
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"#.trim_matches('\n'), true), "4");
}
