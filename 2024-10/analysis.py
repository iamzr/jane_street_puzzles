from solution import KnightsMoves, board
# from paths import paths_1
from alt_paths1 import paths_2
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

k = KnightsMoves(b=board)

scores = set()
try:
    for index, path in enumerate(paths_2[5:97]):
        if len(path) == 7:
            score = k._calculate_score(path=path) 
            logger.info((index, score))
            scores.add(score)
except KeyboardInterrupt:
    logger.warning("interrupted")
    
with open("scores_alt.py", "w") as f:
    f.writelines("paths_1 =[")
    for score in scores:
        f.writelines(f"{score},\n")
    f.writelines("]")