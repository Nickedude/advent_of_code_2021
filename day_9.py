import numpy as np


def read():
    with open("input.txt", "r") as file:
        lines = []

        for line in file.readlines():
            line = [int(c) for c in line if c != "\n"]
            lines.append(np.array(line))

        return np.array(lines)


def get_low_points(grid: np.ndarray):
    width = grid.shape[1]
    height = grid.shape[0]
    low_points = []

    for i in range(height):
        for j in range(width):
            current = grid[i][j]
            neighbors = get_neighbors(grid, i, j)
            neighbors = np.array([grid[x][y] for (x,y) in neighbors])

            if (current < neighbors).all():
                low_points.append((current, (i,j)))

    return low_points


def solve_two(grid: np.ndarray, low_points: np.ndarray):
    sizes = []

    for (i, j) in low_points:
        sizes.append(bfs(grid, i, j))

    sizes = sorted(sizes)[-3:]
    answer = 1

    for size in sizes:
        answer *= size

    print(answer)


def bfs(grid: np.ndarray, i: int, j: int):
    visited = set()
    neighbors = [(i, j)]

    while neighbors:
        (i, j) = neighbors.pop(0)

        if (i, j) in visited or grid[i][j] > 8:
            continue

        visited.add((i, j))
        new_neighbors = get_neighbors(grid, i, j)

        for neighbor in new_neighbors:
            if neighbor not in visited:
                neighbors.append(neighbor)

    return len(visited)


def get_neighbors(grid: np.ndarray, i: int, j: int):
    width = grid.shape[1]
    height = grid.shape[0]
    neighbors = []

    if i + 1 < height:
        neighbors.append((i + 1, j))
    if i - 1 > -1:
        neighbors.append((i - 1, j))
    if j + 1 < width:
        neighbors.append((i, j + 1))
    if j - 1 > -1:
        neighbors.append((i, j - 1))

    return neighbors


def main():
    grid = read()
    print(grid)
    low_points = get_low_points(grid)

    low_point_values = np.array([value for (value, _) in low_points])
    low_point_coordinates = np.array([coordinate for (_, coordinate) in low_points])
    print(f"Low points: {low_point_values}")
    low_point_values += 1
    print(f"Sum of low points: {low_point_values.sum()}")

    solve_two(grid, low_point_coordinates)


if __name__ == "__main__":
    main()
