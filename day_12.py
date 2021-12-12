from collections import defaultdict
from typing import Dict, Set


def read():
    graph = defaultdict(set)

    with open("input.txt", "r") as file:
        for edge in file.readlines():
            edge = edge[:-1] if edge[-1] == "\n" else edge
            fst, snd = edge.split("-")
            graph[fst].add(snd)
            graph[snd].add(fst)

    return graph


def solve(graph: Dict[str, Set[str]], can_visit_small_node_twice: bool = False):
    solutions = []
    paths = [["start"]]

    while paths:
        path = paths.pop(0)
        node = path[-1]

        if node == "end":  # End the search when reaching the end node
            solutions.append(path)
            continue

        for neighbor in graph[node]:
            if neighbor == "start":  # Never visit the start node more than once
                continue

            if can_visit_small_node_twice:
                small_nodes = [n for n in path if n.islower()]
                visited_small_twice = len(set(small_nodes)) != len(small_nodes)
            else:
                visited_small_twice = True

            if neighbor.islower() and neighbor in path and visited_small_twice:
                continue

            paths.append(path + [neighbor])

    return len(solutions)


def main():
    graph = read()
    print(graph)
    print(f"First answer: {solve(graph)}")
    print(f"Second answer: {solve(graph, can_visit_small_node_twice=True)}")


if __name__ == "__main__":
    main()
