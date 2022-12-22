// from https://github.com/rust-lang/rust/issues/48731#issuecomment-370235493
pub fn slice_shift_char(a: &str) -> Option<(char, &str)> {
    let mut chars = a.chars();
    chars.next().map(|c| (c, chars.as_str()))
}
