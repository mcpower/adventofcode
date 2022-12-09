use std::env;
use std::ffi::OsStr;

use mcpower_aoc::runner::path_in_ancestor;

fn main() {
    dbg!(path_in_ancestor(
        &env::current_dir().unwrap(),
        OsStr::new("token.txt")
    ));
}
