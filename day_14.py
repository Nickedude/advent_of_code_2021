from collections import defaultdict
from copy import deepcopy
from typing import Dict


def read():
    with open("input.txt", "r") as file:
        polymer = file.readline().rstrip("\n")
        mapping = {}

        for line in file.readlines():
            line = line.rstrip("\n")

            if not line:
                continue

            key, val = line.split(" -> ")
            mapping[key] = val

        return polymer, mapping


def get_score(polymer) -> int:
    counts = {}

    for c in polymer:
        if c not in counts:
            counts[c] = 0

        counts[c] += 1

    counts = list(counts.values())
    return max(counts) - min(counts)


def solve_one(polymer, mapping, num_steps):
    for step in range(num_steps):
        new_polymer = polymer[0]

        for i in range(1, len(polymer)):
            pair = polymer[i - 1:i + 1]
            new_polymer += mapping[pair]
            new_polymer += pair[1]

        polymer = new_polymer

    print(get_score(polymer))


def solve_two(polymer, mapping, num_steps):
    memory = {}
    counts = {polymer[0]: 1}

    for i in range(1, len(polymer)):
        pair = polymer[i - 1:i + 1]
        solution = count(pair, mapping, num_steps, memory)
        counts = merge_counts(solution, counts)

    counts = list(counts.values())
    print(max(counts) - min(counts))


def count(pair, mapping, num_steps, memory) -> Dict:
    if num_steps == 0:
        counts = defaultdict(lambda: 0)
        for c in pair:
            counts[c] += 1

        return counts

    key = pair + "-" + str(num_steps)

    if key not in memory:
        char = mapping[pair]

        left = pair[0] + char
        left_sol = count(left, mapping, num_steps - 1, memory)

        right = char + pair[1]
        right_sol = count(right, mapping, num_steps - 1, memory)

        left_sol[char] = left_sol[char] - 1  # Don't count char twice
        solution = merge_counts(left_sol, right_sol)

        memory[key] = solution

    return deepcopy(memory[key])


def merge_counts(counts_from, counts_to):
    for c, v in counts_from.items():
        if c not in counts_to:
            counts_to[c] = 0

        counts_to[c] += v

    return counts_to


def main():
    polymer, mapping = read()
    print(mapping)
    print(polymer)
    solve_one(polymer, mapping, 10)
    solve_two(polymer, mapping, 40)


if __name__ == "__main__":
    main()