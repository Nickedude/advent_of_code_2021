
def read():
    with open("input.txt") as file:
        input_str = file.readline()
        numbers = list(map(int, input_str.split(",")))

    return numbers


def solve_one(positions):
    min_cost = float("inf")

    for destination in positions:
        cost = 0

        for pos in positions:
            cost += abs(destination - pos)

        if cost < min_cost:
            min_cost = cost

    print(min_cost)


def solve_two(positions):
    min_cost = float("inf")
    start = min(positions)
    end = max(positions)

    for destination in range(start, end):
        cost = 0

        for pos in positions:
            delta = abs(destination - pos)
            delta = int((delta * (delta + 1)) / 2)
            cost += delta

        if cost < min_cost:
            min_cost = cost

    print(min_cost)


def main():
    positions = read()
    print(positions)
    solve_one(positions)
    solve_two(positions)


if __name__ == "__main__":
    main()
