# Correct solution wrapped in heavy OOP (must be judged correct).
class CouponBond:
    def __init__(self, face, coupon_rate, n_years, ytm):
        self.face, self.c = face, face * coupon_rate
        self.n, self.y = n_years, ytm

    def cashflows(self):
        for t in range(1, self.n + 1):
            yield t, self.c + (self.face if t == self.n else 0.0)

    def price(self):
        return sum(cf / (1 + self.y) ** t for t, cf in self.cashflows())

    def macaulay(self):
        p = self.price()
        return sum(t * cf / (1 + self.y) ** t for t, cf in self.cashflows()) / p

    def modified(self):
        return self.macaulay() / (1 + self.y)

    def convexity(self):
        p = self.price()
        return sum(t * (t + 1) * cf / (1 + self.y) ** (t + 2)
                   for t, cf in self.cashflows()) / p

    def summary(self):
        return {"price": self.price(),
                "macaulay_duration_years": self.macaulay(),
                "modified_duration_years": self.modified(),
                "convexity": self.convexity()}


bond = CouponBond(100.0, 0.046, 7, 0.053)
result = bond.summary()
