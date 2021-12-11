import numpy as np


def read():
    with open("input.txt", "r") as file:
        energy_levels = []
        for line in file.readlines():
            line = line[:-1] if line[-1] == "\n" else line
            line = [int(c) for c in line]
            energy_levels.append(np.array(line))

        return np.array(energy_levels)


def get_neighbors(i, j, height, width):
    neighbors = []

    for row in range(i-1, i+2):
        for col in range(j-1, j+2):
            if row == i and col == j:
                continue

            if -1 < row < height and -1 < col < width:
                neighbors.append((row, col))

    return neighbors


def solve_one(energy_levels, num_steps):
    num_flashes = 0

    for step in range(num_steps):
        num_flashes += take_step(energy_levels)

    return num_flashes


def solve_two(energy_levels):
    for step in range(1000):
        num_flashes = take_step(energy_levels)

        if num_flashes == energy_levels.shape[0] * energy_levels.shape[1]:
            return step


def take_step(energy_levels):
    num_flashes = 0
    energy_levels += 1
    has_flashed = np.zeros(energy_levels.shape).astype(bool)
    flashing = np.argwhere(energy_levels > 9)
    flashing = list(flashing)

    while flashing:
        i, j = flashing.pop(0)

        if has_flashed[i, j]:
            continue

        has_flashed[i, j] = True
        num_flashes += 1

        for row, col in get_neighbors(i, j, *energy_levels.shape):
            if has_flashed[row, col]:
                continue

            energy_levels[row, col] += 1

            if energy_levels[row, col] > 9:
                flashing.append((row, col))

    energy_levels[has_flashed] = 0

    return num_flashes


def main():
    energy_levels = read()
    print(energy_levels)

    num_flashes = solve_one(energy_levels, num_steps=100)
    print(f"Num flashes: {num_flashes}")

    num_steps = solve_two(energy_levels)
    num_steps += 100  # From solving first problem
    print(f"All flashed at step: {num_steps + 1}")


if __name__ == "__main__":
    main()