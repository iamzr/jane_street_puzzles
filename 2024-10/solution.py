import collections
import logging
from typing import NamedTuple, Optional
import numpy as np
from sympy import lambdify, simplify, symbols

logger = logging.getLogger(__name__)


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


class Board:
    def __init__(self, b: list[list[str]]) -> None:
        self.b = b
        self.l = len(self.b)

    def get(self, p: Point):
        return self.b[p.y][p.x]

    def __len__(self):
        return self.l


class KnightsMoves:
    def __init__(self):
        board = [
            ["A", "A", "A", "B", "B", "C"],
            ["A", "A", "A", "B", "B", "C"],
            ["A", "A", "B", "B", "C", "C"],
            ["A", "A", "B", "B", "C", "C"],
            ["A", "B", "B", "C", "C", "C"],
            ["A", "B", "B", "C", "C", "C"],
        ]

        b = Board(b=board)
        self.b = b
        self.n = len(b)

    def possible_moves(self, curr: Point) -> list[Point]:
        """
        For a given position b[x][y] you can do the following moves:

        b[x - 2][y - 1]
        b[x - 2][y + 1]
        b[x + 2][y - 1]
        b[x + 2][y + 1]
        b[x - 1][y - 2]
        b[x - 1][y + 2]
        b[x + 1][y - 2]
        b[x + 1][y + 2]

        assuming that the new indices i, j satisfy 0 < i, j < n
        """
        x, y = curr

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
            if point.x >= 0 and point.x < self.n and point.y >= 0 and point.y < self.n
        ]

        return result

    def find_paths(
        self,
        start: Point,
        end: Point,
        paths: Optional[list[list[Point]]] = None,
        visited=None,
        min_len: int = 5,
        max_len: int = 8,
    ) -> list[list[Point]]:
        """
        Finds all possible paths between start and end using only knights moves.
        """
        q: collections.deque[list[Point]] = collections.deque()

        if visited is None:
            visited = np.zeros((self.n, self.n))

            logger.debug(f"Visited {start}")
            visited[start.x][start.y] = True

            q.append([start])

        if paths is None:
            paths = []

        while q:
            logger.debug("start iteration")
            path = q.popleft()

            if len(path) > max_len:
                return paths

            curr = path[-1]

            if curr == end and len(path) > min_len:
                logger.debug("Reached the end.")
                paths.append(path)

            possible_moves = self.possible_moves(curr)

            logger.debug(
                f"""Possible moves from {curr}:
{possible_moves}
                         """
            )
            for next in possible_moves:

                logger.debug(f"curr path: {path}")
                visited = next in path

                logger.debug(f"Consider {next}, visited: {visited}")

                if not visited:

                    logger.debug(f"{next} not visited")

                    new_path = list(path)
                    new_path.append(next)

                    q.append(new_path)

            # logger.debug(f"visited:\n{visited}")
            logger.debug("end iteration")

        logger.debug(f"visited:\n{visited}")
        return paths

    def _calculate_score(self, path: list[Point]):
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
            next_letter = self.b.get(next)

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

    def calculate_score(self, path: list[Point]):
        score = self._calculate_score(path=path)
        a, b, c = symbols("a b c")
        return lambdify([a, b, c], score)

    def lambdify_score(self, score):
        a, b, c = symbols("a b c")
        return lambdify([a, b, c], score)

    def flip_path(self, path: list[Point]) -> list[Point]:
        return [Point(x, self.n - 1 - y) for x, y in path]

    def _convert_path_to_output_format(self, path: list[Point]) -> list[str]:
        return [str(point) for point in path]

    def solution_str(
        self, a: int, b: int, c: int, path_1: list[Point], path_2: list[Point]
    ) -> str:
        s = [str(a), str(b), str(c)]
        s.extend(self._convert_path_to_output_format(path=path_1))
        s.extend(self._convert_path_to_output_format(path=path_2))

        return ",".join(s)

    def get_unique_scores(self, paths: list[list[Point]]) -> dict:
        scores: dict = collections.defaultdict(list)
        paths_dict: dict = collections.defaultdict(list)

        for path in paths:
            paths_dict[len(path)].append(path)

        for paths in paths_dict.values():
            s: dict = collections.defaultdict(list)
            for path in paths:
                score = self._calculate_score(path)
                key = score

                for existing_score in scores:
                    if simplify(existing_score - score) == 0:
                        key = existing_score
                        break

                s[key].append(path)

            scores.update(s)

        return scores
