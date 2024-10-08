import collections
import logging
import numpy as np
from sympy import Eq, symbols

logger = logging.getLogger(__name__)

b = [
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"],
]

"""
Also need to keep track of if it's visited or not, and if it's visited then to stop because we cant revisit a square
"""


class KnightsMoves:

    def possible_moves(self, curr: tuple[int, int]) -> list[tuple[int, int]]:
        """
        For a given position b[x][y] you can do the following moves:

        b[x - 2][y - 1]
        b[x - 2][y + 1]
        b[x + 2][y - 1]
        b[x + 2][y + 1]
        b[x - 1][y - 2]
        b[x - 1][y + 1]
        b[x + 1][y - 2]
        b[x + 1][y + 2]

        assuming that the new indices i, j satisfy 0 < i, j < 6
        """
        x = curr[0]
        y = curr[1]

        possible_moves = [(x - 2, y - 1),
                          (x - 2, y + 1),
                          (x + 2, y - 1),
                          (x + 2, y + 1),
                          (x - 1, y - 2),
                          (x - 1, y + 1),
                          (x + 1, y - 2),
                          (x + 1, y + 2)]

        result = [point for point in possible_moves if point[0] >= 0 and point[0] < 6 and point[1] >= 0 and point[1] < 6
                  ]

        return result

    def find_paths(self, board: list[list[str]], start: tuple[int, int], end: tuple[int, int], max_len: int = 8):
        """
        Finds all possible paths between start and end using only knights moves.
        """
        q: collections.deque[tuple[int, int]] = collections.deque()

        visited = np.zeros((len(board), len(board)))

        logger.debug(f"Visited {start}")
        visited[start[0]][start[1]] = True
        q.append([start])

        paths = []
        while q:
            logger.debug("start iteration")
            path = q.popleft()

            if len(path) > max_len:
                return (paths)

            curr = path[-1]

            if curr == end:
                logger.info("Reached the end.")
                paths.append(path)

            possible_moves = self.possible_moves(curr)

            logger.debug(f"""Possible moves from {curr}:
{possible_moves}
                         """)
            for next in possible_moves:

                logger.debug(f"curr path: {path}")
                visited = next in path

                logger.debug(f"Consider {next}, visited: {visited}")
                if not visited:

                    logger.debug(f"{next} not visited")

                    # if next != end:
                    #     visited[next[0]][next[1]] = True

                    new_path = list(path)
                    new_path.append(next)

                    q.append(new_path)

            # logger.debug(f"visited:\n{visited}")
            logger.debug("end iteration")

        logger.debug(f"visited:\n{visited}")
        return paths

    def calculate_score(self, path: list[tuple[int, int]]):
        """
        Given a path, calculate the score
        """
        curr = path.pop(0)

        a, b, c = symbols("a b c")

        score = Eq(a)

        for next in path:
            next_letter = b[curr[0]][curr[1]]

            m = {
                "A": a,
                "B": b,
                "C": c
            }

            next_letter = m[next_letter]

    def flip_path(self, path: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return [(x, 6 - y) for x, y in path]


if __name__ == "__main__":
    logging.basicConfig(filename=f'example.log',
                        encoding='utf-8', level=logging.DEBUG)
    """
    First we start with calculating the different paths between the start and end.
    """

    paths = KnightsMoves().find_paths(board=b, start=(0, 0), end=(5, 5))

    print(paths)

    """
    We need to also find the paths from (0,6) to (6,0), but the thing is all of our solutions are valid from any corner to the corner across.
    So all we need to do is rotate each path and then we have a valid solution for (0,6) and (6,0)
    """

    """
    Need to calculate the formulas for the scores
    """

    """Once we've got a set of paths, then we've essentially got an optimization problem. 

    Minimize: A + B + C 
    given:

    A, B, C > 0 
    path_1 = 2024
    path 2 = 2024
    """
