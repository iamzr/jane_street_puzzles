import datetime
import logging
from multiprocessing import Value
from pathlib import Path
import random

logs_dir = Path(__name__).parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    filename=logs_dir / f"{datetime.datetime.now()}.log",
    filemode="a+",
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Given two points
def find_midpoint(p1: Point, p2: Point) -> Point:
    return Point(x=(p1.x + p2.x) / 2, y=(p1.y + p2.y) / 2)


def find_gradient(p1: Point, p2: Point) -> float:
    return (p2.y - p1.y) / (p2.x - p1.x)


def find_points_on_perpendicular_bisector(p1: Point, p2: Point) -> tuple[Point, Point]:
    p3 = find_midpoint(p1, p2)
    g = find_gradient(p1=p1, p2=p2)

    # Using y - y_1 = m(x - x_1)
    # let x = 0
    y = (1 / g) * -p3.x + p3.y

    p4 = Point(x=0, y=y)

    return p3, p4


# Given three collinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if (
        (q.x <= max(p.x, r.x))
        and (q.x >= min(p.x, r.x))
        and (q.y <= max(p.y, r.y))
        and (q.y >= min(p.y, r.y))
    ):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:

        # Clockwise orientation
        return 1
    elif val < 0:

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):

    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if (o1 == 0) and onSegment(p1, p2, q1):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if (o2 == 0) and onSegment(p1, q2, q1):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if (o3 == 0) and onSegment(p2, p1, q2):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if (o4 == 0) and onSegment(p2, q1, q2):
        return True

    # If none of the cases
    return False


def get_closest_side(p: Point) -> tuple[Point, Point]:
    x = p.x
    y = p.y

    if y <= x and y < 1 - x:
        return Point(0, 0), Point(1, 0)
    elif y > x and y <= 1 - x:
        return Point(0, 0), Point(0, 1)
    elif y >= x and y > 1 - x:
        return Point(0, 1), Point(1, 1)
    elif y < x and y >= 1 - x:
        return Point(1, 0), Point(1, 1)
    else:
        raise ValueError("Something's gone wrong")


def has_solution(blue: Point, red: Point):
    p3, p4 = find_points_on_perpendicular_bisector(blue, red)

    p5, p6 = get_closest_side(blue)

    return doIntersect(p3, p4, p5, p6)


if __name__ == "__main__":
    # # p1 = Point(0.3, 0.3)
    # # p2 = Point(0.2, 0.5)

    # p1 = Point(0.3, 0.3)
    # p2 = Point(0.2, 0.31)

    # p3, p4 = find_points_on_perpendicular_bisector(p1, p2)

    # # closest side
    # p5, p6 = get_closest_side(p1)
    # print(f"closest_side: {p5}, {p6}")

    # print(doIntersect(p3, p4, p5, p6))
    n = 10_000_000_000
    next_magnitude = 10

    i = 0
    results = 0
    while i <= n:
        red = Point(x=random.random(), y=random.random())
        blue = Point(x=random.random(), y=random.random())

        results += has_solution(blue=blue, red=red)
        i += 1

        if i == next_magnitude:
            # Calculate the answer and store in outputs
            ans = results / i
            logger.info(f"At iteration {i}: Answer = {ans}")

            # Update next magnitude to the next power of 10
            next_magnitude *= 10

    ans = results / n
    logger.info(ans)
