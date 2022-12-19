use std::collections::HashMap;

use itertools::Itertools;
use mcpower_aoc::runner::run_samples_and_arg;
use regex::Regex;

#[derive(Hash, Debug, PartialEq, Eq, Clone)]
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
    fn new() -> Self {
        Self {
            time_left: 24,
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

fn dp(blueprint: &Blueprint, state: DpState, cache: &mut HashMap<DpState, u64>) -> u64 {
    if state.time_left == 0 {
        return state.geodes;
    }

    if let Some(cached) = cache.get(&state) {
        return *cached;
    }

    let mut out = 0;
    let ore = if !state.skipped_ore_robot {
        if let Some(new_state) = state.make_ore_robot(blueprint) {
            out = out.max(dp(blueprint, new_state, cache));
            true
        } else {
            false
        }
    } else {
        false
    };
    let clay = if !state.skipped_clay_robot {
        if let Some(new_state) = state.make_clay_robot(blueprint) {
            out = out.max(dp(blueprint, new_state, cache));
            true
        } else {
            false
        }
    } else {
        false
    };
    let obsidian = if !state.skipped_obsidian_robot {
        if let Some(new_state) = state.make_obsidian_robot(blueprint) {
            out = out.max(dp(blueprint, new_state, cache));
            true
        } else {
            false
        }
    } else {
        false
    };
    let geode = if !state.skipped_geode_robot {
        if let Some(new_state) = state.make_geode_robot(blueprint) {
            out = out.max(dp(blueprint, new_state, cache));
            true
        } else {
            false
        }
    } else {
        false
    };

    let mut nothing = state.do_nothing();
    if ore {
        nothing.skipped_ore_robot = true;
    }
    if clay {
        nothing.skipped_clay_robot = true;
    }
    if obsidian {
        nothing.skipped_obsidian_robot = true;
    }
    if geode {
        nothing.skipped_geode_robot = true;
    }
    out = out.max(dp(blueprint, nothing, cache));

    cache.insert(state, out);
    out
}

fn solve(inp: &str, _is_sample: bool) -> (u64, i64) {
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
        .map(|blueprint| {
            dbg!(dp(blueprint, DpState::new(), &mut HashMap::new())) * u64::from(blueprint.id)
        })
        .sum::<u64>();

    let part2 = 0;

    (part1, part2)
}

fn main() {
    run_samples_and_arg(solve, SAMPLES);
}

const SAMPLES: &[&str] = &[r"
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"];
