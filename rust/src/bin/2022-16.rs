// Dijkstra over interesting nodes using Floyd-Warshall. Takes 2 seconds for
// part 2 on my input in release mode.

use std::{
    cmp::Reverse,
    collections::{BTreeSet, BinaryHeap, HashMap},
};

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;
use regex::Regex;

fn solve(inp: &str, _is_sample: bool) -> (u64, u64) {
    // Input 1: Labels
    let re =
        Regex::new(r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$").unwrap();
    let valves: HashMap<&str, (u64, Vec<&str>)> = inp
        .lines()
        .map(|line| {
            let m = re.captures(line).expect("line didn't match regex");
            let (valve, rate, tunnels) = m
                .iter()
                .skip(1)
                .map(|x| x.expect("didn't get match?").as_str())
                .collect_tuple()
                .expect("didn't get 3 things?");
            (
                valve,
                (
                    rate.parse().expect("rate wasn't int"),
                    tunnels.split(", ").collect(),
                ),
            )
        })
        .collect();

    // Input 2: Indices (u8s)
    let valve_to_i: HashMap<&str, u8> = valves
        .keys()
        .cloned()
        .enumerate()
        .map(|(i, k)| (k, i.try_into().expect("index can't fit in u8")))
        .collect();
    let valves = valves
        .into_iter()
        .map(|(k, (flow, tunnels))| {
            (
                *valve_to_i.get(k).unwrap(),
                (
                    flow,
                    tunnels
                        .iter()
                        .map(|tunnel| *valve_to_i.get(tunnel).unwrap())
                        .collect::<Vec<_>>(),
                ),
            )
        })
        .sorted_by_key(|(i, _)| *i)
        .map(|(_i, rest)| rest)
        .collect::<Vec<_>>();
    let start_i = *valve_to_i.get("AA").expect("no AA");

    // Input 3: APSP for all nodes
    let flows = valves.iter().map(|(flow, _)| *flow).collect::<Vec<_>>();
    let n = valves.len();
    let mut dist_matrix = vec![vec![n * 2; n]; n];
    #[allow(clippy::needless_range_loop)]
    for v in 0..n {
        dist_matrix[v][v] = 0;
    }
    for (i, (_, adj)) in valves.iter().enumerate() {
        for j in adj {
            dist_matrix[i][usize::from(*j)] = 1;
        }
    }
    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                if dist_matrix[i][j] > dist_matrix[i][k] + dist_matrix[k][j] {
                    dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j];
                }
            }
        }
    }

    // Input 4: APSP for interesting nodes
    let mut interesting_nodes = BTreeSet::<u8>::new();
    interesting_nodes.insert(start_i);
    for (i, flow) in flows.iter().enumerate() {
        if *flow > 0 {
            interesting_nodes.insert(i.try_into().expect("index can't fit in u8"));
        }
    }
    let flows = interesting_nodes
        .iter()
        .map(|i| flows[usize::from(*i)])
        .collect::<Vec<_>>();
    let dist_matrix: Vec<Vec<_>> = interesting_nodes
        .iter()
        .map(|i| {
            let row = &dist_matrix[usize::from(*i)];
            interesting_nodes
                .iter()
                .map(|j| row[usize::from(*j)])
                .collect()
        })
        .collect();
    let start_i = u8::try_from(
        interesting_nodes
            .iter()
            .find_position(|&&i| i == start_i)
            .unwrap()
            .0,
    )
    .expect("index can't fit in u8");

    assert_eq!(flows[usize::from(start_i)], 0, "start flow wasn't 0");

    let pressure_per_time = flows.iter().sum::<u64>();
    let mut valves_open_to_pressure_lost = HashMap::<u64, u64>::new();
    valves_open_to_pressure_lost.insert(0, pressure_per_time);

    // (time left, valves_open, cur_node): pressure lost
    type SearchNodePart1 = (u8, u64, u8);

    let part1 = {
        let mut pq = BinaryHeap::<Reverse<(u64, SearchNodePart1)>>::new();
        let mut best = HashMap::<SearchNodePart1, u64>::new();
        let start_node: SearchNodePart1 = (30, 0, start_i);
        best.insert(start_node, 0);
        pq.push(Reverse((0, start_node)));

        let best_dist = loop {
            let Some(Reverse((dist, search_node @ (time_left, valves_open, node)))) = pq.pop() else { unreachable!("didn't reach end") };
            {
                let best_dist = *best
                    .get(&search_node)
                    .expect("popped off node not in best??");
                if best_dist < dist {
                    continue;
                }
                assert_eq!(best_dist, dist, "popped off dist isn't best dist??");
            }
            if time_left == 0 {
                break dist;
            }
            let pressure_lost = *valves_open_to_pressure_lost.get(&valves_open).unwrap();
            let adj = {
                let mut iter = dist_matrix[usize::from(node)]
                    .iter()
                    .enumerate()
                    .filter_map(|(i, &dist)| {
                        if dist == 0 || i == usize::from(start_i) || (valves_open >> i) & 1 == 1 {
                            return None;
                        }
                        let cur_rate = flows[i];
                        let new_valves_open = valves_open | (1 << i);
                        valves_open_to_pressure_lost
                            .entry(new_valves_open)
                            .or_insert_with(|| pressure_lost - cur_rate);
                        Some((
                            time_left.checked_sub(u8::try_from(dist + 1).ok()?)?,
                            new_valves_open,
                            i.try_into().expect("index can't fit in u8"),
                        ))
                    });
                let iter_next = iter.next();
                std::iter::once(iter_next.unwrap_or((0, 0, 0))).chain(iter)
            };
            for other_node @ (new_time_left, _, _) in adj {
                let new_dist = dist + pressure_lost * u64::from(time_left - new_time_left);
                if let Some(cur_best) = best.get(&other_node) {
                    if *cur_best <= new_dist {
                        continue;
                    }
                }
                best.insert(other_node, new_dist);
                pq.push(Reverse((new_dist, other_node)));
            }
        };

        30 * pressure_per_time - best_dist
    };

    // (time left, valves_open, node_1, node_2, delta): pressure lost
    // delta -ve = node_1 has more time
    // delta +ve = node_2 has more time
    type SearchNodePart2 = (u8, u64, u8, u8, i8);
    let part2 = {
        let mut pq = BinaryHeap::<Reverse<(u64, SearchNodePart2)>>::new();
        let mut best = HashMap::<SearchNodePart2, u64>::new();
        let start_node: SearchNodePart2 = (26, 0, start_i, start_i, 0);
        best.insert(start_node, 0);
        pq.push(Reverse((0, start_node)));

        let best_dist = loop {
            let Some(Reverse((dist, search_node @ (time_left, valves_open, node_1, node_2, delta)))) = pq.pop() else { unreachable!("didn't reach end") };
            {
                let best_dist = *best
                    .get(&search_node)
                    .expect("popped off node not in best??");
                if best_dist < dist {
                    continue;
                }
                assert_eq!(best_dist, dist, "popped off dist isn't best dist??");
            }
            if time_left == 0 {
                break dist;
            }
            let pressure_lost = *valves_open_to_pressure_lost.get(&valves_open).unwrap();
            for (i, flow) in flows.iter().enumerate() {
                if i == usize::from(start_i) || (valves_open >> i) & 1 == 1 {
                    continue;
                }
                let new_valves_open = valves_open | (1 << i);
                valves_open_to_pressure_lost
                    .entry(new_valves_open)
                    .or_insert_with(|| pressure_lost - flow);
            }
            let adj = {
                let iter_1 = dist_matrix[usize::from(node_1)]
                    .iter()
                    .enumerate()
                    .filter_map(|(i, &dist)| {
                        if dist == 0 || i == usize::from(start_i) || (valves_open >> i) & 1 == 1 {
                            return None;
                        }
                        let new_valves_open = valves_open | (1 << i);

                        // if we should've gone here earlier
                        let i = i.try_into().expect("index can't fit in u8");
                        if delta < 0 {
                            let time_spent = u8::try_from(dist + 1)
                                .ok()?
                                // this checked sub ensures that we never
                                // take a distance which exceeded our delta
                                .checked_sub(delta.unsigned_abs())?;
                            Some((
                                time_left.checked_sub(time_spent)?,
                                new_valves_open,
                                i,
                                node_2,
                                i8::try_from(time_spent).ok()?,
                            ))
                        } else {
                            Some((
                                time_left.checked_sub(u8::try_from(dist + 1).ok()?)?,
                                new_valves_open,
                                i,
                                node_2,
                                // if delta + dist > 128, this is probably
                                // suboptimal anyway
                                delta.checked_add(i8::try_from(dist + 1).ok()?)?,
                            ))
                        }
                    });
                let iter_2 = dist_matrix[usize::from(node_2)]
                    .iter()
                    .enumerate()
                    .filter_map(|(i, &dist)| {
                        if dist == 0 || i == usize::from(start_i) || (valves_open >> i) & 1 == 1 {
                            return None;
                        }
                        let new_valves_open = valves_open | (1 << i);

                        // if we should've gone here earlier
                        let i = i.try_into().expect("index can't fit in u8");
                        if delta > 0 {
                            let time_spent = u8::try_from(dist + 1)
                                .ok()?
                                // this checked sub ensures that we never
                                // take a distance which exceeded our delta
                                .checked_sub(delta.unsigned_abs())?;
                            Some((
                                time_left.checked_sub(time_spent)?,
                                new_valves_open,
                                node_1,
                                i,
                                i8::try_from(-i16::from(time_spent)).ok()?,
                            ))
                        } else {
                            Some((
                                time_left.checked_sub(u8::try_from(dist + 1).ok()?)?,
                                new_valves_open,
                                node_1,
                                i,
                                // if delta + dist > 128, this is probably
                                // suboptimal anyway
                                delta.checked_sub(i8::try_from(dist + 1).ok()?)?,
                            ))
                        }
                    });
                let mut combined = iter_1.chain(iter_2);

                let combined_next = combined.next();
                std::iter::once(combined_next.unwrap_or((0, 0, 0, 0, 0))).chain(combined)
            };
            for other_node @ (new_time_left, _, _, _, _) in adj {
                let new_dist = dist + pressure_lost * u64::from(time_left - new_time_left);
                if let Some(cur_best) = best.get(&other_node) {
                    if *cur_best <= new_dist {
                        continue;
                    }
                }
                best.insert(other_node, new_dist);
                pq.push(Reverse((new_dist, other_node)));
            }
        };

        26 * pressure_per_time - best_dist
    };

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"];
