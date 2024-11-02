import datetime
import logging
from pathlib import Path
import sys

import numpy as np
from solution import KnightsMoves, Point
import pprint


pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)

logs_dir = Path(__name__).parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    filename=logs_dir / f"{datetime.datetime.now()}.log",
    filemode="a+",
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)
board = [
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
]

k = KnightsMoves(board=board)

# Define start and end points
start_point = Point(0, 0)
end_point = Point(5, 5)

min_path_length = 5
max_path_length = 7  # Maximum path length

logger.info("Calculate all paths and return all unique score functions")
scores_1, scores_2 = k.find_paths(
    start=start_point, end=end_point, max_length=max_path_length
)

logger.debug(
    f"""Score functions for paths from {Point(0,0)} to {Point(5,5)}:
    
{pp.pformat(scores_1)}
"""
)
logger.debug(
    f"""Score functions for paths from {Point(0,5)} to {Point(5, 0)}:
    
{pp.pformat(scores_2)}
"""
)


logger.info(
    f"For all the score functions of paths from {Point(0,0)} to {Point(5,5)}, find a combination of (a,b,c) such that score(a,b,c) == 2024 "
)
results_1 = k.check_scores(scores=scores_1)

logger.info(
    f"For all the score functions of paths from {Point(0,5)} to {Point(5,0)}, find a combination of (a,b,c) such that score(a,b,c) == 2024 "
)
results_2 = k.check_scores(scores=scores_2)

logger.info("Find solutions.")
solutions = results_1.keys() & results_2.keys()

if not solutions:
    logger.info("No solution found.")
    sys.exit()

optimal = (np.inf, np.inf, np.inf, "")
for solution in solutions:
    a, b, c = solution
    solution_string = k.solution_str(
        a=a, b=b, c=c, path_1=results_1[solution], path_2=results_2[solution]
    )
    output = f"""Found solution:
For {a=}, {b=}, {c=} where

path_1s: {str(results_1[solution])}

path_2s: {str(results_2[solution])}
"""

    logger.debug(output)

    if a + b + c < optimal[0] + optimal[1] + optimal[2]:
        optimal = (a, b, c, solution_string)

if optimal[3] == "":
    logger.info("No solution found.")
else:
    logger.info(f"Optimal solution: {optimal[3]}")
