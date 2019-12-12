use std::collections::{HashSet, HashMap};

type Point = (i64, i64, i64);
fn add((a, b, c): Point, (x, y, z): Point) -> Point {
    (a+x, b+y, c+z)
}

fn neg((a, b, c): Point) -> Point {
    (-a, -b, -c)
}

fn sub(p: Point, v: Point) -> Point {
    add(p, neg(v))
}

fn sign(i: i64) -> i64 {
    if i > 0 {
        1
    } else if i == 0 {
        0
    } else {
        -1
    }
}

#[aoc(day12, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, sample: bool) -> String {
    let steps = if sample {100} else {1000};


    let mut points: Vec<(Point, Point)> = inp
        .lines()
        .map(|line| {
            if let [x, y, z] = line.split(", ").collect::<Vec<_>>().as_slice() {
                let x: i64 = x[3..].parse().unwrap();
                let y: i64 = y[2..].parse().unwrap();
                let z: i64 = z[2..(z.len() - 1)].parse().unwrap();
                ((x, y, z), (0, 0, 0))
            } else {
                panic!();
            }
        })
        .collect();

    for _ in 0..steps {
        // gravity
        for i in 0..points.len() {
            for j in i+1..points.len() {
                let (dx, dy, dz) = sub(points[i].0, points[j].0);
                let d = (sign(dx), sign(dy), sign(dz));
                points[i].1 = add(points[i].1, neg(d));
                points[j].1 = add(points[j].1, (d));
            }
        }
//        dbg!(&points);
        // velocity
        for i in 0..points.len() {
            points[i].0 = add(points[i].0, points[i].1);
        }
    }

    let out = points.iter().map(|((x, y, z), (dx, dy, dz))| (x.abs() + y.abs() + z.abs()) * (dx.abs() + dy.abs() + dz.abs())).sum::<i64>();

    out.to_string()
}

// (offset, cycle length)
fn simulate_axes(v: Vec<i64>) -> (usize, usize) {
    let mut cur: Vec<_> = v.iter().map(|p| (*p, 0)).collect();
    let mut s = HashMap::new();
    s.insert(cur.clone(), s.len());

    loop {
        for i in 0..cur.len() {
            for j in i+1..cur.len() {
                let d = sign(cur[i].0 - cur[j].0);
                cur[i].1 -= d;
                cur[j].1 += d;
            }
        }
//        dbg!(&points);
        // velocity
        for i in 0..cur.len() {
            let (p, v) = cur[i];
            cur[i].0 += cur[i].1;
        }

        if s.contains_key(&cur) {
            let first_occurrence = *s.get(&cur).unwrap();
            let last_occurrence = s.len();
            return (first_occurrence, last_occurrence - first_occurrence);
        } else {
            s.insert(cur.clone(), s.len());
        }
    }
}

#[aoc(day12, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}


fn gcd(mut m: usize, mut n: usize) -> usize {
    while m != 0 {
        let old_m = m;
        m = n % m;
        n = old_m;
    }
    n
}

fn lcm(m: usize, n: usize) -> usize {
    m * (n / gcd(m, n))
}

fn _part2(inp: &str, sample: bool) -> String {
    let steps = if sample {100} else {1000};


    let mut points: Vec<Point> = inp
        .lines()
        .map(|line| {
            if let [x, y, z] = line.split(", ").collect::<Vec<_>>().as_slice() {
                let x: i64 = x[3..].parse().unwrap();
                let y: i64 = y[2..].parse().unwrap();
                let z: i64 = z[2..(z.len() - 1)].parse().unwrap();
                (x, y, z)
            } else {
                panic!();
            }
        })
        .collect();

    let x = simulate_axes(points.iter().map(|(x, y, z)| x).cloned().collect());
    let y = simulate_axes(points.iter().map(|(x, y, z)| y).cloned().collect());
    let z = simulate_axes(points.iter().map(|(x, y, z)| z).cloned().collect());

    dbg!(x,y,z);

    let cycle = lcm(lcm(x.1, y.1), z.1);

    let mut blah = vec![x.0 + cycle, y.0 + cycle, z.0 + cycle];
    blah.sort();
    let mut out = 0;
    let earliest = x.0.max(y.0.max(z.0));
    if blah[0] >= earliest {
        out = blah[0]
    } else if blah[1] >= earliest {
        out = blah[1]
    } else {
        out = blah[2];
    }


    out.to_string()
}

#[rustfmt::skip]
#[test]
fn day12samples() {
    assert_eq!(_part1(r#"
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"#.trim_matches('\n'), true), "1940");

    assert_eq!(_part2(r#"
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"#.trim_matches('\n'), true), "2772");

    assert_eq!(_part2(r#"
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"#.trim_matches('\n'), true), "4686774924");
}
