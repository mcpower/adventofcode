#[aoc(day08, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let chars: Vec<_> = inp.chars().collect();
    let width = if _sample { 3 } else { 25 };
    let height = if _sample { 2 } else { 6 };

    let mut out = (100, 0);
    for layer in chars.chunks(width * height) {
        let get_num = |c| layer.iter().filter(|&&x| x == c).count();
        let zeroes = get_num('0');
        let ones = get_num('1');
        let twos = get_num('2');
        out = out.min((zeroes, ones * twos));
    }

    out.1.to_string()
}

#[aoc(day08, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let chars: Vec<_> = inp.chars().collect();
    let width = if _sample { 2 } else { 25 };
    let height = if _sample { 2 } else { 6 };
    let layers: Vec<_> = chars.chunks(width * height).collect();

    let mut output: String = String::new();

    for row in 0..height {
        output.push('\n');
        for col in 0..width {
            let pixel = layers
                .iter()
                .map(|layer| layer[row * width + col])
                .find(|&c| c != '2')
                .unwrap();
            let ascii = if pixel == '1' { '#' } else { '.' };
            output.push(ascii);
        }
    }

    output
}

#[test]
fn day08samples() {
    assert_eq!(_part1("123456789012", true), "1");

    assert_eq!(_part2("0222112222120000", true).trim(), ".#\n#.");
}
