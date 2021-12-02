def main():
    with open("input.txt") as file:
        measurements = file.readlines()

    measurements = list(map(lambda s: int(s[:-1]), measurements))
    num_increase = 0

    for i in range(1, len(measurements)):
        if measurements[i] > measurements[i-1]:
            num_increase += 1

    print(f"First answer: {num_increase}")

    num_increase = 0

    for i in range(3, len(measurements)):
        if sum(measurements[i-2:i+1]) > sum(measurements[i-3:i]):
            num_increase += 1

    print(f"Second answer: {num_increase}")

if __name__ == "__main__":
    main()

