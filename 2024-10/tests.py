import numpy as np
from sympy import simplify, symbols
from solution import Point
from solution import KnightsMoves

board = [
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
]

k = KnightsMoves(board=board)


def test_get_solution_string():
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

    result = k.calculate_score(path=path)

    print(result)

    assert simplify(expected - (result)) == 0
