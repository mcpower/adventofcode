use std::collections::{HashSet, HashMap};

type Point = (i64, i64);

fn parse(inp: &str) -> Vec<Vec<&str>> {
    inp.trim().lines().map(|s| s.split(',').collect()).collect()
}

fn run_wire(dirs: &[&str]) -> HashMap<Point, u64> {
    let mut cur = (0, 0);
    let mut dist = 0;
    let mut seen = HashMap::new();
    seen.insert(cur, dist);
    for direction in dirs {
        let mut chars = direction.chars();
        let way = match chars.next() {
            Some('R') => (0, 1),
            Some('L') => (0, -1),
            Some('U') => (-1, 0),
            Some('D') => (1, 0),
            _ => break,
        };
        // dbg!(&direction);
        let num = chars.collect::<String>().parse().unwrap();
        for _ in 0..num {
            cur.0 += way.0;
            cur.1 += way.1;
            dist += 1;

            seen.insert(cur, dist);
        }
    }
    seen
}

fn intersections(wires: &[HashMap<Point, u64>]) -> HashSet<Point> {
    let mut wire_coords_iter = wires
        .iter()
        .map(|wire| to_keys(&wire));

    let first_wire_coords = wire_coords_iter.next().unwrap();
    wire_coords_iter
        .fold(
            first_wire_coords,
            |acc, x| acc.intersection(&x).cloned().collect()
        )
}

fn to_keys<T: std::clone::Clone + std::cmp::Eq + std::hash::Hash, U>(map: &HashMap<T, U>) -> HashSet<T> {
    map.keys().cloned().collect::<HashSet<_>>()
}

#[aoc(day03, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let dirs = parse(inp);
    let wires: Vec<_> = dirs.into_iter().map(|dirs| run_wire(&dirs[..])).collect();
    
    intersections(&wires[..])
        .into_iter()
        .map(|(a, b)| i64::abs(a) + i64::abs(b))
        .filter(|&i| i != 0)
        .min()
        .unwrap()
        .to_string()
}

#[aoc(day03, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let dirs = parse(inp);
    let wires: Vec<_> = dirs.into_iter().map(|dirs| run_wire(&dirs[..])).collect();

    intersections(&wires[..])
        .into_iter()
        .map(|coord| wires.iter().map(|wire| wire.get(&coord).unwrap()).sum::<u64>())
        .filter(|&i| i != 0)
        .min()
        .unwrap()
        .to_string()
}

#[test]
fn day03samples() {
    assert_eq!(_part1(r#"
R8,U5,L5,D3
U7,R6,D4,L4
"#.trim_start_matches('\n'), true), "6");
assert_eq!(_part1(r#"
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
"#.trim_start_matches('\n'), true), "159");
assert_eq!(_part1(r#"
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
"#.trim_start_matches('\n'), true), "135");

assert_eq!(_part2(r#"
R8,U5,L5,D3
U7,R6,D4,L4
"#.trim_start_matches('\n'), true), "30");
assert_eq!(_part2(r#"
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
"#.trim_start_matches('\n'), true), "610");
assert_eq!(_part2(r#"
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
"#.trim_start_matches('\n'), true), "410");
}
