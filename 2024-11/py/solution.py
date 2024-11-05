from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import logging
from multiprocessing import Manager, Pool, Value
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
    __slots__ = ["x", "y"]

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


def worker_task(n):
    i = 0
    results = 0
    while i <= n:
        red = Point(x=random.random(), y=random.random())
        blue = Point(x=random.random(), y=random.random())

        results += has_solution(blue=blue, red=red)
        i += 1

    return results


def main_multithreaded(n, num_threads=5):
    total_results = 0

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        trials_per_thread = n // num_threads
        trials = trials_per_thread * num_threads

        # Create a list of futures for each chunk
        futures = [
            executor.submit(worker_task, trials_per_thread) for i in range(num_threads)
        ]

        # Collect results as they complete
        for future in as_completed(futures):
            total_results += future.result()

    ans = total_results / trials
    logging.info(f"Final answer after {trials} iterations: {ans}")


def main_multiprocessing(n, num_processes=10):
    logger.info(f"Starting main with {num_processes=}")
    # Set up multiprocessing pool
    with Pool(processes=num_processes) as pool:
        trials_per_process = n // num_processes
        logger.debug(f"{trials_per_process=}")
        trials = trials_per_process * num_processes

        # Define the tasks for each chunk
        tasks = [[trials_per_process]] * num_processes

        # Run worker tasks in parallel
        results = pool.starmap(worker_task, tasks)

        # # close the thread pool
        pool.close()
        # wait for issued tasks to complete
        pool.join()

        total_results = 0
        for result in results:
            logger.debug(f"Result: {result}")
            total_results += result

        logger.debug(f"Sum of results: {total_results}")
        logger.debug(f"Trials: {trials}")
        ans = total_results / trials
        logger.info(f"Final Answer after {n} iterations: {ans}")


if __name__ == "__main__":
    logger.info("start")
    main_multiprocessing(n=1_000_000_000, num_processes=10)
