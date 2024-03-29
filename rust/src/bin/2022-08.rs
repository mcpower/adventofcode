use std::{env, fs};

fn solve(inp: &str) -> (i64, i64) {
    let grid = inp
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| c as i64 - '0' as i64)
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    let rows = grid.len();
    let cols = grid.first().expect("empty grid?").len();
    let mut visible: Vec<Vec<bool>> = grid.iter().map(|row| vec![false; row.len()]).collect();

    for (i, row) in grid.iter().enumerate() {
        // front to back
        let mut highest = -1;
        for (j, height) in row.iter().enumerate() {
            if *height > highest {
                highest = *height;
                visible[i][j] = true;
            }
        }
        let mut highest = -1;
        for (j, height) in row.iter().enumerate().rev() {
            if *height > highest {
                highest = *height;
                visible[i][j] = true;
            }
        }
    }
    for j in 0..cols {
        let mut highest = -1;
        for i in 0..rows {
            let height = grid[i][j];
            if height > highest {
                highest = height;
                visible[i][j] = true;
            }
        }
        let mut highest = -1;
        for i in (0..rows).rev() {
            let height = grid[i][j];
            if height > highest {
                highest = height;
                visible[i][j] = true;
            }
        }
    }
    let part1 = visible
        .iter()
        .map(|row| row.iter().map(|x| -> i64 { (*x).into() }).sum::<i64>())
        .sum();

    let mut part2 = 0;
    for row in 0..rows {
        for col in 0..cols {
            let cur_height = grid[row][col];
            let mut right = 0;
            for other_height in grid[row].iter().skip(col + 1) {
                right += 1;
                if *other_height >= cur_height {
                    break;
                }
            }
            let mut left = 0;
            for other_height in grid[row].iter().take(col).rev() {
                left += 1;
                if *other_height >= cur_height {
                    break;
                }
            }
            let mut down = 0;
            for other_height in grid.iter().skip(row + 1).map(|row| row[col]) {
                down += 1;
                if other_height >= cur_height {
                    break;
                }
            }
            let mut up = 0;
            for other_height in grid.iter().take(row).rev().map(|row| row[col]) {
                up += 1;
                if other_height >= cur_height {
                    break;
                }
            }
            part2 = part2.max(up * down * left * right);
        }
    }

    (part1, part2)
}

fn main() {
    dbg!(solve(
        r"30373
25512
65332
33549
35390"
    ));
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (part1, part2) = solve(&contents);
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
