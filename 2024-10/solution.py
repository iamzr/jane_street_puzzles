import collections
import logging
import numpy as np
from sympy import Eq, lambdify, symbols
from scipy.optimize import NonlinearConstraint, minimize

logger = logging.getLogger(__name__)

board = [
    ["A", "B" , "B", "C", "C", "C"],
    ["A", "B" , "B", "C", "C", "C"],
    ["A", "A" , "B", "B", "C", "C"],
    ["A", "A" , "B", "B", "C", "C"],
    ["A", "A" , "A", "B", "B", "C"],
    ["A", "A" , "A", "B", "B", "C"],
]


class KnightsMoves:
    def __init__(self, b):
        self.b = b
        
        self.n = len(b)

    def possible_moves(self, curr: tuple[int, int]) -> list[tuple[int, int]]:
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

        possible_moves = [(x - 2, y - 1),
        (x - 2, y + 1),
        (x + 2, y - 1),
        (x + 2, y + 1),
        (x - 1, y - 2),
        (x - 1, y + 2),
        (x + 1, y - 2),
        (x + 1, y + 2)]

        
        result = [ point for point in possible_moves if point[0] >= 0 and point[0] < self.n and point[1] >= 0 and point[1] < self.n
                  ] 

        return result

    def find_paths(self, start: tuple[int, int], end: tuple[int, int], max_len: int = 8):
        """
        Finds all possible paths between start and end using only knights moves.
        """
        q: collections.deque[list[tuple[int, int]]] = collections.deque()

        visited = np.zeros((self.n, self.n)) 

        logger.debug(f"Visited {start}")
        visited[start[0]][start[1]] = True
        q.append([start])

        paths: list[list[tuple[int, int]]] = []
        while q:
            logger.debug("start iteration")
            path = q.popleft()

            if len(path) > max_len:
                return(paths)

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
        curr = path[0]

        a, b, c = symbols("a b c")

        score = a
        
        m = {
            "A" : a,
            "B" : b,
            "C": c
        }
        
        current_letter = "A"
        for next in path:
            logger.debug(f"next {next}")
            next_letter = board[next[0]][next[1]]

            logger.debug(f"{curr} {current_letter} -> {next} {m[next_letter]}")
            if next_letter != current_letter:
                logger.debug(f"multiply by {m[next_letter]}")
                score *= m[next_letter]
            else:
                logger.debug(f"add {m[next_letter]}")
                score += m[next_letter]

            current_letter = next_letter
        

        logger.debug(score)
        return lambdify([a,b,c], score)
            

            
    def flip_path(self, path: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return [(x, self.n - 1 - y) for x, y in path]       
        

def run_optimization(f, g):
    """Once we've got a set of paths, then we've essentially got an optimization problem. 
    
    Minimize: A + B + C 
    given:
    
    A, B, C > 0 
    path_1 = 2024
    path 2 = 2024
    """
    def constraint_1(x):
        a, b, c = x
        return f(a,b,c) - 2024

    def constraint_2(x):
        a, b, c = x
        return g(a,b,c) - 2024

    c1 = NonlinearConstraint(constraint_1, 0, 0)
    c2 = NonlinearConstraint(constraint_2, 0, 0)

    def objective_function(x):
        a, b, c = x
        return  a + b + c

    x = [1,1,1]

    bounds = (
        (0, None),
        (0, None),
        (0, None)
    )

    res = minimize(objective_function,
                   x, 
                   constraints=[c1, c2],
                   bounds=bounds)
    
    return res


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    """
    First we start with calculating the different paths between the start and end.
    """
    n=6

    k =KnightsMoves(b=board)

    paths = k.find_paths(start=(0,0), end=(5, 5))
    
    with open("paths.txt", "w") as f:
        for path in paths:
            f.writelines(f"{path}\n")


    """
    We need to also find the paths from (0,6) to (6,0), but the thing is all of our solutions are valid from any corner to the corner across.
    So all we need to do is rotate (or just reflect in y = 3) each path and then we have a valid solution for (0,6) and (6,0)
    """
    alt_paths = [(k.flip_path(path)) for path in paths]

    with open("alt_paths.txt", "w") as f:
        for path in alt_paths:
            f.writelines(f"{path}\n")


    """
    Need to calculate the formulas for the scores
    """



