#[aoc(day08, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

fn _part1(inp: &str, _sample: bool) -> String {
    let chars: Vec<_> = inp.chars().collect();
    let width = if _sample {
        3
    } else {
        25
    };
    let height = if _sample {
        2
    } else {
        6
    };
    let len = inp.len();

    let layers = len / (width * height);
    let mut fewest_digits = 100;
    let mut out = 0;
    for layer in 0..layers {
        let v = &chars[layer*width*height..(layer+1)*width*height];
        let zeroes = v.iter().filter(|x| **x == '0').count();
        if zeroes < fewest_digits {
            fewest_digits = zeroes;
            out = v.iter().filter(|x| **x == '1').count() * v.iter().filter(|x| **x == '2').count()
        }
    }

    out.to_string()
}

#[aoc(day08, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let chars: Vec<_> = inp.chars().collect();
    let width = if _sample {
        3
    } else {
        25
    };
    let height = if _sample {
        2
    } else {
        6
    };
    let len = inp.len();

    let get_layer = |i: usize| {
        let mut out = vec![];
        let layers = len / (width * height);
        for layer in 0..layers {
            out.push(chars.get(layer*width*height + i).unwrap());
        }
        out
    };

    let mut out = vec![];

    for i in 0..(width*height) {
        let v = get_layer(i);
        let q = v.iter().filter(|x| ***x != '2').next().unwrap();
        out.push(**q);
    }
    let mut output = String::new();
    output.push('\n');
    for row in 0..height {
        for col in 0..width {
            output.push(out[row*width + col]);
        }
        output.push('\n');
    }
    output = output.replace('0', ".").replace('1', "#");

    output
}

#[test]
fn day08samples() {
//assert_eq!(_part1(r#"
//"#.trim_matches('\n'), true), "");

//assert_eq!(_part2(r#"
//"#.trim_matches('\n'), true), "");
}
