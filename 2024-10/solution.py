import itertools
import logging
from typing import NamedTuple, Self

from sympy import lambdify, symbols

logger = logging.getLogger(__name__)


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return self.__str__()

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


class KnightsMoves:
    def __init__(self, board) -> None:
        self.board = board
        self.n = len(board)

    def get_neighbors(self, point):
        """Return valid neighbors for a given point on the board."""
        x, y = point

        possible_moves = [
            Point(x - 2, y - 1),
            Point(x - 2, y + 1),
            Point(x + 2, y - 1),
            Point(x + 2, y + 1),
            Point(x - 1, y - 2),
            Point(x - 1, y + 2),
            Point(x + 1, y - 2),
            Point(x + 1, y + 2),
        ]

        result = [
            point
            for point in possible_moves
            if x >= 0 and x < self.n and y >= 0 and y < self.n
        ]

        return result

    def calculate_score(self, path: list[Point]):
        """Given a path, calculate the score"""
        curr = path[0]

        a, b, c = symbols("a b c")

        score = 0

        m = {"A": a, "B": b, "C": c}

        current_letter = "A"
        for next in path:
            next_letter = self.board[next.y][next.x]

            logger.debug(f"{curr} {current_letter} -> {next} {next_letter}")
            if next_letter != current_letter:
                score *= m[next_letter]
            else:
                score += m[next_letter]

            current_letter = next_letter

        logger.debug(score)
        return score

    def handle_path(self, path, scores_1, scores_2):

        logger.debug(f"Found path: {path}")
        score = self.calculate_score(path=path)
        if score not in scores_1:
            scores_1[score] = path

        alt_path = [Point(x, 6 - 1 - y) for x, y in path]
        logger.debug(f"Found path: {alt_path}")
        score = self.calculate_score(path=alt_path)
        if score not in scores_2:
            scores_2[score] = alt_path

    def find_paths(
        self,
        start,
        end,
        max_length,
        current_path=None,
        visited=None,
        depth=0,
        scores_1=None,
        scores_2=None,
    ):
        if current_path is None:
            current_path = []
        if visited is None:
            visited = set()
        if scores_1 is None:
            scores_1 = {}
        if scores_2 is None:
            scores_2 = {}

        # Add the current point to the path and mark as visited
        current_path.append(start)
        visited.add(start)

        # If we have reached the end point, add the path to all_paths
        if start == end:
            self.handle_path(current_path.copy(), scores_1, scores_2)
        elif depth < max_length:  # Continue exploring if max depth not reached
            for neighbor in self.get_neighbors(start):
                if neighbor not in visited:
                    self.find_paths(
                        neighbor,
                        end,
                        max_length,
                        current_path,
                        visited,
                        depth + 1,
                        scores_1,
                        scores_2,
                    )

        # Backtrack: remove the current point from path and visited set
        current_path.pop()
        visited.remove(start)

        return scores_1, scores_2

    @staticmethod
    def solution_str(
        a: int, b: int, c: int, path_1: list[Point], path_2: list[Point]
    ) -> str:
        s = [str(a), str(b), str(c)]
        s.extend([str(point) for point in path_1])
        s.extend([str(point) for point in path_2])

        return ",".join(s)

    @staticmethod
    def _lambdify_score(score):
        a, b, c = symbols("a b c")
        return lambdify([a, b, c], score)

    def check_scores(self, scores: dict):
        result = {}
        for score in scores:
            score_func = self._lambdify_score(score=score)

            for a, b, c in itertools.product(range(1, 50), range(1, 50), range(1, 50)):
                s = score_func(a, b, c)

                if s == 2024 and result.get((a, b, c)) is None:
                    result[(a, b, c)] = scores[score]

        return result
