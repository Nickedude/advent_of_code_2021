from typing import Tuple
import numpy as np


def get_coordinate(s: str) -> Tuple[int, int]:
    return tuple(map(int, s.split(",")))


def read() -> np.ndarray:
    coordinates = []

    with open("input.txt", "r") as file:
        for line in file.readlines():
            fst, snd = line.split("->")
            x1, y1 = get_coordinate(fst)
            x2, y2 = get_coordinate(snd)
            coordinates.append(np.array([[x1, y1], [x2, y2]]))

    return np.array(coordinates)


def get_grid(lines: np.ndarray) -> np.ndarray:
    xmax = lines[:, :, 0].max()
    ymax = lines[:, :, 1].max()
    return np.zeros((ymax + 1, xmax + 1))


def get_indices(start: int, end: int) -> np.ndarray:
    step = 1

    if start > end:
        step = -1
        end -= 1
    else:
        end += 1

    return np.arange(start, end, step)


def add_vertical_lines(lines: np.ndarray, grid: np.ndarray):
    for i in range(lines.shape[0]):
        [[x1, y1], [x2, y2]] = lines[i]

        if x1 == x2:
            indices = get_indices(y1, y2)
            grid[indices, x1] += 1

        elif y1 == y2:
            indices = get_indices(x1, x2)
            grid[y1, indices] += 1


def get_diagonal_indices(x1: int, y1: int, x2: int, y2: int) -> Tuple[np.array, np.array]:
    xs = get_indices(x1, x2)
    ys = get_indices(y1, y2)

    return xs, ys


def add_diagonal_lines(lines: np.ndarray, grid: np.ndarray):
    for i in range(lines.shape[0]):
        [[x1, y1], [x2, y2]] = lines[i]

        if x1 != x2 and y1 != y2:
            xs, ys = get_diagonal_indices(x1, y1, x2, y2)
            grid[ys, xs] += 1


def score(grid: np.ndarray) -> int:
    return (grid >= 2).sum()


def main():
    lines = read()
    grid = get_grid(lines)

    add_vertical_lines(lines, grid)
    print(grid)
    print(score(grid))

    add_diagonal_lines(lines, grid)
    print(grid)
    print(score(grid))


if __name__ == "__main__":
    main()
