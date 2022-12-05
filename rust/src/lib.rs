use std::{
    ffi::OsStr,
    path::{Path, PathBuf},
};

pub fn path_in_ancestor(mut cur_path: &Path, file_name: &OsStr) -> Option<PathBuf> {
    loop {
        let Some(path) = cur_path
            .read_dir()
            .unwrap()
            .map(|result| result.unwrap())
            .find(|entry| entry.file_name() == file_name) else {
                if let Some(parent) = cur_path.parent() {
                    cur_path = parent;
                    continue;
                } else {
                    break None;
                }
            };
        break Some(path.path());
    }
}
