use std::collections::{HashSet, HashMap};
#[aoc(day03, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let wires: Vec<Vec<&str>> = inp.trim().lines().map(|s| s.split(',').collect()).collect();
    let mut seens = vec![];
    for dirs  in wires {
        let mut cur = (0, 0);
        let mut seen = HashSet::new();
        seen.insert(cur);
        for direction in dirs {
            let mut way = (0, 0);
            match direction.chars().nth(0) {
                Some('R') => way.1 += 1,
                Some('L') => way.1 -= 1,
                Some('U') => way.0 -= 1,
                Some('D') => way.0 += 1,
                _ => break,
            }
            // dbg!(&direction);
            let num: u64 = direction.chars().skip(1).collect::<String>().parse().unwrap();
            for i in 0..num {
                cur.0 += way.0;
                cur.1 += way.1;
    
                seen.insert(cur);
            }
        }
        seens.push(seen);
    }
    
    let mut s = seens[0].intersection(&seens[1]);

    s.into_iter()
        .filter(|&&q| q != (0, 0))
        .map(|(a, b)| i64::abs(a.clone()) + i64::abs(b.clone()))
        .min()
        .unwrap()
        .to_string()
}

#[aoc(day03, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let wires: Vec<Vec<&str>> = inp.trim().lines().map(|s| s.split(',').collect()).collect();
    let mut seens = vec![];
    for dirs  in wires {
        let mut cur = (0, 0);
        let mut dist = 0i64;
        let mut seen = HashMap::new();
        seen.insert(cur, dist);
        for direction in dirs {
            let mut way = (0, 0);
            match direction.chars().nth(0) {
                Some('R') => way.1 += 1,
                Some('L') => way.1 -= 1,
                Some('U') => way.0 -= 1,
                Some('D') => way.0 += 1,
                _ => break,
            }
            // dbg!(&direction);
            let num: u64 = direction.chars().skip(1).collect::<String>().parse().unwrap();
            for i in 0..num {
                cur.0 += way.0;
                cur.1 += way.1;
                dist += 1;
    
                seen.insert(cur, dist);
            }
        }
        seens.push(seen);
    }
    
    let first: HashSet<(i64, i64)> = seens[0].keys().map(|q| q.clone()).collect::<HashSet<_>>();
    let second: HashSet<(i64, i64)> = seens[1].keys().map(|q| q.clone()).collect::<HashSet<_>>();
    let mut s = first.intersection(&second);

    s.into_iter()
        .filter(|&&q| q != (0, 0))
        .map(|s| seens[0].get(s).unwrap() + seens[1].get(s).unwrap())
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

// assert_eq!(part2(r#"
// "#.trim_start_matches('\n'), true), "");
}
