mod year2018;
use mc_aoc::Runner;

fn main() {
    let mut r = Runner::new();
    year2018::setup(&mut r);
    r.run();
}
