#[aoc(day08, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, sample: bool) -> String {
    let chars: Vec<_> = inp.chars().collect();
    let cols = if sample { 3 } else { 25 };
    let rows = if sample { 2 } else { 6 };

    chars
        .chunks(cols * rows)
        .map(|layer| {
            let num = |c| layer.iter().filter(|&&x| x == c).count();
            (num('0'), num('1') * num('2'))
        })
        .min()
        .unwrap()
        .1
        .to_string()
}

#[aoc(day08, part2)]
pub fn part2(inp: &str) -> String {
    // need extra new line because cargo-aoc displays the string inline with the day/part
    "\n".to_string() + _part2(inp, false).as_ref()
}

fn _part2(inp: &str, sample: bool) -> String {
    let chars: Vec<_> = inp.chars().collect();
    let cols = if sample { 2 } else { 25 };
    let rows = if sample { 2 } else { 6 };
    let layers = chars.chunks(cols * rows);

    (0..rows)
        .map(|row| {
            (0..cols)
                .map(|col| {
                    layers
                        .clone()
                        .map(|layer| layer[row * cols + col])
                        .find(|&c| c != '2')
                        .map(|pixel| if pixel == '1' { '#' } else { '.' })
                        .unwrap_or('?')
                })
                .collect::<String>()
        })
        .collect::<Vec<_>>()
        .join("\n")
}

#[test]
fn day08samples() {
    assert_eq!(_part1("123456789012", true), "1");

    assert_eq!(_part2("0222112222120000", true).trim(), ".#\n#.");
}
