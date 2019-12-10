use std::collections::{HashMap, HashSet};

#[aoc(day06, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn num_orbits<'a>(
    s: &'a str,
    parents: &HashMap<&str, &'a str>,
    cache: &mut HashMap<&'a str, usize>,
) -> usize {
    if let Some(&cached) = cache.get(s) {
        cached
    } else {
        let out = 1 + num_orbits(parents.get(&s).unwrap(), parents, cache);
        cache.insert(s, out);
        out
    }
}

fn _part1(inp: &str, _sample: bool) -> String {
    let mut parents: HashMap<&str, &str> = HashMap::new();
    for s in inp.lines() {
        let mut it = s.split(')');
        let from = it.next().unwrap();
        let to = it.next().unwrap();

        parents.insert(to, from);
    }
    let mut cache: HashMap<&str, usize> = HashMap::new();
    cache.insert("COM", 0);

    parents
        .keys()
        .map(|s| num_orbits(s, &parents, &mut cache))
        .sum::<usize>()
        .to_string()
}

#[aoc(day06, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn ancestors<'a>(s: &'a str, parents: &HashMap<&'a str, &'a str>) -> HashSet<&'a str> {
    std::iter::successors(Some(s), |i| parents.get(i).cloned()).collect()
}

fn _part2(inp: &str, _sample: bool) -> String {
    let mut parents: HashMap<&str, &str> = HashMap::new();
    for s in inp.lines() {
        let mut it = s.split(')');
        let from = it.next().unwrap();
        let to = it.next().unwrap();

        parents.insert(to, from);
    }

    let you = ancestors("YOU", &parents);
    let san = ancestors("SAN", &parents);
    let out = you.symmetric_difference(&san).count() - 2;

    out.to_string()
}

#[rustfmt::skip]
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
