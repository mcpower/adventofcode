use std::{
    env,
    ffi::OsStr,
    path::{Path, PathBuf},
};

use itertools::Itertools;

pub fn path_in_ancestor(mut cur_path: &Path, file_name: &OsStr) -> Option<PathBuf> {
    loop {
        if let Some(path) = cur_path
            .read_dir()
            .unwrap()
            .map(|result| result.unwrap())
            .find(|entry| entry.file_name() == file_name)
        {
            break Some(path.path());
        }

        if let Some(parent) = cur_path.parent() {
            cur_path = parent;
            continue;
        }

        break None;
    }
}

/// this function is cursed
pub fn get_program_day_and_year() -> Option<(u16, u8)> {
    let binary_path = PathBuf::from(env::args_os().next()?);
    let binary_name = binary_path.file_name()?.to_str()?;
    let (year, day) = binary_name.split('-').collect_tuple()?;
    Some((year.parse().ok()?, day.parse().ok()?))
}
