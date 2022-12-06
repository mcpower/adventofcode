use std::{
    env,
    ffi::OsStr,
    path::{Path, PathBuf},
};

use chrono::prelude::*;
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

type AocYear = u16;
type AocDay = u8;
type AocYearDay = (AocYear, AocDay);

/// this function is cursed
pub fn get_program_day_and_year() -> Option<AocYearDay> {
    let binary_path = PathBuf::from(env::args_os().next()?);
    let binary_name = binary_path.file_name()?.to_str()?;
    let (year, day) = binary_name.split('-').collect_tuple()?;
    Some((year.parse().ok()?, day.parse().ok()?))
}

pub fn get_aoc_start(year: AocYear, day: AocDay) -> DateTime<FixedOffset> {
    FixedOffset::east_opt(-5 * 3600)
        .unwrap()
        .from_local_datetime(
            &NaiveDate::from_ymd_opt(year.into(), 12, day.into())
                .unwrap()
                .and_time(Default::default()),
        )
        .unwrap()
}
