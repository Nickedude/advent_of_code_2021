def solve_one(y_end):
    y_vel = -y_end - 1  # When reaching y=0 velocity will be -y_end
    y_best = int(y_vel * (y_vel + 1) / 2)  # Sum from 1 to n
    print(y_best)


def throw(ys, xs, x_start, x_end, y_start, y_end):
    solutions = []

    for y_vel in ys:
        for x_vel in xs:
            x_pos, y_pos = 0, 0
            curr_xvel = x_vel
            curr_yvel = y_vel

            while x_pos <= x_end and y_pos >= y_end:

                if x_start <= x_pos <= x_end and y_end <= y_pos <= y_start:
                    solutions.append((x_vel, y_vel))
                    break

                x_pos += curr_xvel
                y_pos += curr_yvel
                curr_yvel -= 1
                if curr_xvel > 0:
                    curr_xvel -= 1
                elif curr_xvel < 0:
                    curr_xvel += 1

    return solutions


def solve_two():
    y_start = -73
    y_end = -98
    y_cands = list(range(y_end, -y_end + 1))
    x_start = 137
    x_end = 171
    x_cands = list(range(1, x_end+1))

    print(y_cands)
    print(x_cands)

    solutions = throw(y_cands, x_cands, x_start, x_end, y_start, y_end)
    print(len(solutions))


def read():
    with open("input.txt", "r") as file:
        line = file.readline()
        line = line.lstrip("target area: ")
        xstr, ystr = line.split(", ")
        x_start, x_end = xstr.split("..")
        x_start = x_start[2:]
        y_end, y_start = ystr.split("..")
        y_end = y_end[2:]

    return int(x_start), int(x_end), int(y_start), int(y_end)


def main():
    x_start, x_end, y_start, y_end = read()
    solve_one(y_end)
    solve_two()


if __name__ == "__main__":
    main()
