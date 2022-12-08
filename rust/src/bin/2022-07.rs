use std::{collections::HashMap, env, fs};

use once_cell::sync::OnceCell;

// TODO: use &'a strs here
#[derive(Debug)]
enum Command {
    Cd { dir: String },
    Ls { entries: HashMap<String, LsEntry> },
}

// TODO: use NonZeroU64 here
#[derive(Debug)]
enum LsEntry {
    File { size: i64 },
    Dir,
}

#[derive(Debug)]
enum FsNode {
    File {
        size: i64,
    },
    Dir {
        children: OnceCell<HashMap<String, FsNode>>,
        size: OnceCell<i64>,
    },
}

impl From<LsEntry> for FsNode {
    fn from(entry: LsEntry) -> Self {
        match entry {
            LsEntry::File { size } => FsNode::File { size },
            LsEntry::Dir => FsNode::Dir {
                children: OnceCell::new(),
                size: OnceCell::new(),
            },
        }
    }
}

const TARGET_SPACE: i64 = 70000000 - 30000000;

impl FsNode {
    fn unwrap_children(&self) -> &OnceCell<HashMap<String, FsNode>> {
        match self {
            FsNode::File { size: _ } => panic!("tried unwrapping children of file"),
            FsNode::Dir { children, size: _ } => children,
        }
    }

    fn total_size(&self) -> i64 {
        match self {
            FsNode::File { size } => *size,
            FsNode::Dir { children, size } => *size.get_or_init(|| {
                children
                    .get()
                    .as_ref()
                    .expect("tried getting size of file that hasn't been ls'd")
                    .iter()
                    .map(|(_, v)| v.total_size())
                    .sum()
            }),
        }
    }

    fn part1(&self) -> i64 {
        match self {
            FsNode::File { size: _ } => 0,
            FsNode::Dir { children, size: _ } => {
                let total_size = self.total_size();
                let children_part1: i64 = children
                    .get()
                    .expect("tried getting size of file that hasn't been ls'd")
                    .iter()
                    .map(|(_, v)| v.part1())
                    .sum();
                children_part1 + if total_size <= 100000 { total_size } else { 0 }
            }
        }
    }

    fn part2(&self, target_reduction: i64) -> Option<i64> {
        match self {
            FsNode::File { size: _ } => None,
            FsNode::Dir { children, size: _ } => {
                let total_size = self.total_size();
                let best_child = children
                    .get()
                    .expect("tried getting size of file that hasn't been ls'd")
                    .iter()
                    .filter_map(|(_, v)| v.part2(target_reduction))
                    .min();
                if let Some(ans) = best_child {
                    Some(ans)
                } else if total_size >= target_reduction {
                    Some(total_size)
                } else {
                    None
                }
            }
        }
    }
}

fn solve(inp: &str) -> (i64, i64) {
    let root = FsNode::Dir {
        children: OnceCell::new(),
        size: OnceCell::new(),
    };
    // this is horrible but I can't be bothered reading too-many-lists to figure
    // out how to refer to a FsNode's parent
    let mut cur_path: Vec<String> = vec![];

    inp.strip_prefix("$ ")
        .expect("input didn't start with $ ")
        .split("\n$ ")
        .map(|command| {
            let mut lines = command.lines();
            let command = lines.next().expect("command was empty?");
            if command == "ls" {
                Command::Ls {
                    entries: lines
                        .map(|line| {
                            let (size, filename) =
                                line.split_once(' ').expect("ls line didn't have space");
                            let entry = if size == "dir" {
                                LsEntry::Dir
                            } else {
                                LsEntry::File {
                                    size: size.parse().expect("size wasn't dir or a number"),
                                }
                            };
                            (filename.to_owned(), entry)
                        })
                        .collect(),
                }
            } else if let Some(dir) = command.strip_prefix("cd ") {
                Command::Cd {
                    dir: dir.to_owned(),
                }
            } else {
                unreachable!("command wasn't ls or cd")
            }
        })
        .for_each(|command| match command {
            Command::Cd { dir } => match dir.as_str() {
                "/" => cur_path.clear(),
                ".." => {
                    cur_path.pop();
                }
                dir => cur_path.push(dir.to_owned()),
            },
            Command::Ls { entries } => {
                // get reference to current dir FsNode children
                // this will be fun and inefficient...
                let cur_children =
                    cur_path
                        .iter()
                        .fold(root.unwrap_children(), |children, child| {
                            children
                                .get()
                                .as_ref()
                                .expect("tried going into child which hasn't been ls'ed yet")
                                .get(child)
                                .expect("tried going into child which doesn't exist")
                                .unwrap_children()
                        });

                cur_children
                    .set(entries.into_iter().map(|(k, v)| (k, v.into())).collect())
                    .expect("tried ls'ing a directory that has already been ls'ed before");
            }
        });
    let part1 = root.part1();

    let target_reduction = root.total_size() - TARGET_SPACE;

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
