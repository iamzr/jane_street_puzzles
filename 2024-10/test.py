import datetime
import itertools
import logging
from pathlib import Path
import pprint
from typing import NamedTuple

import numpy as np
from sympy import lambdify, symbols

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)

logs_dir = Path(__name__).parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=logs_dir / f"{datetime.datetime.now()}.log",
    filemode="a+",
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        _indicies_map = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
        }

        x = _indicies_map[self.x]
        y = self.y + 1

        return f"{x}{y}"


board = [
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
]


class TreeNode:
    def __init__(self, point):
        self.point = point
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"TreeNode(point={self.point}, children={self.children})"


def get_neighbors(point):
    """Return valid neighbors for a given point on the board."""
    x, y = point

    possible_moves = [
        (x - 2, y - 1),
        (x - 2, y + 1),
        (x + 2, y - 1),
        (x + 2, y + 1),
        (x - 1, y - 2),
        (x - 1, y + 2),
        (x + 1, y - 2),
        (x + 1, y + 2),
    ]

    n = 6

    result = [
        point for point in possible_moves if x >= 0 and x < n and y >= 0 and y < n
    ]

    return result


scores_1 = {}
scores_2 = {}


def calculate_score(path: list[Point]):
    """
    Given a path, calculate the score
    """
    curr = path[0]

    a, b, c = symbols("a b c")

    score = 0

    m = {"A": a, "B": b, "C": c}

    current_letter = "A"
    for next in path:
        logger.debug(f"next {next}")
        next_letter = board[next.y][next.x]

        logger.debug(f"{curr} {current_letter} -> {next} {m[next_letter]}")
        if next_letter != current_letter:
            logger.debug(f"multiply by {m[next_letter]}")
            score *= m[next_letter]
        else:
            logger.debug(f"add {m[next_letter]}")
            score += m[next_letter]

        current_letter = next_letter

    logger.debug(score)
    return score


def handle_path(path):
    path = [Point(x, y) for x, y, in path]
    score = calculate_score(path=path)
    if score not in scores_1:
        scores_1[score] = path

    alt_path = [Point(x, 6 - 1 - y) for x, y in path]
    score = calculate_score(path=alt_path)
    if score not in scores_2:
        scores_2[score] = alt_path


def find_paths(
    start,
    end,
    board,
    max_length,
    current_path=None,
    visited=None,
    depth=0,
    all_paths=None,
):
    """
    Perform DFS to find all paths from start to end within a max length, without constructing a tree.

    Parameters:
    - start: The starting point (tuple).
    - end: The endpoint (tuple).
    - board: The 2D board array.
    - max_length: Maximum allowed path length.
    - current_path: The path being built as a list of points.
    - visited: Set of visited points for the current path.
    - depth: Current depth of recursion.
    - all_paths: List to store all complete paths from start to end.

    Returns:
    - List of all paths from start to end point.
    """
    if current_path is None:
        current_path = []
    if visited is None:
        visited = set()
    if all_paths is None:
        all_paths = []

    # Add the current point to the path and mark as visited
    current_path.append(start)
    visited.add(start)

    # If we have reached the end point, add the path to all_paths
    if start == end:
        all_paths.append(current_path.copy())
        handle_path(current_path)
    elif depth < max_length:  # Continue exploring if max depth not reached
        for neighbor in get_neighbors(start):
            if neighbor not in visited:
                find_paths(
                    neighbor,
                    end,
                    board,
                    max_length,
                    current_path,
                    visited,
                    depth + 1,
                    all_paths,
                )

    # Backtrack: remove the current point from path and visited set
    current_path.pop()
    visited.remove(start)

    return all_paths


def _convert_path_to_output_format(path: list[Point]) -> list[str]:
    return [str(point) for point in path]


def solution_str(
    a: int, b: int, c: int, path_1: list[Point], path_2: list[Point]
) -> str:
    s = [str(a), str(b), str(c)]
    s.extend(_convert_path_to_output_format(path=path_1))
    s.extend(_convert_path_to_output_format(path=path_2))

    return ",".join(s)


def lambdify_score(score):
    a, b, c = symbols("a b c")
    return lambdify([a, b, c], score)


# Define start and end points
start_point = (0, 0)
end_point = (5, 5)

min_path_length = 5
max_path_length = 7  # Maximum path length

# Generate the tree
# tree_root = find_paths(start_point, end_point, board, min_path_length, max_path_length)
all_paths = find_paths(start_point, end_point, board, max_path_length)

logger.info(
    f"""Score functions for paths from (0,0) to (5,5):
    
{pp.pformat(scores_1)}
"""
)
logger.info(
    f"""Score functions for paths from (0,5) to (5, 0):
    
{pp.pformat(scores_2)}
"""
)


def check_scores(scores: dict):
    result = {}
    for score in scores:
        score_func = lambdify_score(score=score)

        for a, b, c in itertools.product(range(1, 50), range(1, 50), range(1, 50)):
            s = score_func(a, b, c)

            if s == 2024 and result.get((a, b, c)) is None:
                result[(a, b, c)] = scores[score]

    return result


results_1 = check_scores(scores_1)
results_2 = check_scores(scores_2)

solutions = results_1.keys() & results_2.keys()

optimal = (np.inf, np.inf, np.inf, "")
for solution in solutions:
    a, b, c = solution
    solution_string = solution_str(
        a=a, b=b, c=c, path_1=results_1[solution], path_2=results_2[solution]
    )
    output = f"""Solution:
For {a=}, {b=}, {c=} where

path_1s: {_convert_path_to_output_format(results_1[solution])}

path_2s: {_convert_path_to_output_format(results_2[solution])}
"""

    print(output)
    logger.debug(output)

    if a + b + c < optimal[0] + optimal[1] + optimal[2]:
        optimal = (a, b, c, solution_string)

logger.info(f"Optimal solution: {optimal[3]}")
