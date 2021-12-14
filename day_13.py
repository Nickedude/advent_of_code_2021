import numpy as np

def read():
    with open("input.txt", "r") as file:
        dots = []
        folds = []
        for line in file.readlines():
            line = line[:-1] if line[-1] == "\n" else line

            if not line:
                continue
            elif "fold" in line:
                line = line[len("fold along "):]
                axis, val = line.split("=")
                val = int(val)
                folds.append((axis, val))
            else:
                x, y = line.split(",")
                dots.append((int(x), int(y)))

    return dots, folds


def fold_left(grid, coordinate):
    left = grid[:, :coordinate]
    left = left[:, ::-1]
    right = grid[:, coordinate + 1:]
    width_right = right.shape[1]
    width_left = left.shape[1]
    if width_left > width_right:
        diff = width_left - width_right
        right = np.hstack((right, np.zeros((right.shape[0], diff))))

    elif width_right > width_left:
        diff = width_right - width_left
        right = np.hstack((left, np.zeros((left.shape[0], diff))))

    return left + right


def fold_up(grid, coordinate):
    upper = grid[:coordinate, :]
    lower = grid[coordinate + 1:, :]
    lower = lower[::-1, :]

    height_upper = upper.shape[0]
    height_lower = lower.shape[0]

    if height_upper > height_lower:
        diff = height_upper - height_lower
        lower = np.vstack((lower, np.zeros((diff, lower.shape[1]))))

    elif height_lower > height_upper:
        diff = height_lower - height_upper
        upper = np.hstack((upper, np.zeros((diff, upper.shape[1]))))

    return upper + lower


def solve(dots, folds):
    xmax = max([x for (x, y) in dots])
    ymax = max([y for (x, y) in dots])
    grid = np.zeros((ymax + 1, xmax + 1))

    for x, y in dots:
        grid[y, x] = 1

    for axis, coordinate in folds:
        if axis == "x":
            grid = fold_left(grid, coordinate)
        elif axis == "y":
            grid = fold_up(grid, coordinate)
        else:
            raise NotImplementedError()

        print(f"Num dots: {(grid > 0).sum()}")

    grid[grid > 0] = 1
    print(grid)


def main():
    dots, folds = read()
    print(dots)
    print(folds)
    solve(dots, folds)


if __name__ == "__main__":
    main()
