type Point = (i16, i16, i16);
fn add((a, b, c): Point, (x, y, z): Point) -> Point {
    (a + x, b + y, c + z)
}

fn neg((a, b, c): Point) -> Point {
    (-a, -b, -c)
}

fn sub(p: Point, v: Point) -> Point {
    add(p, neg(v))
}

fn sign(i: i16) -> i16 {
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
    let steps = if sample { 100 } else { 1000 };

    let mut points: Vec<(Point, Point)> = inp
        .lines()
        .map(|line| {
            if let [x, y, z] = line.split(", ").collect::<Vec<_>>().as_slice() {
                let x: i16 = x[3..].parse().unwrap();
                let y: i16 = y[2..].parse().unwrap();
                let z: i16 = z[2..(z.len() - 1)].parse().unwrap();
                ((x, y, z), (0, 0, 0))
            } else {
                panic!();
            }
        })
        .collect();

    for _ in 0..steps {
        // gravity
        for i in 0..points.len() {
            for j in i + 1..points.len() {
                let (dx, dy, dz) = sub(points[i].0, points[j].0);
                let d = (sign(dx), sign(dy), sign(dz));
                points[i].1 = add(points[i].1, neg(d));
                points[j].1 = add(points[j].1, d);
            }
        }
        // velocity
        for (pos, vel) in &mut points {
            *pos = add(*pos, *vel);
        }
    }

    let out = points
        .iter()
        .map(|((x, y, z), (dx, dy, dz))| {
            (x.abs() + y.abs() + z.abs()) * (dx.abs() + dy.abs() + dz.abs())
        })
        .sum::<i16>();

    out.to_string()
}

fn simulate_axes(v: Vec<i16>) -> usize {
    // can always "undo" a state so every state has one parent
    // therefore it must always cycle to the start
    let orig: [i16;8] = [v[0],v[1],v[2],v[3],0,0,0,0];
    let mut ps = orig;
    let mut i = 0usize;

    loop {
        // gravity
        for i in 0..4 {
            for j in 0..4 {
                use std::cmp::Ordering;
                ps[i+4] += match ps[i].cmp(&ps[j]) {
                    Ordering::Less => 1,
                    Ordering::Equal => 0,
                    Ordering::Greater => -1
                };
            }
        }
        // velocity
        for i in 0..4 {
            ps[i] += ps[i+4];
        }
        i += 1;

        if ps == orig {
            return i;
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

fn _part2(inp: &str, _sample: bool) -> String {
    let points: Vec<Point> = inp
        .lines()
        .map(|line| {
            if let [x, y, z] = line.split(", ").collect::<Vec<_>>().as_slice() {
                let x: i16 = x[3..].parse().unwrap();
                let y: i16 = y[2..].parse().unwrap();
                let z: i16 = z[2..(z.len() - 1)].parse().unwrap();
                (x, y, z)
            } else {
                panic!();
            }
        })
        .collect();

    let x = simulate_axes(points.iter().map(|p| p.0).collect());
    let y = simulate_axes(points.iter().map(|p| p.1).collect());
    let z = simulate_axes(points.iter().map(|p| p.2).collect());

    lcm(lcm(x, y), z).to_string()
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
