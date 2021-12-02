def main():
    with open("input.txt") as file:
        commands = file.readlines()

    commands = list(map(lambda s: s[:-1].split(" "), commands))
    commands = list(map(lambda command: (command[0], int(command[1])), commands)) 

    x, y_1, y_2, aim = 0, 0, 0, 0

    for direction, delta in commands:
        if "forward" in direction:
            x += delta
            y_2 += aim * delta
        elif "up" in direction:
            y_1 -= delta
            aim -= delta
        elif "down" in direction:
            y_1 += delta
            aim += delta
        else:
            raise ValueError(direction)

    print(f"First answer: {x * y_1}")
    print(f"First answer: {x * y_2}")


if __name__ == "__main__":
    main()
