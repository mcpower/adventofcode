use std::{collections::HashMap, env, fs};

use once_cell::unsync::OnceCell;

#[derive(Debug)]
enum FsNode<'a, 's> {
    File {
        parent: &'a FsNode<'a, 's>,
        size: i64,
    },
    Dir {
        parent: Option<&'a FsNode<'a, 's>>,
        children: OnceCell<HashMap<&'s str, FsNode<'a, 's>>>,
        size: OnceCell<i64>,
    },
}

const TARGET_SPACE: i64 = 70000000 - 30000000;

impl<'a, 's> FsNode<'a, 's> {
    fn new_dir(parent: Option<&'a FsNode<'a, 's>>) -> FsNode<'a, 's> {
        FsNode::Dir {
            parent,
            children: OnceCell::new(),
            size: OnceCell::new(),
        }
    }

    fn unwrap_children<'b: 's>(&'b self) -> &'b OnceCell<HashMap<&'s str, FsNode>> {
        match self {
            FsNode::File { size: _, parent: _ } => panic!("tried unwrapping children of file"),
            FsNode::Dir {
                children,
                size: _,
                parent: _,
            } => children,
        }
    }

    fn total_size(&self) -> i64 {
        match self {
            FsNode::File { size, parent: _ } => *size,
            FsNode::Dir {
                children,
                size,
                parent: _,
            } => *size.get_or_init(|| {
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
            FsNode::File { size: _, parent: _ } => 0,
            FsNode::Dir {
                children,
                size: _,
                parent: _,
            } => {
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
            FsNode::File { size: _, parent: _ } => None,
            FsNode::Dir {
                children,
                size: _,
                parent: _,
            } => {
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

    fn get_parent(&self) -> &'a FsNode<'a, 's> {
        match self {
            FsNode::File { parent, .. } => parent,
            FsNode::Dir { parent, .. } => parent.expect("tried getting parent of root"),
        }
    }
}

fn solve(inp: &str) -> (i64, i64) {
    let root = FsNode::new_dir(None);
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
                        FsNode::new_dir(Some(cur_dir))
                    } else {
                        FsNode::File {
                            size: size.parse().expect("size wasn't dir or a number"),
                            parent: cur_dir,
                        }
                    };
                    (filename, entry)
                })
                .collect();
            cur_dir
                .unwrap_children()
                .set(entries)
                .expect("tried ls'ing a directory that has already been ls'ed before");
        } else if let Some(dir) = command.strip_prefix("cd ") {
            match dir {
                "/" => cur_dir = &root,
                ".." => cur_dir = cur_dir.get_parent(),

                dir => {
                    cur_dir = cur_dir
                        .unwrap_children()
                        .get()
                        .expect("tried cd'ing from a file??")
                        .get(dir)
                        .expect("tried cd'ing into a directory that doesn't exist")
                }
            }
        } else {
            unreachable!("command wasn't ls or cd")
        }
    }
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
