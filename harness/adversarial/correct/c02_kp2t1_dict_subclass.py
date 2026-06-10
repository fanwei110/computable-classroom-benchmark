# Correct solution storing results in a dict SUBCLASS (must be judged correct).
class AnswerBox(dict):
    """A needlessly fancy container."""


rf = 0.023
erm = 0.094
betas = {"x": 0.62, "y": 1.18, "z": 1.51}

er = {s: rf + b * (erm - rf) for s, b in betas.items()}

result = AnswerBox()
result["er_x"] = er["x"]
result["er_y"] = er["y"]
result["er_z"] = er["z"]
result["alpha_y"] = 0.131 - er["y"]
