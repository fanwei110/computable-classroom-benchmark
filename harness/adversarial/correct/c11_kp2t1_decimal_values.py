# Correct solution computed with decimal.Decimal values
# (must be judged correct after coercion).
from decimal import Decimal

rf = Decimal("0.023")
erm = Decimal("0.094")

er_x = rf + Decimal("0.62") * (erm - rf)
er_y = rf + Decimal("1.18") * (erm - rf)
er_z = rf + Decimal("1.51") * (erm - rf)

result = {
    "er_x": er_x,
    "er_y": er_y,
    "er_z": er_z,
    "alpha_y": Decimal("0.131") - er_y,
}
