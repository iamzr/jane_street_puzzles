# %%
from solution import KnightsMoves, b
# calculate all paths up to n moves
max_len = 8
paths = KnightsMoves().find_paths(
    board=b, start=(0, 0), end=(5, 5), max_len=max_len)
