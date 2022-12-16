use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashMap},
};

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;
use regex::Regex;

fn solve(inp: &str, _is_sample: bool) -> (u64, u64) {
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
    let i_to_valve = valves
        .keys()
        .cloned()
        .enumerate()
        .map(|(i, k)| (i as u8, k))
        .collect::<HashMap<_, _>>();
    let valve_to_i = i_to_valve
        .iter()
        .map(|(i, k)| (*k, *i))
        .collect::<HashMap<_, _>>();

    let valves_better = valves
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

    let pressure_per_time = valves_better.iter().map(|(i, _)| *i).sum::<u64>();
    let mut valves_open_to_pressure_lost = HashMap::<u64, u64>::new();
    valves_open_to_pressure_lost.insert(0, pressure_per_time);

    // the better way of doing this is to only consider non-zero flow rate
    // valves, but whatever
    // (time left, valves_open, cur_node): pressure lost
    type SearchNodePart1 = (u8, u64, u8);

    let part1 = {
        let mut pq = BinaryHeap::<Reverse<(u64, SearchNodePart1)>>::new();
        let mut best = HashMap::<SearchNodePart1, u64>::new();
        let start_node: SearchNodePart1 = (30, 0, start_i);
        best.insert(start_node, 0);
        pq.push(Reverse((0, start_node)));

        let best_dist = loop {
            let Some(Reverse((dist, node @ (time_left, valves_open, cur_node)))) = pq.pop() else { unreachable!("didn't reach end") };
            {
                let best_dist = *best.get(&node).expect("popped off node not in best??");
                if best_dist < dist {
                    continue;
                }
                assert_eq!(best_dist, dist, "popped off dist isn't best dist??");
            }
            if node.0 == 0 {
                break dist;
            }
            let adj = {
                let pressure_lost = *valves_open_to_pressure_lost.get(&valves_open).unwrap();
                valves_better
                    .get(cur_node as usize)
                    .unwrap()
                    .1
                    .iter()
                    .map(move |other| ((time_left - 1, valves_open, *other), pressure_lost))
                    .chain(
                        ((valves_open >> cur_node) & 1 == 0)
                            .then(|| {
                                let cur_rate = valves_better[cur_node as usize].0;
                                if cur_rate == 0 {
                                    return None;
                                }
                                let new_valves_open = valves_open | (1 << cur_node);
                                valves_open_to_pressure_lost
                                    .entry(new_valves_open)
                                    .or_insert_with(|| pressure_lost - cur_rate);
                                Some(((time_left - 1, new_valves_open, cur_node), pressure_lost))
                            })
                            .flatten(),
                    )
            };
            for (other_node, weight) in adj {
                let new_dist = dist + weight;
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

    type SearchNodePart2 = (u8, u64, u8, u8);
    let part2 = {
        let mut pq = BinaryHeap::<Reverse<(u64, SearchNodePart2)>>::new();
        let mut best = HashMap::<SearchNodePart2, u64>::new();
        let start_node: SearchNodePart2 = (26, 0, start_i, start_i);
        best.insert(start_node, 0);
        pq.push(Reverse((0, start_node)));

        let best_dist = loop {
            let Some(Reverse((dist, node @ (time_left, valves_open, cur_node, cur_node_2)))) = pq.pop() else { unreachable!("didn't reach end") };
            {
                let best_dist = *best.get(&node).expect("popped off node not in best??");
                if best_dist < dist {
                    continue;
                }
                assert_eq!(best_dist, dist, "popped off dist isn't best dist??");
            }
            if node.0 == 0 {
                break dist;
            }
            let pressure_lost = *valves_open_to_pressure_lost.get(&valves_open).unwrap();
            let adj = {
                valves_better
                    .get(cur_node as usize)
                    .unwrap()
                    .1
                    .iter()
                    .map(move |other| (0, *other))
                    .chain(
                        ((valves_open >> cur_node) & 1 == 0)
                            .then(|| {
                                let cur_rate = valves_better[cur_node as usize].0;
                                if cur_rate == 0 {
                                    return None;
                                }
                                let bit = 1 << cur_node;
                                let new_valves_open = valves_open | bit;
                                valves_open_to_pressure_lost
                                    .entry(new_valves_open)
                                    .or_insert_with(|| pressure_lost - cur_rate);
                                Some((bit, cur_node))
                            })
                            .flatten(),
                    )
                    .cartesian_product(
                        valves_better
                            .get(cur_node_2 as usize)
                            .unwrap()
                            .1
                            .iter()
                            .map(move |other| (0, *other))
                            .chain(
                                ((valves_open >> cur_node_2) & 1 == 0)
                                    .then(|| {
                                        let cur_rate = valves_better[cur_node_2 as usize].0;
                                        if cur_rate == 0 {
                                            return None;
                                        }
                                        let bit = 1 << cur_node_2;
                                        let new_valves_open = valves_open | bit;
                                        valves_open_to_pressure_lost
                                            .entry(new_valves_open)
                                            .or_insert_with(|| pressure_lost - cur_rate);
                                        Some((bit, cur_node_2))
                                    })
                                    .flatten(),
                            ),
                    )
                    .map(|((bit_1, node_1), (bit_2, node_2))| {
                        if bit_1 != 0 && bit_2 != 0 {
                            let new_valves_open = valves_open | bit_1 | bit_2;
                            valves_open_to_pressure_lost
                                .entry(new_valves_open)
                                .or_insert_with(|| {
                                    pressure_lost
                                        - valves_better[node_1 as usize].0
                                        - valves_better[node_2 as usize].0
                                });
                        }
                        (
                            (time_left - 1, valves_open | bit_1 | bit_2, node_1, node_2),
                            pressure_lost,
                        )
                    })
            };
            for (other_node, weight) in adj {
                let new_dist = dist + weight;
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
