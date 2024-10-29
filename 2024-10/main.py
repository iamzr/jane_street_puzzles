import itertools
import logging
from pathlib import Path

from solution import KnightsMoves, Point

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

output_dir = Path(__file__).parent / "output"

k = KnightsMoves()

"""
First we start with calculating the different paths between the start and end.
"""
logger.info("Calculate paths from (0,0) to (5,5)")
try:
    paths_1 = k.find_paths(start=Point(0, 0), end=Point(5, 5), min_len=5, max_len=7)
except KeyboardInterrupt:
    logger.warning("interrupted")

# with open(output_dir / "paths.py", "w") as f:
#     f.writelines("paths_1 =[")
#     for path in paths_1:
#         f.writelines(f"{path},\n")
#     f.writelines("]")

"""
We need to also find the paths from (0,6) to (6,0), but the thing is all of our solutions are valid from any corner to the corner across.
So all we need to do is rotate (or just reflect in y = 3) each path and then we have a valid solution for (0,6) and (6,0)
"""

logger.info("Calculate paths from (0,6) to (6,0)")
alt_paths = [(k.flip_path(path)) for path in paths_1]

# with open(output_dir / "alt_paths.py", "w") as f:
#     f.writelines("paths_1 =[")
#     for path in alt_paths:
#         f.writelines(f"{path},\n")
#     f.writelines("]")

"""
Need to calculate the score functions for the paths.
For a given path length the score functions will be degenerate, i.e. every unique path might not result in a unique score function.
We will use a set so that we are only considering unique score functions moving forward.
"""

logger.info("Remove degnerate score functions")
paths_1_scores = k.get_unique_scores(paths=paths_1)
paths_2_scores = k.get_unique_scores(paths=alt_paths)

# with open(output_dir / "scores_1.py", "w") as f:
#     f.writelines("scores_1 =[")
#     for score in paths_1_scores:
#         f.writelines(f"{score},\n")
#     f.writelines("]")

# with open(output_dir / "scores_2.py", "w") as f:
#     f.writelines("scores_2 =[")
#     for score in paths_1_scores:
#         f.writelines(f"{score},\n")
#     f.writelines("]")

"""
Now you have two lists of score functions, we can simply loop over every pair of score functions to find the correct solution
"""

logger.info("Run optimization")
for score_1, score_2 in itertools.product(paths_1_scores, paths_2_scores):
    score_func_1 = k.lambdify_score(score_1)
    score_func_2 = k.lambdify_score(score_2)

    for a, b, c in itertools.product(range(1, 50), range(1, 50), range(1, 50)):
        s_1 = score_func_1(a, b, c)
        s_2 = score_func_2(a, b, c)
        if s_1 == 2024 and s_2 == 2024 and (a + b + c) <= 50:
            print(a, b, c)
            print(
                f"""found solution
For {a=}, {b=}, {c=} where

score_1: {score_1}

score_2: {score_2}

path_1s: {[k._convert_path_to_output_format(path) for path in paths_1_scores[score_1]]}

path_2s: {[k._convert_path_to_output_format(path) for path in paths_2_scores[score_2]]}

solution_string {k.solution_str(a=a, b=b, c=c, path_1=paths_1_scores[score_1][0], path_2=paths_2_scores[score_2][0])}
            """
            )

            break
