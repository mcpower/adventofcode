// from https://github.com/rust-lang/rust/issues/48731#issuecomment-370235493
pub fn slice_shift_char(a: &str) -> Option<(char, &str)> {
    let mut chars = a.chars();
    chars.next().map(|c| (c, chars.as_str()))
}

pub fn gcd(mut n: i64, mut m: i64) -> i64 {
    assert!(n > 0 && m > 0);
    while m != 0 {
        if m < n {
            std::mem::swap(&mut m, &mut n);
        }
        m %= n;
    }
    n
}

pub fn lcm(n: i64, m: i64) -> i64 {
    n / gcd(n, m) * m
}
