use std::{collections::HashMap, env, fs};

use once_cell::unsync::OnceCell;

#[derive(Debug)]
enum FsNode<'a, 's> {
    Dir(FsDir<'a, 's>),
    File { size: i64 },
}

#[derive(Debug)]
struct FsDir<'a, 's> {
    parent: Option<&'a FsDir<'a, 's>>,
    children: OnceCell<HashMap<&'s str, FsNode<'a, 's>>>,
    size: OnceCell<i64>,
}

impl<'a, 's> FsDir<'a, 's> {
    fn new_dir(parent: Option<&'a FsDir<'a, 's>>) -> FsDir<'a, 's> {
        FsDir {
            parent,
            children: OnceCell::new(),
            size: OnceCell::new(),
        }
    }

    fn get_size(&self) -> i64 {
        *self.size.get_or_init(|| {
            self.children
                .get()
                .expect("tried getting size of directory that hasn't been ls'd")
                .iter()
                .map(|(_, v)| v.get_size())
                .sum()
        })
    }

    fn part1(&self) -> i64 {
        let total_size = self.get_size();
        let children_part1: i64 = self
            .children
            .get()
            .expect("tried getting part 1 of directory that hasn't been ls'd")
            .iter()
            .filter_map(|(_, v)| v.as_dir())
            .map(FsDir::part1)
            .sum();
        children_part1 + if total_size <= 100000 { total_size } else { 0 }
    }

    fn part2(&self, target_reduction: i64) -> Option<i64> {
        let total_size = self.get_size();
        self.children
            .get()
            .expect("tried getting part 2 of directory that hasn't been ls'ed")
            .iter()
            .filter_map(|(_, v)| v.as_dir())
            .filter_map(|dir| dir.part2(target_reduction))
            .chain(if total_size >= target_reduction {
                Some(total_size)
            } else {
                None
            })
            .min()
    }
}

const TARGET_SPACE: i64 = 70000000 - 30000000;

impl<'a, 's> FsNode<'a, 's> {
    fn get_size(&self) -> i64 {
        match self {
            FsNode::File { size } => *size,
            FsNode::Dir(dir) => dir.get_size(),
        }
    }

    fn as_dir(&self) -> Option<&FsDir<'a, 's>> {
        if let Self::Dir(v) = self {
            Some(v)
        } else {
            None
        }
    }
}

fn solve(inp: &str) -> (i64, i64) {
    let root = FsDir::new_dir(None);
    let mut cur_dir = &root;

    for command in inp
        .strip_prefix("$ ")
        .expect("input didn't start with $ ")
        .split("\n$ ")
    {
        let mut lines = command.lines();
        let command = lines.next().expect("command was empty?");
        if command == "ls" {
            let entries = lines
                .map(|line| {
                    let (size, filename) = line.split_once(' ').expect("ls line didn't have space");
                    let entry = if size == "dir" {
                        FsNode::Dir(FsDir::new_dir(Some(cur_dir)))
                    } else {
                        FsNode::File {
                            size: size.parse().expect("size wasn't dir or a number"),
                        }
                    };
                    (filename, entry)
                })
                .collect();
            cur_dir
                .children
                .set(entries)
                .expect("tried ls'ing a directory that has already been ls'ed before");
        } else if let Some(dir) = command.strip_prefix("cd ") {
            match dir {
                "/" => cur_dir = &root,
                ".." => cur_dir = cur_dir.parent.expect("tried cd'ing .. from /"),
                _ => {
                    cur_dir = cur_dir
                        .children
                        .get()
                        .expect("tried cd'ing from a directory that hasn't been ls'ed")
                        .get(dir)
                        .expect("tried cd'ing into a directory that doesn't exist")
                        .as_dir()
                        .expect("tried cd'ing to a file")
                }
            }
        } else {
            unreachable!("command wasn't ls or cd")
        }
    }
    let part1 = root.part1();

    let target_reduction = root.get_size() - TARGET_SPACE;

    let part2 = root
        .part2(target_reduction)
        .expect("couldn't find part 2 answer");
    (part1, part2)
}

fn main() {
    dbg!(solve(
        r#"$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"#
    ));
    let filename = env::args().nth(1).expect("missing filename arg");
    let contents = fs::read_to_string(filename).expect("opening file failed");

    let (part1, part2) = solve(&contents);
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
