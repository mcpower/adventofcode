#[allow(clippy::many_single_char_names)]
fn farey(n: usize) -> Vec<(usize, usize)> {
    let (mut a, mut b, mut c, mut d) = (0, 1, 1, n);
    let mut out = vec![];
    out.push((a, b));

    while c < n {
        let k = (n + b) / d;

        let (newa, newb, newc, newd) = (c, d, k * c - a, k * d - b);
        a = newa;
        b = newb;
        c = newc;
        d = newd;
        out.push((a, b));
    }
    out
}

fn gcd(mut m: i64, mut n: i64) -> i64 {
    m = m.abs();
    n = n.abs();
    while m != 0 {
        let old_m = m;
        m = n % m;
        n = old_m;
    }
    n.abs()
}

#[aoc(day10, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let grid: Vec<Vec<bool>> = inp
        .lines()
        .map(|line| line.chars().map(|c| c == '#').collect())
        .collect();

    let rows = grid.len();
    let cols = grid[0].len();

    let mut best = 0;
    for row in 0..rows {
        for col in 0..cols {
            if !grid[row][col] {
                continue;
            }
            let mut count = 0;
            for other_row in 0..rows {
                for other_col in 0..cols {
                    let drow = (other_row as i64) - (row as i64);
                    let dcol = (other_col as i64) - (col as i64);
                    // if (drow, dcol) = (0, 0) this should be false
                    if gcd(drow, dcol) != 1 {
                        continue;
                    }
                    let mut cur_row = other_row as i64;
                    let mut cur_col = other_col as i64;
                    while 0 <= cur_row
                        && cur_row < rows as i64
                        && 0 <= cur_col
                        && cur_col < cols as i64
                        {
                            if grid[cur_row as usize][cur_col as usize] {
                                count += 1;
                                break;
                            }
                            cur_row += drow;
                            cur_col += dcol;
                        }
                }
            }
            best = best.max(count);
        }
    }

    best.to_string()
}

#[aoc(day10, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let grid: Vec<Vec<bool>> = inp
        .lines()
        .map(|line| line.chars().map(|c| c == '#').collect())
        .collect();

    let rows = grid.len();
    let cols = grid[0].len();

    let mut best = (0usize, 0usize, 0usize);
    for row in 0..rows {
        for col in 0..cols {
            if !grid[row][col] {
                continue;
            }
            let mut count = 0;
            for other_row in 0..rows {
                for other_col in 0..cols {
                    let drow = (other_row as i64) - (row as i64);
                    let dcol = (other_col as i64) - (col as i64);
                    // if (drow, dcol) = (0, 0) this should be false
                    if gcd(drow, dcol) != 1 {
                        continue;
                    }
                    let mut cur_row = other_row as i64;
                    let mut cur_col = other_col as i64;
                    while 0 <= cur_row
                        && cur_row < rows as i64
                        && 0 <= cur_col
                        && cur_col < cols as i64
                    {
                        if grid[cur_row as usize][cur_col as usize] {
                            count += 1;
                            break;
                        }
                        cur_row += drow;
                        cur_col += dcol;
                    }
                }
            }
            best = best.max((count, row, col));
        }
    }

    let best_row = best.1 as i64;
    let best_col = best.2 as i64;

    // (0, 1) to (1, 0)
    let mut seq = farey(rows.max(cols) + 1);
    seq.extend(seq.clone().into_iter().rev().skip(1).map(|(x, y)| (y, x)));

    let mut wtf = vec![];

    wtf.extend(seq.iter().rev().map(|(x, y)| (-(*x as i64), (*y as i64))));
    wtf.pop();
    wtf.extend(seq.iter().map(|(x, y)| ((*x as i64), (*y as i64))));
    wtf.pop();
    wtf.extend(seq.iter().rev().map(|(x, y)| ((*x as i64), -(*y as i64))));
    wtf.pop();
    wtf.extend(seq.iter().map(|(x, y)| (-(*x as i64), -(*y as i64))));
    wtf.pop();

    let mut todo: Vec<Vec<i64>> = vec![];

    for (drow, dcol) in &wtf {
        let drow = *drow;
        let dcol = *dcol;
        let (mut cur_row, mut cur_col) = (best_row + drow, best_col + dcol);
        let mut i = 0;
        while 0 <= cur_row && cur_row < rows as i64 && 0 <= cur_col && cur_col < cols as i64 {
            if grid[cur_row as usize][cur_col as usize] {
                let out = cur_col * 100 + cur_row;
                if todo.len() <= i {
                    todo.push(vec![]);
                }
                todo[i].push(out);
                i += 1;
            }
            cur_row += drow;
            cur_col += dcol;
        }
    }

    todo.iter().flatten().take(200).last().unwrap().to_string()
}

#[test]
fn day10samples() {
    assert_eq!(_part1(r#"
.#..#
.....
#####
....#
...##
"#.trim_matches('\n'), true), "8");
    assert_eq!(_part1(r#"
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"#.trim_matches('\n'), true), "33");
    assert_eq!(_part1(r#"
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"#.trim_matches('\n'), true), "35");
    assert_eq!(_part1(r#"
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"#.trim_matches('\n'), true), "41");
    assert_eq!(_part1(r#"
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"#.trim_matches('\n'), true), "210");

    assert_eq!(_part2(r#"
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"#.trim_matches('\n'), true), "802");
}
