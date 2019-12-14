use std::collections::HashMap;

#[aoc(day14, part1)]
pub fn part1(inp: &str) -> String {
    _part1(inp, false)
}

type Ingredient = (usize, String);

fn get(x: &str) -> Ingredient {
    let mut i = x.split(' ');
    let num = i.next().unwrap().parse::<usize>().unwrap();
    let ing = i.next().unwrap().to_string();
    (num, ing)
}

fn topsort(recipes: &HashMap<String, (usize, Vec<Ingredient>)>) -> Vec<String> {
    let mut out = vec![];

    let mut inedges: HashMap<String, usize> = HashMap::new();

    inedges.insert("ORE".to_string(), 0);

    for (key, value) in recipes.iter() {
        inedges.insert(key.clone(), value.1.len());
    }

    let mut outs: HashMap<String, Vec<String>> = HashMap::new();
    for (key, value) in recipes.iter() {
        for (_, other) in &value.1 {
            outs.entry(other.clone()).or_insert_with(Vec::new).push(key.clone());
        }
    }

    while !inedges.is_empty() {
        let (name, dependent) = inedges.clone().into_iter().min_by_key(|pair| pair.1).unwrap();
        if dependent != 0 {
            dbg!(name, dependent);
            panic!();
        }
        out.push(name.clone());
        if outs.contains_key(&name) {
            for other in outs.get(&name).unwrap() {
                *inedges.get_mut(other).unwrap() -= 1;
            }
        }
        inedges.remove(&name);

    }

    out
}

fn _part1(inp: &str, _sample: bool) -> String {
    let mut recipes: HashMap<String, (usize, Vec<Ingredient>)> = HashMap::new();
    for line in inp.lines() {
        let sides: Vec<_> = line.split(" => ").collect();
        if let [left, right] = sides.as_slice() {
            let left_ing = get(right);
            let right_ings: Vec<_> = left.split(", ").map(get).collect();
            recipes.insert(left_ing.1, (left_ing.0, right_ings));
        } else {
            panic!();
        }
    }

    let sorted = topsort(&recipes);

    let mut needed: HashMap<String, usize> = HashMap::new();

    needed.insert("FUEL".to_string(), 1);
    let mut out = 0;

    for ing in sorted.iter().rev() {
        let &amount = needed.get(ing).unwrap();
        if ing == "ORE" {
            out = amount;
        } else {
            let blah = recipes.get(ing).unwrap();
            // how many recipes
            let how_many = (amount + blah.0 - 1) / blah.0;
            for (num, other) in &blah.1 {
                *needed.entry(other.clone()).or_insert(0) += num * how_many;
            }
        }
    }


    out.to_string()
}

#[aoc(day14, part2)]
pub fn part2(inp: &str) -> String {
    _part2(inp, false)
}

fn _part2(inp: &str, _sample: bool) -> String {
    let mut recipes: HashMap<String, (usize, Vec<Ingredient>)> = HashMap::new();
    for line in inp.lines() {
        let sides: Vec<_> = line.split(" => ").collect();
        if let [left, right] = sides.as_slice() {
            let left_ing = get(right);
            let right_ings: Vec<_> = left.split(", ").map(get).collect();
            recipes.insert(left_ing.1, (left_ing.0, right_ings));
        } else {
            panic!();
        }
    }

    let sorted = topsort(&recipes);

    let fuel_to_ore = |fuel: usize| -> usize {
        let mut needed: HashMap<String, usize> = HashMap::new();
        needed.insert("FUEL".to_string(), fuel);
        let mut out = 0;

        for ing in sorted.iter().rev() {
            let &amount = needed.get(ing).unwrap();
            if ing == "ORE" {
                out = amount;
            } else {
                let blah = recipes.get(ing).unwrap();
                // how many recipes
                let how_many = (amount + blah.0 - 1) / blah.0;
                for (num, other) in &blah.1 {
                    *needed.entry(other.clone()).or_insert(0) += num * how_many;
                }
            }
        }
        out
    };

    let mut lo = 1usize;
    let mut hi = 1000000000000usize;

    let mut best_so_far = hi;

    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        if fuel_to_ore(mid) <= 1000000000000usize {
            // good
            best_so_far = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }


    best_so_far.to_string()
}

#[rustfmt::skip]
#[test]
fn day14samples() {
assert_eq!(_part1(r#"
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"#.trim_matches('\n'), true), "31");
    assert_eq!(_part1(r#"
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"#.trim_matches('\n'), true), "165");
    assert_eq!(_part1(r#"
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"#.trim_matches('\n'), true), "2210736");

    assert_eq!(_part2(r#"
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"#.trim_matches('\n'), true), "460664");

//assert_eq!(_part2(r#"
//"#.trim_matches('\n'), true), "");
}
