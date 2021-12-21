import numpy as np

class Scanner:

    def __init__(self, id_, points):
        self.id_ = id_
        self.points = points


def read():
    with open("input.txt", "r") as file:
        scanners = []

        for line in file.readlines():
            line = line.rstrip("\n")

            if not line:
                continue

            if "scanner" in line:
                id_ = line.lstrip("--- ").rstrip(" ---")
                id_ = int(id_.split("scanner ")[1])
                scanners.append(Scanner(id_, []))
                continue

            nums = line.split(",")
            print(nums)
            x, y, z = tuple(map(int, nums))
            scanners[-1].points.append(np.array([x, y, z]))

    for scanner in scanners:
        scanner.points = np.array(scanner.points)

    return scanners


def solve(scanners):
    for i, fst_scanner in enumerate(scanners):
        for snd_scanner in scanners[i+1:]:
            for facing in ["x", "y", "z"]:
                for k in ["pos", "neg"]:
                    for rotation in [0, 90, 180, 270]:
                        rotated_points = rotate(snd_scanner.points, alt)


def main():
    scanners = read()
    solve(scanners)


if __name__ == "__main__":
    main()
