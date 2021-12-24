from concurrent.futures import ThreadPoolExecutor

import numpy as np


def parse(coordinate_range):
    coordinate_range = coordinate_range[2:]
    start, end = coordinate_range.split("..")
    return [int(start), int(end)]


def read():
    with open("input.txt", "r") as file:
        instructions = []

        for line in file.readlines():
            line = line.rstrip("\n")
            action, coordinates = line.split(" ")
            assert action in {"on", "off"}
            action = 1 if action == "on" else 0

            coordinates = coordinates.split(",")
            coordinates = list(map(parse, coordinates))
            instructions.append((action, coordinates))

        return instructions


def translate_ranges(ranges, cube_coordinates, cube_size):
    new_ranges = []

    for coordinate_range, cube_coordinate in zip(ranges, cube_coordinates):
        assert len(coordinate_range) == 2
        new_coordinate_range = []

        for coordinate in coordinate_range:
            coordinate += cube_size // 2

            if coordinate < 0:
                coordinate = 0

            if coordinate > cube_size - 1:
                coordinate = cube_size - 1

            new_coordinate_range.append(coordinate)

        new_ranges.append(new_coordinate_range)

    return new_ranges


def is_not_in_range_old(coordinate_ranges, cube_coordinates, cube_size):
    for (start, end), cube_coordinate in zip(coordinate_ranges, cube_coordinates):
        cube_max = cube_coordinate + cube_size // 2
        cube_min = cube_coordinate - cube_size // 2

        if start > cube_max or end < cube_min:
            return True

    return False


def is_not_in_range(ranges):
    for start, end in ranges:
        if start > 50 or end < -50:
            return True

    return False


def count_lit_cubes(instructions, cube_coordinates, cube_size):
    grid = np.zeros((cube_size, cube_size, cube_size), dtype=int)
    num_on = 0

    for action, ranges in instructions:
        if is_not_in_range_old(ranges, cube_coordinates, cube_size):
            continue

        ranges = translate_ranges(ranges, cube_coordinates, cube_size)

        [(x_start, x_end), (y_start, y_end), (z_start, z_end)] = ranges
        grid[x_start:x_end + 1, y_start:y_end + 1, z_start:z_end + 1] = action

        delta = grid.sum() - num_on
        assert delta <= (x_end - x_start + 1) * (y_end - y_start + 1) * (z_end - z_start + 1)
        num_on = grid.sum()

    return num_on


def get_intersection(fst_cuboid, snd_cuboid):
    intersection = 1

    for (fst_start, fst_end), (snd_start, snd_end) in zip(fst_cuboid, snd_cuboid):
        if fst_start <= snd_start <= fst_end <= snd_end:    # s1----s2++++e1----e2
            width = fst_end - snd_start + 1

        elif snd_start <= fst_start <= snd_end <= fst_end:  # s2----s1++++e2----e1
            width = snd_end - fst_start + 1

        elif fst_start <= snd_start <= snd_end <= snd_start: # s1----s2++++e2----e1
            width = snd_end - snd_start + 1

        elif snd_start <= fst_start <= fst_end <= snd_end: # s2----s1++++e1----s1
            width = fst_end - fst_start + 1

        else:
            width = 0
        intersection *= width

    return intersection

def count_lit_cubes_fast(instructions, initialize: bool = False):
    cuboids_and_counts = []

    for action, new_cuboid in instructions:
        if initialize and is_not_in_range(new_cuboid):
            continue

        new_num_lit_cubes = 1

        for start, end in new_cuboid:
            length = end - start + 1
            new_num_lit_cubes *= length

        for i, (cuboid, num_lit_cubes) in enumerate(cuboids_and_counts):
            intersection = get_intersection(new_cuboid, cuboid)

            if intersection > 0:
                if action == 0:  # Off
                    cuboids_and_counts[i][1] = num_lit_cubes - intersection
                elif action == 1:  # On
                    new_num_lit_cubes -= intersection

        if action == 1 and new_num_lit_cubes > 0:
            cuboids_and_counts.append([new_cuboid, new_num_lit_cubes])

    total_num_lit_cubes = sum([count for _, count in cuboids_and_counts])
    return total_num_lit_cubes


def solve_two(instructions):
    size = 0
    step = 1001

    for _, coordinate_ranges in instructions:
        for start, end in coordinate_ranges:
            current_size = end - start + 1  # Add 1 to include the origin
            size = max(size, current_size)

    count = 0

    cubes = []

    for x in range(0, size, step):
        for y in range(0, size, step):
            for z in range(0, size, step):
                cubes.append([x, y, z])

    print(f"Number of cubes to process: {len(cubes)}")

    non_empty_cubes = []

    for i, cube in enumerate(cubes):
        in_range = False

        if i % 100_000 == 0:
            print(f"Processing cube {i}/{len(cubes)}")

        for action, ranges in instructions:
            if is_not_in_range(ranges, cube, step):
                continue

            in_range = True
            break

        if in_range:
            non_empty_cubes.append(cube)

    del cubes
    print(f"Number of non empty cubes to process: {len(non_empty_cubes)}")

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = []
        for cube in non_empty_cubes:
            futures.append(pool.submit(count_lit_cubes, instructions, cube, step))

        for i, future in enumerate(futures):
            if i % 5 == 0:
                print(f"Processed {i}/{len(non_empty_cubes)} cubes", flush=True)

            count += future.result()


def solve_one(instructions):
    cube_size = 101  # -50 to 50, including 0 gives 101 coordinates
    cube_coordinates = [0, 0, 0]
    count = count_lit_cubes(instructions, cube_coordinates, cube_size)
    print(f"Sum of grid is: {count}")


def main():
    instructions = read()
    solve_one(instructions)
    #solve_two(instructions)


if __name__ == "__main__":
    main()
