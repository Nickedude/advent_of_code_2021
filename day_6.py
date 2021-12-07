from time import time
from typing import List, Dict


def read() -> List[int]:
    with open("input.txt", "r") as file:
        fishes = file.readline()
        fishes = list(map(int, fishes.split(",")))

    fishes_map = {}

    for fish in fishes:
        if fish not in fishes_map:
            fishes_map[fish] = 0

        fishes_map[fish] += 1

    return fishes_map


def solve(fishes: Dict[int, int], num_days: int):
    for day in range(num_days):
        num_parents = fishes.get(0, 0)

        for days_left in range(0, 8):
            fishes[days_left] = fishes.get(days_left + 1, 0)

        fishes[6] += num_parents
        fishes[8] = num_parents

    total_num_fishes = 0

    for num_fishes in fishes.values():
        total_num_fishes += num_fishes

    print(total_num_fishes)


def main():
    fishes = read()
    solve(fishes, num_days=256)


if __name__ == "__main__":
    main()
