from copy import deepcopy


def read():
    with open("input.txt", "r") as file:
        sequences = []

        for line in file.readlines():
            sequence, output = line.split("|")
            output = output[:-1]

            def parse(l):
                l = l.split(" ")
                return [x for x in l if x]

            sequences.append((parse(sequence), parse(output)))

        return sequences


def solve(sequences):
    count = 0
    unique_lengths = {2, 4, 3, 7}

    for _, output in sequences:
        for output_sequence in output:
            if len(output_sequence) in unique_lengths:
                count += 1

    print(count)


def get_all_chars():
    return ["a", "b", "c", "d", "e", "f", "g"]


def solve_2(sequences):
    count = 0
    numbers = {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg"
    }

    lengths = {len(s): i for (i, s) in numbers.items()}
    unique_lengths = {l: i for (l, i) in lengths.items() if l in [2, 4, 3, 7]}

    for input_, output in sequences:
        print(input_)
        alternatives = {char: get_all_chars() for char in get_all_chars()}

        for input_sequence in input_:
            length = len(input_sequence)

            if length in unique_lengths:
                target = unique_lengths[length]

                for char in numbers[target]:
                    new_alternatives = list(input_sequence)
                    if len(alternatives[char]) > len(new_alternatives):
                        alternatives[char] = new_alternatives

        global MEMORY
        MEMORY = {}
        ans = backtrack(input_, alternatives, numbers)
        print(ans)

        k = ""

        for o in output:
            p = decode(o, ans, numbers)
            k += str(p)

        k = int(k)
        print(k)
        count += k

    print(count)


def decode(input_sequence, alternatives, numbers):
    decoded = []
    alternatives = {v[0]: k for (k, v) in alternatives.items()}
    for char in input_sequence:
        decoded.append(alternatives[char])

    decoded = sorted(decoded)
    decoded = "".join(decoded)

    for num, seq in numbers.items():
        if decoded == "".join(sorted(seq)):
            return num

    return None


MEMORY = {}

def hash_(alternatives):
    hash_str = ""

    for char in alternatives:
        hash_str += f"{char}-"
        for alt in alternatives[char]:
            hash_str += alt

        hash_str += "."

    return hash_str

def backtrack(input_, alternatives, numbers):
    alt_values = list(alternatives.values())
    hash_value = hash_(alternatives)
    if hash_value in MEMORY:
        return MEMORY[hash_value]

    # Base case
    if all([len(alt) == 1 for alt in alt_values]):
        flat_values = [alt[0] for alt in alt_values]
        if len(flat_values) != len(set(flat_values)):  # Not all alternatives unique
            MEMORY[hash_value] = None
            return None

        seen_numbers = []
        for input_sequence in input_:
            decoded = decode(input_sequence, alternatives, numbers)
            seen_numbers.append(decoded)

        seen_numbers = set(seen_numbers)
        all_numbers = set(list(range(0, 10)))
        if seen_numbers == all_numbers:
            MEMORY[hash_value] = alternatives
            return alternatives

    # Recursive case
    for char in alternatives:
        if len(alternatives[char]) == 1:
            continue

        for alt in alternatives[char]:
            fixed_alternatives = deepcopy(alternatives)
            fixed_alternatives[char] = [alt]
            solution = backtrack(input_, fixed_alternatives, numbers)

            if solution is not None:
                MEMORY[hash_value] = solution
                return solution

    MEMORY[hash_value] = None
    return None


def main():
    sequences = read()
    solve(sequences)
    solve_2(sequences)


if __name__ == "__main__":
    main()
