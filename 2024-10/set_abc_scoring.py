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


def flip_board(board: list[list[int]]) -> list[list[int]]:
    return board[::-1]


def score_path(a: int, b: int, c: int, path: list[tuple[int, int]]) -> int:
    board = get_board(a, b, c)
    board_flipped = flip_board(board)

    score = 0
    score_flipped = 0
    old_move = [0, 0]
    for new_move in path[1:]:

        # check if moving to the same letter and apply rules
        if board[old_move[0]][old_move[1]] == board[new_move[0]][new_move[1]]:
            score += board[new_move[0]][new_move[1]]
        else:
            score *= board[new_move[0]][new_move[1]]

        # same for flipped board
        if board_flipped[old_move[0]][old_move[1]] == board_flipped[new_move[0]][new_move[1]]:
            score_flipped += board_flipped[new_move[0]][new_move[1]]
        else:
            score_flipped *= board_flipped[new_move[0]][new_move[1]]

        # check if score is over 2024
        if (score > 2024) or (score_flipped > 2024):
            break

        old_move = new_move

    # check if score is corect at the end of the path
    if (score == 2024) and (score_flipped == 2024):
        print(f"Path: {path}")
        print(f"a: {a}, b: {b}, c: {c}")


# %%
a, b, c, = 1, 2, 3
for path in paths:
    score_path(a, b, c, path)
