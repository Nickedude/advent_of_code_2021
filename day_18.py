import math
from copy import deepcopy


class SnailFishNumber:

    def __init__(self, left, right, parent):
        """Constructor.

        Creates a snailfish number that holds two sub-numbers that are either ints or other
        snailfish numbers.
        """
        self.left = left
        self.right = right
        self.parent = parent

        self._set_parent(self.left)
        self._set_parent(self.right)

    def __repr__(self):
        left_repr = str(self.left) if isinstance(self.left, int) else self.left.__repr__()
        right_repr = str(self.right) if isinstance(self.right, int) else self.right.__repr__()
        return "[" + left_repr + "," + right_repr + "]"

    def __add__(self, other):
        new_snailfish_number = SnailFishNumber(deepcopy(self), deepcopy(other), None)
        self._reduce(new_snailfish_number)
        return new_snailfish_number

    def _set_parent(self, other):
        if isinstance(other, SnailFishNumber):
            other.parent = self

    def get_child(self, direction):
        if direction == "left":
            return self.left
        elif direction == "right":
            return self.right

        raise NotImplementedError(f"Can't get child in direction {direction}")

    def set_child(self, direction, child):
        if direction == "left":
            self.left = child
        elif direction == "right":
            self.right = child
        else:
            raise NotImplementedError(f"Can't set child in direction {direction}")

    def magnitude(self):
        left_magnitude = self.left if isinstance(self.left, int) else self.left.magnitude()
        right_magnitude = self.right if isinstance(self.right, int) else self.right.magnitude()
        return 3 * left_magnitude + 2 * right_magnitude

    @staticmethod
    def replace(child, parent, new_child):
        if parent.left == child:
            parent.left = new_child
        elif parent.right == child:
            parent.right = new_child
        else:
            raise ValueError(f"Child {child} can't be found in parent {parent}")

    @staticmethod
    def _reduce(snailfish_number):
        reduced = False

        while not reduced:
            exploded = SnailFishNumber._explode(snailfish_number)

            if not exploded:
                split = SnailFishNumber._split(snailfish_number)
                reduced = not exploded and not split

    @staticmethod
    def _explode(number) -> bool:
        return SnailFishNumber._explode_helper(number, 0)

    @staticmethod
    def _explode_helper(number, depth):
        if isinstance(number, int):
            return False

        if depth == 4:
            assert isinstance(number.left, int)
            assert isinstance(number.right, int)
            SnailFishNumber._explode_left(number)
            SnailFishNumber._explode_right(number)
            SnailFishNumber.replace(number, number.parent, 0)

            return True

        found_left = SnailFishNumber._explode_helper(number.left, depth + 1)

        if found_left:
            return True

        return SnailFishNumber._explode_helper(number.right, depth + 1)

    @staticmethod
    def _explode_left(number):
        SnailFishNumber._explode_direction(number, left=True)

    @staticmethod
    def _explode_right(number):
        SnailFishNumber._explode_direction(number, left=False)

    @staticmethod
    def _explode_direction(exploding_number, left: bool):
        exploding_direction = "left" if left else "right"
        opposite_direction = "right" if left else "left"

        previous = exploding_number
        current = exploding_number.parent

        # Find parent with a child in the exploding direction (e.g left) that's not the exploding
        # number itself. This child will contain the number that should be incremented.
        while current is not None and current.get_child(exploding_direction) == previous:
            previous = current
            current = current.parent

        # Check if we reached the root of the tree - if so there's no number to add to
        if current is None:
            return

        # If the child in the exploding durection is a number we're done
        if isinstance(current.get_child(exploding_direction), int):
            num = current.get_child(exploding_direction)
            num += exploding_number.get_child(exploding_direction)
            current.set_child(exploding_direction, num)
            return

        # Otherwise, traverse the tree one step down in the exploding direction.
        current = current.get_child(exploding_direction)

        # Then, go in the opposite direction until a number is found
        while not isinstance(current.get_child(opposite_direction), int):
            current = current.get_child(opposite_direction)

        num = current.get_child(opposite_direction)
        num += exploding_number.get_child(exploding_direction)
        current.set_child(opposite_direction, num)

    @staticmethod
    def _split(number):
        return SnailFishNumber._split_helper(number, number.parent)

    @staticmethod
    def _split_helper(number, parent) -> bool:
        if isinstance(number, int):
            if number < 10:
                return False

            left = math.floor(number / 2.0)
            right = math.ceil(number / 2.0)
            new_child = SnailFishNumber(left, right, parent)
            SnailFishNumber.replace(number, parent, new_child)
            return True

        assert isinstance(number, SnailFishNumber)
        split_left = SnailFishNumber._split_helper(number.left, number)

        if split_left:
            return True

        return SnailFishNumber._split_helper(number.right, number)


def parse_number(line: str) -> SnailFishNumber:
    if line.count(",") == 0:  # Base case - string is just a number
        return int(line)

    assert line[0] == "["
    assert line[-1] == "]"
    line = line[1:-1]  # Drop outer parentheses

    if line[0] == "[":  # Left part is SnailFishNumber - find where to split by counting parentheses
        parenthesis_count = 1
        ptr = 1

        while parenthesis_count > 0:
            if line[ptr] == "[":
                parenthesis_count += 1
            elif line[ptr] == "]":
                parenthesis_count -= 1

            ptr += 1

    else:
        ptr = 0
        while line[ptr] != ",":
            ptr += 1

    left = line[0:ptr]
    right = line[ptr + 1:]

    return SnailFishNumber(parse_number(left), parse_number(right), None)


def read():
    numbers = []

    with open("input.txt", "r") as file:
        for line in file.readlines():
            line = line.rstrip("\n")
            numbers.append(parse_number(line))

    return numbers


def main():
    numbers = read()
    sum_of_numbers = numbers[0]

    for num in numbers[1:]:
        sum_of_numbers = sum_of_numbers + num

    print(f"Magnitude: {sum_of_numbers.magnitude()}")

    max_sum = 0
    numbers = read()

    for fst in numbers:
        for snd in numbers:
            fst_sum = fst + snd
            snd_sum = snd + fst

            max_sum = max(max_sum, fst_sum.magnitude(), snd_sum.magnitude())

    print(f"Max sum: {max_sum}")


if __name__ == "__main__":
    main()
