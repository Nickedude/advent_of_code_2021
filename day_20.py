import numpy as np

KERNEL_SIZE = 3


def parse(c):
    if c == "#":
        return 1
    elif c == ".":
        return 0

    raise NotImplementedError(f"Can't parse {c}")


def read():
    with open("input.txt", "r") as file:
        enhancement = file.readline().rstrip("\n")
        enhancement = [parse(c) for c in enhancement]

        image = []

        for line in file.readlines():
            line = line.rstrip("\n")

            if not line:
                continue

            line = [parse(c) for c in line]

            image.append(np.array(line))

    return np.array(image), np.array(enhancement)


def pad_width(image, num_zeros_to_pad):
    _, width = image.shape
    return np.vstack((
        np.zeros((num_zeros_to_pad, width)),
        image,
        np.zeros((num_zeros_to_pad, width))
    ))


def pad_height(image, num_zeros_to_pad):
    height, _ = image.shape
    return np.hstack((
        np.zeros((height, num_zeros_to_pad)),
        image,
        np.zeros((height, num_zeros_to_pad))
    ))


def enhance(image, enhancement, step):
    num_to_skip = 1
    height, width = image.shape
    output = np.zeros((height, width)).astype(int)

    if enhancement[0] == 1 and step % 2 == 0:
        output[0, :] = 1
        output[-1, :] = 1
        output[:, 0] = 1
        output[:, -1] = 1

    for i in range(height):
        if i < num_to_skip or i > height - num_to_skip - 1:
            continue
        for j in range(width):
            if j < num_to_skip or j > width - num_to_skip - 1:
                continue

            crop = image[i-1:i+2, j-1:j+2]
            assert (3, 3) == crop.shape
            crop = "".join(map(str, list(crop.flatten())))
            index = int(crop, 2)
            pixel_out = enhancement[index]

            output[i, j] = pixel_out

    return output.astype(int)


def solve(image, enhancement, num_steps):
    num_zeros_to_pad = (KERNEL_SIZE - 1) * num_steps
    padded_image = pad_width(image, num_zeros_to_pad)
    padded_image = pad_height(padded_image, num_zeros_to_pad).astype(int)

    print(f"Enhancing for {num_steps} steps ...")

    for i in range(num_steps):
        if (i % 5) == 0:
            print(f"{i}/{num_steps} steps complete ...")

        padded_image = enhance(padded_image, enhancement, i)

    print(padded_image.sum())


def main():
    image, enhancement = read()
    print(enhancement)
    print(image)
    solve(image, enhancement, num_steps=2)
    solve(image, enhancement, num_steps=50)


if __name__ == "__main__":
    main()
