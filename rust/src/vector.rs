#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq)]
pub struct Vec2(pub i64, pub i64);

impl Vec2 {
    pub fn norm_inf(&self) -> i64 {
        self.0.abs().max(self.1.abs())
    }
}

impl std::ops::Add<Vec2> for Vec2 {
    type Output = Vec2;

    fn add(self, rhs: Vec2) -> Self::Output {
        Vec2(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl std::ops::AddAssign<Vec2> for Vec2 {
    fn add_assign(&mut self, rhs: Vec2) {
        self.0 += rhs.0;
        self.1 += rhs.1;
    }
}

impl std::ops::Neg for Vec2 {
    type Output = Vec2;

    fn neg(self) -> Self::Output {
        Vec2(-self.0, -self.1)
    }
}

impl std::ops::Sub<Vec2> for Vec2 {
    type Output = Vec2;

    fn sub(self, rhs: Vec2) -> Self::Output {
        Vec2(self.0 - rhs.0, self.1 - rhs.1)
    }
}
