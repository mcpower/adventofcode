use mcpower_aoc::{runner::run_samples_and_arg, vector::Vec2};
use once_cell::sync::OnceCell;

// Treat Vec2s as a pair of:
// - row, where 0 is the top-most row which has a rock, 1 is the row "below"
//   that, and rocks spawn in with their lowest point at -4.
// - col, where 0 is the left-most column, and 6 is the right-most column.
const ROCK_BOTTOM_LEFT: Vec2 = Vec2(-4, 2);

fn rocks() -> &'static Vec<Vec<Vec2>> {
    static INSTANCE: OnceCell<Vec<Vec<Vec2>>> = OnceCell::new();
    INSTANCE.get_or_init(|| {
        r"
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"
        .trim()
        .split("\n\n")
        .map(|block| {
            let mut out: Vec<Vec2> = block
                .lines()
                .enumerate()
                .flat_map(|(row_index_from_top, row)| {
                    row.chars().enumerate().filter(|(_, c)| *c == '#').map(
                        move |(col_index_from_left, _)| {
                            Vec2(row_index_from_top as i64, col_index_from_left as i64)
                        },
                    )
                })
                .collect();
            let lowest_row = out
                .iter()
                .map(|Vec2(r, _)| *r)
                .max()
                .expect("rock had no blocks?");
            let row_adjust = ROCK_BOTTOM_LEFT.0 - lowest_row;
            let col_adjust = ROCK_BOTTOM_LEFT.1;
            for point in out.iter_mut() {
                point.0 += row_adjust;
                point.1 += col_adjust;
            }
            out
        })
        .collect()
    })
}

const BOARD_WIDTH: usize = 7;

fn solve(inp: &str, _is_sample: bool) -> (usize, i64) {
    let rocks = rocks();
    let deltas = inp
        .trim()
        .chars()
        .map(|c| {
            Vec2(
                0,
                match c {
                    '<' => -1,
                    '>' => 1,
                    _ => unreachable!("inp char wasn't <>: {}", c),
                },
            )
        })
        .collect::<Vec<_>>();
    let part1 = {
        let mut board: Vec<[bool; BOARD_WIDTH]> = vec![];
        let mut cur_rock_i: usize = 0;
        let mut cur_rock = rocks[cur_rock_i % rocks.len()].clone();
        for delta in deltas.iter().cycle() {
            if cur_rock_i == 2022 {
                break;
            }
            // left/right
            let new_rock = cur_rock.iter().map(|pos| *pos + *delta).collect::<Vec<_>>();
            if new_rock.iter().all(|Vec2(row, col)| {
                let row = *row;
                let col = *col;
                // "is good
                if !(0 <= col && col < BOARD_WIDTH as i64) {
                    return false;
                }
                if row >= 0 {
                    let row = row as usize;
                    if row > board.len() {
                        // went beneath the board
                        return false;
                    }
                    if board[board.len() - 1 - row][col as usize] {
                        // collided into something
                        return false;
                    }
                }
                true
            }) {
                cur_rock = new_rock;
            }

            let new_rock = cur_rock
                .iter()
                .map(|pos| *pos + Vec2(1, 0))
                .collect::<Vec<_>>();
            if new_rock.iter().all(|Vec2(row, col)| {
                let row = *row;
                let col = *col;
                // "is good
                if !(0 <= col && col < BOARD_WIDTH as i64) {
                    return false;
                }
                if row >= 0 {
                    let row = row as usize;
                    if row >= board.len() {
                        // went beneath the board
                        return false;
                    }
                    if board[board.len() - 1 - row][col as usize] {
                        // collided into something
                        return false;
                    }
                }
                true
            }) {
                cur_rock = new_rock;
            } else {
                // commit
                let zero_board_i = board.len() as i64 - 1;
                for Vec2(row, col) in cur_rock {
                    let board_i = usize::try_from(zero_board_i - row)
                        .expect("attempted to commit to negative board row");
                    if board_i >= board.len() {
                        board.resize(board_i + 1, [false; 7]);
                    }
                    board[board_i][col as usize] = true;
                }
                cur_rock_i += 1;
                cur_rock = rocks[cur_rock_i % rocks.len()].clone();
            }
        }
        board.len()
    };
    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"];
