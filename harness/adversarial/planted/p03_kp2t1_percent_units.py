# PLANTED ERROR (conventional, units): outputs percent (6.702) where the
# course convention is decimal (0.06702). Expected: numeric_wrong.
rf, erm = 0.023, 0.094

er_x = (rf + 0.62 * (erm - rf)) * 100
er_y = (rf + 1.18 * (erm - rf)) * 100
er_z = (rf + 1.51 * (erm - rf)) * 100

result = {
    "er_x": er_x,
    "er_y": er_y,
    "er_z": er_z,
    "alpha_y": 13.1 - er_y,
}
