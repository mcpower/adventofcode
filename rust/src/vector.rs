#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct Vec2(pub i64, pub i64);

impl Vec2 {
    pub fn map<F>(&self, f: F) -> Vec2
    where
        F: Fn(i64) -> i64,
    {
        Vec2(f(self.0), f(self.1))
    }

    pub fn norm_1(&self) -> i64 {
        self.0.abs() + self.1.abs()
    }

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

impl std::ops::SubAssign<Vec2> for Vec2 {
    fn sub_assign(&mut self, rhs: Vec2) {
        self.0 -= rhs.0;
        self.1 -= rhs.1;
    }
}

impl std::ops::Mul<Vec2> for i64 {
    type Output = Vec2;

    fn mul(self, rhs: Vec2) -> Self::Output {
        Vec2(self * rhs.0, self * rhs.1)
    }
}

impl std::ops::Mul<i64> for Vec2 {
    type Output = Vec2;

    fn mul(self, rhs: i64) -> Self::Output {
        Vec2(self.0 * rhs, self.1 * rhs)
    }
}

impl std::ops::MulAssign<i64> for Vec2 {
    fn mul_assign(&mut self, rhs: i64) {
        self.0 *= rhs;
        self.1 *= rhs;
    }
}

impl std::ops::Div<i64> for Vec2 {
    type Output = Vec2;

    fn div(self, rhs: i64) -> Self::Output {
        Vec2(self.0 / rhs, self.1 / rhs)
    }
}

impl std::ops::DivAssign<i64> for Vec2 {
    fn div_assign(&mut self, rhs: i64) {
        self.0 /= rhs;
        self.1 /= rhs;
    }
}

pub const FOUR_ADJ: [Vec2; 4] = [Vec2(-1, 0), Vec2(0, 1), Vec2(1, 0), Vec2(0, -1)];
