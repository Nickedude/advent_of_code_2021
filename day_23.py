import heapq
from copy import deepcopy
from functools import lru_cache

COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


HALLWAY_X_MAX = 12
HALLWAY_X_MIN = 0
HALLWAY_Y = 1

NUM_AMPHIPODS = 0
Y_MAX = 0
HOMES = None
GOAL = None


def read():
    global Y_MAX, NUM_AMPHIPODS, HOMES, GOAL
    positions = dict()
    types = ["A", "B", "C", "D"]

    with open("input.txt", "r") as file:
        for i, line in enumerate(file.readlines()):
            if i <= 1:
                continue

            if not any([type_ in line for type_ in types]):
                break

            # Remove newlines
            line = line.rstrip("\n")

            for j, char in enumerate(line):
                if char in {"#", " "}:  # Skip walls and empty space
                    continue

                if char not in positions:
                    positions[char] = list()

                positions[char].append((j, i))

    NUM_AMPHIPODS = len(positions["A"])
    Y_MAX = 2 + NUM_AMPHIPODS
    HOMES = get_homes()
    GOAL = get_id(HOMES)

    # Sanity check positions
    all_homes = {pos for type_ in HOMES for pos in HOMES[type_]}

    for type_ in positions:
        for pos in positions[type_]:
            assert pos in all_homes, f"{pos} not in {all_homes}"

    return positions


def get_homes():
    homes = {}
    x = 1
    y_start = 2

    for type_ in ["A", "B", "C", "D"]:
        x += 2
        homes[type_] = set()
        for y in range(y_start, y_start + NUM_AMPHIPODS):
            homes[type_].add((x, y))

    return homes


def print_state(positions):
    reverse_positions = {pos: type_ for type_ in positions for pos in positions[type_]}
    print("#" * (HALLWAY_X_MAX + 1))
    row = "#"

    for x in range(HALLWAY_X_MIN + 1, HALLWAY_X_MAX):
        pos = (x, HALLWAY_Y)
        if pos in reverse_positions:
            row += reverse_positions[pos]
        else:
            row += "."

    row += "#"
    print(row)

    for i in range(1, Y_MAX - 1):
        row = ""

        for x in range(HALLWAY_X_MIN, HALLWAY_X_MAX):
            if x < 2 or x > HALLWAY_X_MAX - 3:
                if i == 1:
                    row += "#"
                else:
                    row += " "

                continue

            pos = (x, HALLWAY_Y + i)

            if pos in reverse_positions:
                row += reverse_positions[pos]
            else:
                if x % 2 == 0:
                    row += "#"
                else:
                    row += "."
        row += "#"
        print(row)

    print("  " + "#" * 9 + "  ")
    print("------------------------------------------")


def is_done(positions):
    # We're done if all types are at one of their home positions.
    for type_ in positions:
        for pos in positions[type_]:
            if pos not in HOMES[type_]:
                return False

    return True


def can_move_into_target_room(type_, positions):
    target_room = HOMES[type_]

    for other_type in positions:
        if other_type == type_:  # Same type can be in the room
            continue

        for other_pos in positions[other_type]:
            if other_pos in target_room:
                return False

    return True


def can_move_across_hallway(x, x_room, occupied):
    step = 1 if x_room > x else -1

    for x_check in range(x + step, x_room + step, step):
        if (x_check, HALLWAY_Y) in occupied:  # Can't move to room because is blocked
            return False

    return True


def get_hallway_moves(type_, x, step, occupied, prior_cost):
    cost = prior_cost + COSTS[type_]  # One step to get into hallway
    end = HALLWAY_X_MIN if step < 0 else HALLWAY_X_MAX
    moves = []

    for x_new in range(x + step, end, step):  # Slide to the left
        cost += COSTS[type_]

        if (x_new, HALLWAY_Y) in occupied:
            break

        if x_new in get_room_xs():  # Can't stop outside a room
            continue

        moves.append((x_new, HALLWAY_Y, cost))

    return moves


def get_upward_moves(type_, x, y, occupied):
    y_new = y
    cost = 0

    while (y_new - 1) > HALLWAY_Y:
        if (x, y_new - 1) in occupied:
            return []  # Blocked from above

        y_new -= 1
        cost += COSTS[type_]

    assert y_new == (HALLWAY_Y + 1)  # Just outside hallway

    moves = []
    moves.extend(get_hallway_moves(type_, x, 1, occupied, cost))
    moves.extend(get_hallway_moves(type_, x, -1, occupied, cost))
    return moves


@lru_cache
def get_room_xs():
    return {pos[0] for type_ in HOMES for pos in HOMES[type_]}


@lru_cache
def get_all_rooms():
    return {pos for type_ in HOMES for pos in HOMES[type_]}


def get_moves(pos, type_, occupied, positions):
    moves = []
    x, y = pos

    if pos in get_all_rooms():  # Currently in a room
        if pos not in HOMES[type_]:  # Not in home - move out
            return get_upward_moves(type_, x, y, occupied)

        # At it's home
        if not can_move_into_target_room(type_, positions):
            # Home contains amphipods of the wrong type -> move out
            return get_upward_moves(type_, x, y, occupied)

        # Room contains amphipods of the same type -> move down
        y_new = y

        while y_new + 1 < Y_MAX:
            if (x, y_new + 1) in occupied:
                break

            y_new += 1

        if y != y_new and y_new < Y_MAX and (x, y_new) not in occupied:
            return [(x, y_new, COSTS[type_])]

        return []

    else:  # Currently in the hallway, will only move into it's room
        if can_move_into_target_room(type_, positions):
            x_room = list(HOMES[type_])[0][0]

            if can_move_across_hallway(x, x_room, occupied):
                cost = abs(x_room - x) * COSTS[type_]

                y_new = HALLWAY_Y + 1
                cost += COSTS[type_]

                while (y_new + 1) < Y_MAX:
                    if (x_room, y_new + 1) in occupied:
                        break

                    y_new += 1
                    cost += COSTS[type_]

                moves.append((x_room, y_new, cost))

    return moves


def get_id(positions):
    key = ""
    for type_ in sorted(positions.keys()):
        key += f"{type_}:"
        for pos in sorted(positions[type_]):
            key += f"{pos},"

        key += "."

    return key


class State:
    def __init__(self, cost, positions):
        self.cost = cost
        self.predicted_remaining_cost = heuristic(positions)
        self.positions = positions

    def __lt__(self, other):
        return self.get_predicted_cost() < other.get_predicted_cost()

    def get_predicted_cost(self):
        return self.cost + self.predicted_remaining_cost

    def get_id(self):
        return get_id(self.positions)

    def __repr__(self):
        return f"{self.cost}, {self.predicted_remaining_cost}, {self.positions}"


def heuristic(positions):
    h = 0

    for type_ in positions:
        x_home, _ = list(HOMES[type_])[0]
        for x, y in positions[type_]:
            h += COSTS[type_] * abs(x_home - x)

            if x != x_home:  # Needs to walk vertically as well
                y_diff = 1  # At least one step down from hallway
                y_diff += abs(HALLWAY_Y - y)  # Distance to hallway, will be zero if in hallway
                h += COSTS[type_] * y_diff

    return h


def a_star(positions):
    frontier = [State(0, positions)]
    costs = dict()
    num_visited = 0
    predecessors = {}
    step = 0

    while frontier:
        node = heapq.heappop(frontier)
        cost = node.cost
        positions = node.positions
        id_ = node.get_id()
        step += 1

        if (step % 10000) == 0:
            print(step, node.cost, node.get_predicted_cost(), len(frontier), flush=True)

        if id_ == GOAL:
            current = node
            while current in predecessors:
                print(current.cost)
                print_state(current.positions)
                current = predecessors[current]
            print(f"Done! Cost is: {cost}")
            print(f"Number of nodes visited: {num_visited}")
            return

        if cost < costs.get(id_, float("inf")):
            num_visited += 1
            costs[id_] = cost

            occupied = {pos for type_ in positions for pos in positions[type_]}

            for type_ in positions:
                for i, pos in enumerate(positions[type_]):
                    moves = get_moves(pos, type_, occupied, positions)

                    for x_new, y_new, move_cost in moves:
                        new_positions = deepcopy(positions)
                        new_positions[type_][i] = (x_new, y_new)

                        new_cost = cost + move_cost
                        new_state = State(new_cost, new_positions)

                        existing_cost = costs.get(new_state.get_id(), float("inf"))

                        if new_cost < existing_cost:
                            predecessors[new_state] = node
                            heapq.heappush(frontier, new_state)


def main():
    import time
    start = time.time()

    positions = read()
    print_state(positions)
    a_star(positions)

    print(f"Runtime: {time.time() - start}")


if __name__ == "__main__":
    main()
