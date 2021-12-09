import functools


def read():
    with open("input.txt") as file:
        bits = []
        for line in file.readlines():
            bits.append(line[:-1])

        return bits


def get_gamma_rate(bits):
    counts = [0 for _ in range(len(bits[0]))]

    for line in bits:
        for i, c in enumerate(line):
            if c == '1':
                counts[i] += 1

    gamma_rate = ""

    for count in counts:
        if count >= len(bits) / 2:
            gamma_rate += "1"
        else:
            gamma_rate += "0"

    return gamma_rate


def get_epsilon_rate(gamma_rate):
    epsilon_rate = ""

    for c in gamma_rate:
        if c == '0':
            epsilon_rate += '1'
        else:
            epsilon_rate += '0'

    return epsilon_rate


def get_decimal_num(bit_str):
    num = 0
    for i, bit in enumerate(bit_str[::-1]):
        if bit == '1':
            num += 2 ** int(i)

    return num


def get_rating(all_bits, get_reference):
    bits_left = [bit for bit in all_bits]
    ptr = 0

    while len(bits_left) > 1:
        reference = get_reference(bits_left)
        bits_left = [bits for bits in bits_left if bits[ptr] == reference[ptr]]
        ptr += 1

    return bits_left[0]


def main():
    bits = read()
    print(bits)

    gamma_rate = get_gamma_rate(bits)
    gamma_rate_decimal = get_decimal_num(gamma_rate)
    print(f"Gamma rate: {gamma_rate} aka {gamma_rate_decimal}")

    epsilon_rate = get_epsilon_rate(gamma_rate)
    epsilon_rate_decimal = get_decimal_num(epsilon_rate)
    print(f"Epsilon rate: {epsilon_rate} aka {epsilon_rate_decimal}")

    print(f"Answer one: {gamma_rate_decimal * epsilon_rate_decimal}")

    generator_rating = get_rating(bits, get_gamma_rate)
    generator_rating_decimal = get_decimal_num(generator_rating)
    print(f"CO2 generator rate: {generator_rating} aka {generator_rating_decimal}")

    scrubber_rating = get_rating(bits, lambda bits_left: get_epsilon_rate(get_gamma_rate(bits_left)))
    scrubber_rating_decimal = get_decimal_num(scrubber_rating)
    print(f"CO2 generator rate: {scrubber_rating} aka {scrubber_rating_decimal}")

    print(f"Answer two: {scrubber_rating_decimal * generator_rating_decimal}")


if __name__ == "__main__":
    main()
