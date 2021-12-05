from typing import Tuple, List, Set
import numpy as np


MARKED = -1


def parse_line_of_ints(line: str, delimiter: str) -> np.array:
    line = filter(lambda s: s != "", line.split(delimiter))
    return np.array(list(map(int, line)))


def read() -> Tuple[np.array, np.ndarray]:
    with open("input.txt", "r") as file:
        numbers = parse_line_of_ints(file.readline(), delimiter=",")
        boards = []

        for line in file.readlines():
            if line == "\n":
                boards.append([])  # Create new board
                continue

            line = parse_line_of_ints(line, delimiter=" ")
            assert len(line) == 5, f"Failed parsing, found line of incorrect length: {line}"
            boards[-1].append(line)

    for i in range(len(boards)):
        boards[i] = np.array(boards[i])

    return numbers, np.array(boards)


def mark(number: int, boards: np.ndarray):
    boards[boards == number] = MARKED


def get_new_winners(boards: np.ndarray, boards_to_discard: Set[int] = None) -> List[int]:
    boards_to_discard = set() if boards_to_discard is None else boards_to_discard
    winners = []

    for i in range(boards.shape[0]):
        if i in boards_to_discard:
            continue

        for j in range(boards.shape[1]):
            if (boards[i, j, :] == MARKED).all() or (boards[i, :, j] == MARKED).all():
                winners.append(i)

    return winners


def get_score(number: int, board: np.ndarray) -> int:
    unmarked_sum = board[board != MARKED].sum()
    return unmarked_sum * number


def solve(numbers: List[int], boards: np.ndarray):
    first, last = None, None
    winners = set()

    for num in numbers:
        mark(num, boards)
        new_winners = get_new_winners(boards, winners)

        for winner in new_winners:
            winners.add(winner)
            score = get_score(num, boards[winner])

            if len(winners) == 1:
                first = score

            last = score

    return first, last


def main():
    numbers, boards = read()

    print(numbers)
    print(boards)

    first, last = solve(numbers, boards)

    print(first)
    print(last)


if __name__ == "__main__":
    main()