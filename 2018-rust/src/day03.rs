use regex::Regex;

use std::collections::HashSet;
use std::error::Error;

#[derive(Debug)]
pub struct Claim {
    num: i32,
    x: usize,
    y: usize,
    w: usize,
    h: usize,
}

impl Claim {
    fn right_x(&self) -> usize {
        self.x + self.w
    }

    fn bottom_y(&self) -> usize {
        self.y + self.h
    }
}

impl std::str::FromStr for Claim {
    type Err = Box<dyn Error>;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"^#(?P<num>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)$").unwrap();
        }
        
        let caps = RE.captures(s).ok_or(Box::<dyn Error>::from("invalid claim string"))?;

        Ok(Claim {
            num: caps.name("num").unwrap().as_str().parse()?,
            x: caps.name("x").unwrap().as_str().parse()?,
            y: caps.name("y").unwrap().as_str().parse()?,
            w: caps.name("w").unwrap().as_str().parse()?,
            h: caps.name("h").unwrap().as_str().parse()?,
        })
    }
}


pub fn parse_input(inp: &str) -> Vec<Claim> {
    inp.lines()
        .map(|line| line.parse().unwrap())
        .collect()
}

#[derive(PartialEq, Debug, Clone, Copy)]
enum GridClaim {
    Unclaimed,
    Claimed(i32),
    Overlap,
}

impl GridClaim {
    fn claim(&mut self, num: i32) {
        *self = match *self {
            GridClaim::Unclaimed => GridClaim::Claimed(num),
            _ => GridClaim::Overlap,
        }
    }
}

#[aoc(day03, part1)]
pub fn part1(inp: &str) -> String {
    let claims = parse_input(inp);

    let grid_width = claims.iter().map(|c| c.right_x()).max().unwrap();
    let grid_height = claims.iter().map(|c| c.bottom_y()).max().unwrap();

    let mut grid: Vec<Vec<GridClaim>> = vec![vec![GridClaim::Unclaimed; grid_height as usize]; grid_width as usize];

    for claim in claims {
        for x_coord in claim.x .. claim.right_x() {
            for y_coord in claim.y .. claim.bottom_y() {
                grid[x_coord][y_coord].claim(claim.num);
            }
        }
    }

    grid.into_iter()
        .map(|row| row.into_iter().filter(|x| *x == GridClaim::Overlap).count())
        .sum::<usize>()
        .to_string()
}

#[aoc(day03, part2)]
pub fn part2(inp: &str) -> String {
    let claims = parse_input(inp);

    let grid_width = claims.iter().map(|c| c.right_x()).max().unwrap();
    let grid_height = claims.iter().map(|c| c.bottom_y()).max().unwrap();

    let mut grid: Vec<Vec<GridClaim>> = vec![vec![GridClaim::Unclaimed; grid_height as usize]; grid_width as usize];
    let mut candidates = HashSet::with_capacity(claims.len());
    for claim in &claims {
        candidates.insert(claim.num);
    }

    for claim in &claims {
        for x_coord in claim.x .. claim.right_x() {
            for y_coord in claim.y .. claim.bottom_y() {
                match grid[x_coord][y_coord] {
                    GridClaim::Unclaimed => {},
                    GridClaim::Claimed(other) => {
                        candidates.remove(&other);
                        candidates.remove(&claim.num);
                    },
                    GridClaim::Overlap => {
                        candidates.remove(&claim.num);
                    },
                };
                grid[x_coord][y_coord].claim(claim.num);
            }
        }
    }

    assert_eq!(candidates.len(), 1);

    candidates.iter().next().unwrap().to_string()
}

#[test]
fn day03samples() {
assert_eq!(part1(r#"
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"#.trim_start_matches('\n')), "4");

assert_eq!(part2(r#"
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"#.trim_start_matches('\n')), "3");
}
