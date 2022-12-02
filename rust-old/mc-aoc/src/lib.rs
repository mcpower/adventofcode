use chrono::prelude::*;
use std::collections::hash_map::Entry;
use std::collections::HashMap;
use std::fmt;
use std::ops::Add;
use std::path;

#[derive(Ord, PartialOrd, Eq, PartialEq, Copy, Clone, Hash, Debug)]
pub struct Day {
    year: u16,
    day: u8,
}

impl Day {
    pub fn new(year: u16, day: u8) -> Day {
        if year < 2015 {
            panic!("year {} is less than 2015", year);
        }
        if year >= 3000 {
            panic!(
                "year {} is over 3000 - is AoC still running after 900 years?",
                year
            );
        }
        if !(1..=25).contains(&day) {
            panic!("day {} is not between 1 and 25", day);
        }
        Day { year, day }
    }
}

impl fmt::Display for Day {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} Day {}", self.year, self.day)
    }
}

#[derive(Ord, PartialOrd, Eq, PartialEq, Copy, Clone, Hash, Debug)]
pub struct Problem {
    day: Day,
    part: u8,
}

impl Problem {
    pub fn new(day: Day, part: u8) -> Problem {
        if part != 1 && part != 2 {
            panic!("part {} is not 1 or 2", part);
        }
        Problem { day, part }
    }

    pub fn new_with_day(year: u16, day: u8, part: u8) -> Problem {
        Problem::new(Day::new(year, day), part)
    }
}

impl fmt::Display for Problem {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} Part {}", self.day, self.part)
    }
}

#[derive(Eq, PartialEq, Copy, Clone, Debug)]
pub struct Sample<'a> {
    input: &'a str,
    output: &'a str,
}

impl<'a> Sample<'a> {
    pub fn new(input: &'a str, output: &'a str) -> Sample<'a> {
        Sample { input, output }
    }

    pub fn from_single_str(sample: &'a str) -> Sample<'a> {
        let mut it = sample
            .trim_matches('\n')
            .split(r"\/-\/-OUTPUT-\/-\/")
            .map(|case| case.trim_matches('\n'));
        if let Some(input) = it.next() {
            if let Some(output) = it.next() {
                if it.next() != None {
                    panic!("more than one output found for sample");
                }
                Sample { input, output }
            } else {
                // no output
                Sample { input, output: "" }
            }
        } else {
            panic!("no input found for sample");
        }
    }

    pub fn from_str(samples: &'a str) -> Vec<Sample<'a>> {
        samples
            .trim_matches('\n')
            .split("=-=-=-=-=-=-=-=-=-")
            .map(|sample| sample.trim_matches('\n'))
            .filter(|sample| !sample.is_empty())
            .map(Sample::from_single_str)
            .collect()
    }
}

type Solution<'a> = &'a dyn Fn(&str, bool) -> String;
type DoubleSolution<'a> = &'a dyn Fn(&str, bool) -> (String, String);

pub struct Runner<'a> {
    solutions: HashMap<Problem, Solution<'a>>,
    double_solutions: HashMap<Day, DoubleSolution<'a>>,
    samples: HashMap<Problem, Vec<Sample<'a>>>,
    cookie: Option<String>,
}

impl<'a> Runner<'a> {
    pub fn add_solution(&mut self, day: Day, part: u8, solution: Solution<'a>) {
        let problem = Problem::new(day, part);
        if self.solutions.contains_key(&problem) {
            panic!("trying to add multiple solutions for {:?}", problem);
        }
        self.solutions.insert(problem, solution);
    }

    pub fn add_samples(&mut self, day: Day, part: u8, sample_str: &'a str) {
        let samples = Sample::from_str(sample_str);
        match self.samples.entry(Problem::new(day, part)) {
            Entry::Occupied(mut entry) => {
                entry.get_mut().extend(samples);
            }
            Entry::Vacant(entry) => {
                entry.insert(samples);
            }
        }
    }

    pub fn add_sample(&mut self, day: Day, part: u8, input: &'a str, output: &'a str) {
        self.samples
            .entry(Problem::new(day, part))
            .or_insert_with(Vec::new)
            .push(Sample::new(input, output));
    }

    pub fn run(&self) {
        if let Some(problem) = self.solutions.keys().max() {
            self.run_day(problem.day);
        } else {
            panic!("no solutions found");
        }
    }

    pub fn run_day(&self, day: Day) {
        // prefer double_solutions over solutions
        // check whether we have a solution first
        unimplemented!()
    }

    pub fn run_problem(&self, problem: Problem) {
        // prefer solutions over double_solutions
        // check whether we have a solution first
        unimplemented!()
    }

    pub fn get_actual_input(self, day: Day) -> Result<String, String> {
        let Day {
            year: year_num,
            day: day_num,
        } = day;
        let mut path: path::PathBuf = [
            "input",
            year_num.to_string().as_str(),
            day_num.to_string().as_str(),
        ]
        .iter()
        .collect();
        path.set_extension("txt");
        if !path.is_file() {
            // figure out whether we can fetch it
            let timezone = FixedOffset::west(5 * 3600);
            let release_time = timezone
                .ymd(year_num as i32, 12, day_num as u32)
                .and_hms(0, 0, 0);
            let current_time = Utc::now().with_timezone(&timezone);
            if current_time < release_time {
                return Err(format!(
                    "{} releases in {}",
                    day,
                    release_time - current_time
                ));
            }
            let parent_dir = path.parent().unwrap();
            std::fs::create_dir_all(parent_dir)
                .map_err(|_| format!("can't create directory {:?}", parent_dir))?;
            // TODO: fetch file and write to path
            unimplemented!()
        } else {
            std::fs::read_to_string(path.as_path()).map_err(|_| format!("can't read {:?}", path))
        }
    }

    pub fn new() -> Runner<'a> {
        Runner {
            solutions: HashMap::new(),
            double_solutions: HashMap::new(),
            samples: HashMap::new(),
            cookie: Runner::get_cookie(),
        }
    }

    pub fn get_cookie() -> Option<String> {
        // TODO
        None
    }

    // not sure if this will be used?
    // useful for pre-running the program before an implementation is written
    // to download the input
    pub fn _get_today() -> Option<Day> {
        // add one hour to get possibly upcoming day
        let upcoming_aoc_date = Utc::now()
            .with_timezone(&FixedOffset::west(5 * 3600))
            .add(chrono::Duration::hours(1))
            .date();
        if upcoming_aoc_date.month() != 12 || upcoming_aoc_date.day() > 25 {
            None
        } else {
            Some(Day::new(
                upcoming_aoc_date.year() as u16,
                upcoming_aoc_date.day() as u8,
            ))
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::{Day, Runner, Sample};
    use std::panic;

    static LENGTH_SAMPLE: &'static str = r#"
=-=-=-=-=-=-=-=-=-
hello world
\/-\/-OUTPUT-\/-\/
11
=-=-=-=-=-=-=-=-=-
pizza
\/-\/-OUTPUT-\/-\/
5
=-=-=-=-=-=-=-=-=-
12345
=-=-=-=-=-=-=-=-=-
"#;
    static DAY: Day = Day { year: 2018, day: 1 };

    fn empty_solution(_inp: &str, _sample: bool) -> String {
        "".to_string()
    }

    fn identity_solution(inp: &str, _sample: bool) -> String {
        inp.to_string()
    }

    fn length_solution(inp: &str, _sample: bool) -> String {
        inp.len().to_string()
    }

    fn panics<T: FnOnce() -> ()>(function: T) -> bool {
        let old_hook = panic::take_hook();
        panic::set_hook(Box::new(|_| {}));
        let result = panic::catch_unwind(panic::AssertUnwindSafe(function));
        panic::set_hook(old_hook);
        result.is_err()
    }

    #[test]
    fn sample_parses_correctly() {
        let samples = Sample::from_str(LENGTH_SAMPLE);
        let expected = vec![
            Sample::new("hello world", "11"),
            Sample::new("pizza", "5"),
            Sample::new("12345", ""),
        ];
        assert_eq!(samples, expected);
    }

    // type-check only function
    fn _can_add_multiple_solutions() {
        let mut runner = Runner::new();
        runner.add_solution(DAY, 1, &empty_solution);
        runner.add_solution(DAY, 2, &identity_solution);
    }

    #[test]
    fn cannot_add_multiple_solutions_one_problem() {
        let mut runner = Runner::new();
        runner.add_solution(DAY, 1, &empty_solution);

        assert!(panics(|| runner.add_solution(DAY, 1, &identity_solution)));
    }

    fn setup_function(runner: &mut Runner) {
        runner.add_solution(DAY, 1, &identity_solution);
        runner.add_solution(DAY, 2, &length_solution);
        runner.add_samples(
            DAY,
            1,
            r#"
=-=-=-=-=-=-=-=-=-
hello world
\/-\/-OUTPUT-\/-\/
hello world
=-=-=-=-=-=-=-=-=-
pizza
\/-\/-OUTPUT-\/-\/
pizza
=-=-=-=-=-=-=-=-=-
12345
=-=-=-=-=-=-=-=-=-
"#,
        );
    }

    #[test]
    fn setup_functions_work() {
        let mut runner = Runner::new();
        setup_function(&mut runner);
    }
}
