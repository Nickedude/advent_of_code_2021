from itertools import product


def parse(s):
    return int(s.rstrip("\n").split("position: ")[1])


def read():
    with open("input.txt", "r") as file:
        p1_start_pos = parse(file.readline())
        p2_start_pos = parse(file.readline())

    return p1_start_pos, p2_start_pos


def solve_one(p1_start_pos, p2_start_pos):
    dice = 1
    rolls = 0
    player = 0
    positions = [p1_start_pos, p2_start_pos]
    scores = [0, 0]
    run = True

    while run:
        move = 0

        for i in range(3):
            move += dice
            dice += 1
            rolls += 1

            if dice > 100:
                dice = 1

        move = move % 10  # 10 steps takes the player to the exact same position
        positions[player] += move

        if positions[player] > 10:
            positions[player] -= 10

        score = positions[player]
        scores[player] += score
        player = (player + 1) % 2

        run = all([s < 1000 for s in scores])

    loser = 0 if scores[0] < 1000 else 1
    print(f"First answer: {rolls * scores[loser]}")


def solve_two(p1, p2):
    scores = [0, 0]
    positions = [p1, p2]
    starting_player = 0

    all_moves = list(product([1, 2, 3], repeat=3))
    all_moves = [sum(move) for move in all_moves]
    unique_moves = set(all_moves)
    moves = {move: 0 for move in unique_moves}

    memory = {}

    for move in all_moves:
        moves[move] += 1

    wins = play(starting_player, positions, scores, moves, memory)
    print(f"Second answer: {max(wins)}")


def play(player, positions, scores, moves, memory):
    if any([s >= 21 for s in scores]):  # Game over
        if scores[0] >= 21:
            return [1, 0]
        else:
            return [0, 1]

    identifier = f"{player}-{positions}-{scores}"

    if identifier not in memory:
        next_player = (player + 1) % 2
        wins = [0, 0]

        for num_steps_to_move, count in moves.items():
            new_positions = [p for p in positions]
            new_positions[player] += num_steps_to_move

            if new_positions[player] > 10:  # Wrap around, e.g from 11 -> 1
                new_positions[player] -= 10

            new_scores = [s for s in scores]
            new_scores[player] += new_positions[player]

            wins_from_sub_problem = play(next_player, new_positions, new_scores, moves, memory)

            for i in range(len(wins)):
                wins[i] += wins_from_sub_problem[i] * count

        memory[identifier] = wins

    return memory[identifier]


def main():
    p1_start_pos, p2_start_pos = read()
    print("Starting positions:", p1_start_pos, p2_start_pos)
    solve_one(p1_start_pos, p2_start_pos)
    solve_two(p1_start_pos, p2_start_pos)


if __name__ == "__main__":
    main()
