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

    board = board[::-1]
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
        if board[old_move[1]][old_move[0]] == board[new_move[1]][new_move[0]]:
            score += board[new_move[1]][new_move[0]]
        else:
            score *= board[new_move[1]][new_move[0]]

        # same for flipped board
        if board_flipped[old_move[1]][old_move[0]] == board_flipped[new_move[1]][new_move[0]]:
            score_flipped += board_flipped[new_move[1]][new_move[0]]
        else:
            score_flipped *= board_flipped[new_move[1]][new_move[0]]

        # check if score is over 2024
        if (score > 2024) or (score_flipped > 2024):
            break

        old_move = new_move

    # check if score is corect at the end of the path
    if (score == 2024) and (score_flipped == 2024):
        return path


# %%
min_sum = 150
min_abc = None
min_path = None
for a in range(1, 50):
    for b in range(1, 50):
        if a == b:
            continue
        for c in range(1, 50):
            if c == a or c == b:
                continue
            for path in paths:
                if score_path(a, b, c, path):
                    if min_sum > a + b + c:
                        min_abc = (a, b, c)
                        min_path = path
                        min_sum = a + b + c
                        print(min_abc, min_path, min_sum)
