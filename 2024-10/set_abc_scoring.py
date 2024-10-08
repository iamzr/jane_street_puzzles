# %%
from solution import KnightsMoves, b
# calculate all paths up to n moves
max_len = 8
paths = KnightsMoves().find_paths(
    board=b, start=(0, 0), end=(5, 5), max_len=max_len)

# %%


def flip_path(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(x, 6 - y) for x, y in path]


def get_board(a: int, b: int, c: int):
    board = [
        [a, b, b, c, c, c],
        [a, b, b, c, c, c],
        [a, a, b, b, c, c],
        [a, a, b, b, c, c],
        [a, a, a, b, b, c],
        [a, a, a, b, b, c],
    ]
    return board


def flip_board(board: list[list[str]]) -> list[list[str]]:
    return [row[::-1] for row in board]


def score_path(a: int, b: int, c: int, path: list[tuple[int, int]]) -> int:
    board = get_board(a, b, c)

    score = a
    old_move = [0, 0]
    for new_move in path[1:]:
        if board[old_move[0]][old_move[1]] == board[new_move[0]][new_move[1]]:
            score += board[new_move[0]][new_move[1]]
        else:
            score *= board[new_move[0]][new_move[1]]
