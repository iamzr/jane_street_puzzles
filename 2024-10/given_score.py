import itertools
import logging

from sympy import lambdify
from solution import KnightsMoves, run_optimization, board

from paths import paths_1
from alt_paths import paths_2

logging.basicConfig(level=logging.DEBUG)

k = KnightsMoves(b=board)

paths_1 = paths_1
paths_2 = paths_2

paths = [
    [(0,0), (1,2), (2,0), (3,2), (5,1), (4,3), (5,5)]
]

paths_1 = paths
paths_2 = [k.flip_path(paths[0])]

for path_1, path_2 in itertools.product(paths_1, paths_2):
    logging.info(f"path1:{path_1}\npath2:{path_2}")
    logging.debug("calculate score 1")
    score_1 = k.calculate_score(path=path_1)

    logging.debug("calculate score 2")
    score_2 = k.calculate_score(path=path_2)

    for a, b, c in itertools.product(range(1,50), range(1,50), range(1,50)):
        s_1 = score_1(a, b, c)
        s_2 = score_2(a,b,c)
        if s_1 == 2024 and s_2 == 2024:
            print(a,b,c)
            print("found solution")
            break
    
    logging.debug("no solution found")