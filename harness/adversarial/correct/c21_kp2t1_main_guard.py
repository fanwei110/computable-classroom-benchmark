# Correct solution that follows the common script idiom: all work inside
# main(), result assigned under `if __name__ == "__main__"`. A classroom
# run (python file.py) produces `result`; the harness must too.
# (Added 2026-06-11 with the runpy executor amendment - DEVIATIONS.md #5.)


def main():
    rf, erm = 0.023, 0.094
    betas = {"x": 0.62, "y": 1.18, "z": 1.51}
    er = {s: rf + b * (erm - rf) for s, b in betas.items()}
    return {
        "er_x": er["x"],
        "er_y": er["y"],
        "er_z": er["z"],
        "alpha_y": 0.131 - er["y"],
    }


if __name__ == "__main__":
    result = main()
    print(result)
