use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashMap, HashSet},
};

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;
use regex::Regex;

#[derive(Hash, Debug, PartialEq, Eq, Clone, PartialOrd, Ord)]
struct DpState {
    time_left: u8,
    ore: u64,
    clay: u64,
    obsidian: u64,
    geodes: u64,
    ore_robots: u64,
    clay_robots: u64,
    obsidian_robots: u64,
    geode_robots: u64,
    skipped_ore_robot: bool,
    skipped_clay_robot: bool,
    skipped_obsidian_robot: bool,
    skipped_geode_robot: bool,
}

impl DpState {
    fn new(original_time: u8) -> Self {
        Self {
            time_left: original_time,
            ore: 0,
            clay: 0,
            obsidian: 0,
            geodes: 0,
            ore_robots: 1,
            clay_robots: 0,
            obsidian_robots: 0,
            geode_robots: 0,
            skipped_ore_robot: false,
            skipped_clay_robot: false,
            skipped_obsidian_robot: false,
            skipped_geode_robot: false,
        }
    }

    /// Assumes time_left >= 1.
    fn do_nothing(&self) -> DpState {
        DpState {
            time_left: self.time_left - 1,
            ore: self.ore + self.ore_robots,
            clay: self.clay + self.clay_robots,
            obsidian: self.obsidian + self.obsidian_robots,
            geodes: self.geodes + self.geode_robots,
            ..*self
        }
    }

    fn make_ore_robot(&self, blueprint: &Blueprint) -> Option<DpState> {
        Some(DpState {
            ore: self
                .ore
                .checked_sub(u64::from(blueprint.ore_robot_ore_cost))?
                + self.ore_robots,
            ore_robots: self.ore_robots + 1,
            skipped_ore_robot: false,
            skipped_clay_robot: false,
            skipped_obsidian_robot: false,
            skipped_geode_robot: false,
            ..self.do_nothing()
        })
    }

    fn make_clay_robot(&self, blueprint: &Blueprint) -> Option<DpState> {
        Some(DpState {
            ore: self
                .ore
                .checked_sub(u64::from(blueprint.clay_robot_ore_cost))?
                + self.ore_robots,
            clay_robots: self.clay_robots + 1,
            skipped_ore_robot: false,
            skipped_clay_robot: false,
            skipped_obsidian_robot: false,
            skipped_geode_robot: false,
            ..self.do_nothing()
        })
    }

    fn make_obsidian_robot(&self, blueprint: &Blueprint) -> Option<DpState> {
        Some(DpState {
            ore: self
                .ore
                .checked_sub(u64::from(blueprint.obsidian_robot_ore_cost))?
                + self.ore_robots,
            clay: self
                .clay
                .checked_sub(u64::from(blueprint.obsidian_robot_clay_cost))?
                + self.clay_robots,
            obsidian_robots: self.obsidian_robots + 1,
            skipped_ore_robot: false,
            skipped_clay_robot: false,
            skipped_obsidian_robot: false,
            skipped_geode_robot: false,
            ..self.do_nothing()
        })
    }

    fn make_geode_robot(&self, blueprint: &Blueprint) -> Option<DpState> {
        Some(DpState {
            ore: self
                .ore
                .checked_sub(u64::from(blueprint.geode_robot_ore_cost))?
                + self.ore_robots,
            obsidian: self
                .obsidian
                .checked_sub(u64::from(blueprint.geode_robot_obsidian_cost))?
                + self.obsidian_robots,
            geode_robots: self.geode_robots + 1,
            skipped_ore_robot: false,
            skipped_clay_robot: false,
            skipped_obsidian_robot: false,
            skipped_geode_robot: false,
            ..self.do_nothing()
        })
    }

    fn expand(
        &self,
        blueprint: &Blueprint,
    ) -> std::iter::Flatten<std::array::IntoIter<Option<DpState>, 5>> {
        let ore = if !self.skipped_ore_robot {
            self.make_ore_robot(blueprint)
        } else {
            None
        };
        let clay = if !self.skipped_clay_robot {
            self.make_clay_robot(blueprint)
        } else {
            None
        };
        let obsidian = if !self.skipped_obsidian_robot {
            self.make_obsidian_robot(blueprint)
        } else {
            None
        };
        let geode = if !self.skipped_geode_robot {
            self.make_geode_robot(blueprint)
        } else {
            None
        };
        let mut nothing = self.do_nothing();
        if ore.is_some() {
            nothing.skipped_ore_robot = true;
        }
        if clay.is_some() {
            nothing.skipped_clay_robot = true;
        }
        if obsidian.is_some() {
            nothing.skipped_obsidian_robot = true;
        }
        if geode.is_some() {
            nothing.skipped_geode_robot = true;
        }
        [ore, clay, obsidian, geode, Some(nothing)]
            .into_iter()
            .flatten()
    }

    /// Total wasted geodes at the moment.
    fn _total_wasted_geodes(&self, original_time: u8) -> u64 {
        let original_time = u64::from(original_time);
        let time_left = u64::from(self.time_left);
        (original_time - time_left) * original_time - self.geodes
    }

    /// Undestimate of total wasted geodes at the end.
    fn total_wasted_geodes_guess(&self, original_time: u8) -> u64 {
        let original_time = u64::from(original_time);
        let time_left = u64::from(self.time_left);
        original_time * original_time
            - (self.geodes + self.geode_robots * time_left + time_left * (time_left - 1) / 2)
    }
}

#[derive(Debug)]
struct Blueprint {
    id: u8,
    ore_robot_ore_cost: u8,
    clay_robot_ore_cost: u8,
    obsidian_robot_ore_cost: u8,
    obsidian_robot_clay_cost: u8,
    geode_robot_ore_cost: u8,
    geode_robot_obsidian_cost: u8,
}

fn _dp(blueprint: &Blueprint, state: DpState, cache: &mut HashMap<DpState, u64>) -> u64 {
    if state.time_left == 0 {
        return state.geodes;
    }

    if let Some(cached) = cache.get(&state) {
        return *cached;
    }

    let out = state
        .expand(blueprint)
        .map(|new_state| _dp(blueprint, new_state, cache))
        .max()
        .unwrap_or(0);

    cache.insert(state, out);
    out
}

fn dijkstra(blueprint: &Blueprint, original_time: u8) -> u64 {
    let mut pq = BinaryHeap::<Reverse<(u64, DpState)>>::new();
    pq.push(Reverse((0, DpState::new(original_time))));
    let mut seen: HashSet<DpState> = HashSet::new();
    loop {
        let Some(Reverse((_, state))) = pq.pop() else {
            unreachable!("didn't get end");
        };
        if state.time_left == 0 {
            break state.geodes;
        }

        for new_state in state.expand(blueprint) {
            if !seen.contains(&new_state) {
                pq.push(Reverse((
                    new_state.total_wasted_geodes_guess(original_time),
                    new_state.clone(),
                )));
                seen.insert(new_state);
            }
        }
    }
}

fn solve(inp: &str, _is_sample: bool) -> (u64, u64) {
    let re = Regex::new(r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$").unwrap();
    let blueprints = inp
        .lines()
        .map(|line| {
            let (
                id,
                ore_robot_ore_cost,
                clay_robot_ore_cost,
                obsidian_robot_ore_cost,
                obsidian_robot_clay_cost,
                geode_robot_ore_cost,
                geode_robot_obsidian_cost,
            ) = re
                .captures(line)
                .expect("line didn't match regex")
                .iter()
                .skip(1) // first one is always the entire match
                .map(|opt| {
                    opt.expect("capturing group didn't capture?")
                        .as_str()
                        .parse::<u8>()
                        .expect("capture wasn't number?")
                })
                .collect_tuple()
                .expect("didn't get 7 things from regex capture?");
            Blueprint {
                id,
                ore_robot_ore_cost,
                clay_robot_ore_cost,
                obsidian_robot_ore_cost,
                obsidian_robot_clay_cost,
                geode_robot_ore_cost,
                geode_robot_obsidian_cost,
            }
        })
        .collect::<Vec<_>>();
    let part1 = blueprints
        .iter()
        .map(|blueprint| dijkstra(blueprint, 24) * u64::from(blueprint.id))
        .sum::<u64>();

    let part2 = blueprints
        .iter()
        .take(3)
        .map(|blueprint| dijkstra(blueprint, 32))
        .product();

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"];
