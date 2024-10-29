import numpy as np
from sympy import simplify, symbols
from solution import Board, Point
from solution import KnightsMoves

board = [
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
]

b = Board(b=board)

k = KnightsMoves()


def test_get():
    assert b.get(Point(2, 1)) == "A"
    assert b.get(Point(0, 0)) == "A"
    assert b.get(Point(5, 5)) == "C"
    assert b.get(Point(2, 5)) == "B"
    assert b.get(Point(4, 4)) == "C"


def test_get_value():

    assert k.b.get(Point(0, 4)) == "A"


def test_convert_to_path():
    path1 = [
        Point(x=0, y=0),
        Point(x=1, y=2),
        Point(x=3, y=1),
        Point(x=1, y=0),
        Point(x=2, y=2),
        Point(x=3, y=4),
        Point(x=5, y=5),
    ]

    path2 = path1

    s = k.solution_str(a=1, b=2, c=3, path_1=path1, path_2=path2)

    assert s == "1,2,3,a1,b3,d2,b1,c3,d5,f6,a1,b3,d2,b1,c3,d5,f6"


def test_get_unique_scores():
    paths = [
        [
            Point(0, 0),
            Point(2, 1),
            Point(1, 3),
            Point(3, 2),
            Point(2, 4),
            Point(4, 3),
            Point(5, 5),
        ]
    ]

    p = []
    p.extend(paths)
    p.extend(paths)
    p.extend(paths)

    s = k.get_unique_scores(paths=p)

    assert len(s) == 1


def test_get_path_output():
    path = [
        Point(0, 0),
        Point(2, 1),
        Point(1, 3),
        Point(3, 2),
        Point(2, 4),
        Point(4, 3),
        Point(5, 5),
    ]

    result = k._convert_path_to_output_format(path=path)

    return result


def test_calculate_score():
    path = [
        Point(0, 0),
        Point(2, 1),
        Point(1, 3),
        Point(3, 2),
        Point(2, 4),
        Point(4, 3),
        Point(5, 5),
    ]

    a, b, c = symbols("a b c")

    expected = 3 * a * b * c + b * c + c

    result = k._calculate_score(path=path)

    print(result)

    assert simplify(expected - (result)) == 0


if __name__ == "__main__":
    print(test_get_path_output())
