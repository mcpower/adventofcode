use mcpower_aoc::runner::run_samples_and_arg;

const DECRYPTION: i64 = 811589153;

fn solve(inp: &str, _is_sample: bool) -> (i64, i64) {
    let starting_nums: Vec<i64> = inp.lines().map(|x| x.parse().unwrap()).collect();
    let part1 = {
        // the ith number in this array is the index into starting_nums for that
        // position
        let mut perm: Vec<usize> = (0..starting_nums.len()).collect();
        // the ith number represents what index the ith number in starting_nums went
        // to
        let mut inv_perm: Vec<usize> = (0..starting_nums.len()).collect();
        for i in 0..starting_nums.len() {
            let perm_idx = inv_perm[i];
            let delta = starting_nums[i];
            let move_to_perm_idx =
                (perm_idx as i64 + delta).rem_euclid(starting_nums.len() as i64 - 1) as usize;
            {
                let removed = perm.remove(perm_idx);
                perm.insert(move_to_perm_idx, removed);
            }
            inv_perm = {
                let mut inv = vec![perm.len(); perm.len()];
                for (i, &x) in perm.iter().enumerate() {
                    inv[x] = i;
                }
                inv
            };
        }

        let zero_idx_in_starting_nums = starting_nums
            .iter()
            .position(|&num| num == 0)
            .expect("zero not in starting nums");
        let zero_idx_in_perm = inv_perm[zero_idx_in_starting_nums];

        [1000, 2000, 3000]
            .iter()
            .map(|i| starting_nums[perm[(zero_idx_in_perm + i) % perm.len()]])
            .sum::<i64>()
    };

    let part2 = {
        // the ith number in this array is the index into starting_nums for that
        // position
        let mut perm: Vec<usize> = (0..starting_nums.len()).collect();
        // the ith number represents what index the ith number in starting_nums went
        // to
        let mut inv_perm: Vec<usize> = (0..starting_nums.len()).collect();
        for _ in 0..10 {
            for i in 0..starting_nums.len() {
                let perm_idx = inv_perm[i];
                let delta = starting_nums[i] * DECRYPTION;
                let move_to_perm_idx =
                    (perm_idx as i64 + delta).rem_euclid(starting_nums.len() as i64 - 1) as usize;
                {
                    let removed = perm.remove(perm_idx);
                    perm.insert(move_to_perm_idx, removed);
                }
                inv_perm = {
                    let mut inv = vec![perm.len(); perm.len()];
                    for (i, &x) in perm.iter().enumerate() {
                        inv[x] = i;
                    }
                    inv
                };
            }
        }

        let zero_idx_in_starting_nums = starting_nums
            .iter()
            .position(|&num| num == 0)
            .expect("zero not in starting nums");
        let zero_idx_in_perm = inv_perm[zero_idx_in_starting_nums];
        DECRYPTION
            * [1000, 2000, 3000]
                .iter()
                .map(|i| starting_nums[perm[(zero_idx_in_perm + i) % perm.len()]])
                .sum::<i64>()
    };

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
