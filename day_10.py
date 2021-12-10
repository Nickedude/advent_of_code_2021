def read():
    with open("input.txt", "r") as file:
        lines = file.readlines()
        lines = [line[:-1] for line in lines]
        return lines


def get_score(stack):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    current_score = 0

    for c in stack:
        current_score *= 5
        current_score += scores[c]

    return current_score


def solve(lines):
    error = 0
    all_scores = []
    openers = {"(", "<", "{", "["}
    matches = {")": "(", "]": "[", "}": "{", ">": "<"}
    errors = {")": 3, "]": 57, "}": 1197, ">": 25137}

    for line in lines:
        stack = []
        corrupt = False

        for i, c in enumerate(line):
            if c in openers:
                stack = [c] + stack
            else:
                prev = stack.pop(0)

                if prev != matches[c]:
                    error += errors[c]
                    corrupt = True
                    break

        if not corrupt:
            all_scores.append(get_score(stack))

    print(error)

    all_scores = sorted(all_scores)
    idx = len(all_scores) // 2
    print(all_scores[idx])


def main():
    lines = read()
    solve(lines)


if __name__ == "__main__":
    main()
