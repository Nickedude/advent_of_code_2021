import numpy as np
import heapq


def read():
    with open("input.txt", "r") as file:
        grid = []

        for line in file.readlines():
            line = line.rstrip("\n")
            grid.append(np.array(list(map(int, [c for c in line]))))

        return np.array(grid)


def create_big_grid(grid):
    multiplier = 5
    height, width = grid.shape
    big_grid = np.zeros((height * 5, width * 5))

    for row in range(multiplier):
        for col in range(multiplier):
            row_start = row * height
            col_start = col * width
            row_end = (row + 1) * height
            col_end = (col + 1) * width
            grid_to_insert = grid + row + col

            # while (grid_to_insert > 9).any():
            #     indices = np.nonzero(grid_to_insert > 9)
            #     grid_to_insert[indices] = grid_to_insert[indices] - 8
            for i in range(grid_to_insert.shape[0]):
                for j in range(grid_to_insert.shape[1]):
                    if grid_to_insert[i, j] > 9:
                        grid_to_insert[i, j] -= 9

            big_grid[row_start:row_end, col_start:col_end] = grid_to_insert

    return big_grid

def ucs(grid):
    costs = {}
    predecessors = {}
    visited = set()
    nodes = []
    heapq.heappush(nodes, (0, (0, 0), (-1, -1)))
    end = grid.shape[0] - 1, grid.shape[1] - 1

    while nodes:
        cost, pos, pred = heapq.heappop(nodes)

        if pos not in costs or costs[pos] > cost:
            costs[pos] = cost
            predecessors[pos] = pred

        if pos == end:
            return cost

        if pos not in visited:
            visited.add(pos)
            row, col = pos
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]

            for neighbor in neighbors:
                row, col = neighbor

                if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
                    heapq.heappush(nodes, (cost + grid[row, col], neighbor, pos))



def main():
    grid = read()
    print(grid)
    cost = ucs(grid)
    print(cost)
    cost = ucs(create_big_grid(grid))
    print(cost)


if __name__ == "__main__":
    main()