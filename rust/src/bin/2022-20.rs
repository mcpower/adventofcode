use mcpower_aoc::runner::run_samples_and_arg;

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let starting_nums: Vec<i64> = inp.lines().map(|x| x.parse().unwrap()).collect();
    // the ith number in this array is the index into starting_nums for that
    // position, after one permutation
    let perm: Vec<usize> = {
        let mut perm: Vec<usize> = (0..starting_nums.len()).collect();
        let mut has_moved = vec![false; starting_nums.len()];
        let mut cur_pointer = 0;
        for _ in 0..starting_nums.len() {
            while has_moved[cur_pointer] {
                cur_pointer += 1;
            }
            let starting_idx = perm[cur_pointer];
            let delta = starting_nums[starting_idx];
            let move_to =
                (cur_pointer as i64 + delta).rem_euclid(starting_nums.len() as i64 - 1) as usize;
            {
                let removed = perm.remove(cur_pointer);
                perm.insert(move_to, removed);
            }
            {
                has_moved.remove(cur_pointer);
                has_moved.insert(move_to, true);
            }
        }
        perm
    };
    // the ith number represents what index the ith number in starting_nums went
    // to
    let inv_perm: Vec<usize> = {
        let mut inv = vec![perm.len(); perm.len()];
        for (i, &x) in perm.iter().enumerate() {
            inv[x] = i;
        }
        inv
    };

    let part1 = {
        let zero_idx_in_starting_nums = starting_nums
            .iter()
            .position(|&num| num == 0)
            .expect("zero not in starting nums");
        let zero_idx_in_perm = dbg!(inv_perm[zero_idx_in_starting_nums]);
        [1000, 2000, 3000]
            .iter()
            .map(|i| starting_nums[perm[(zero_idx_in_perm + i) % perm.len()]])
            .sum()
    };

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
1
2
-3
3
-2
0
4
"];
