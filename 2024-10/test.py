import datetime
import itertools
import logging
from solution import KnightsMoves, Point

k = KnightsMoves()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=f"logfile {datetime.datetime.now()}",
    filemode="a+",
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)


class TreeNode:
    def __init__(self, point):
        self.point = point
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"TreeNode(point={self.point}, children={self.children})"


def get_neighbors(point):
    """Return valid neighbors for a given point on the board."""
    x, y = point

    possible_moves = [
        (x - 2, y - 1),
        (x - 2, y + 1),
        (x + 2, y - 1),
        (x + 2, y + 1),
        (x - 1, y - 2),
        (x - 1, y + 2),
        (x + 1, y - 2),
        (x + 1, y + 2),
    ]

    n = 6

    result = [
        point for point in possible_moves if x >= 0 and x < n and y >= 0 and y < n
    ]

    return result


# def find_paths(start, end, board, min_length, max_length, visited=None, depth=0):
#     """
#     Recursively find all paths from start to end within a max length and return as a tree.

#     Parameters:
#     - start: The starting point (tuple).
#     - end: The ending point (tuple).
#     - board: The 2D board array.
#     - max_length: Maximum allowed path length.
#     - visited: Set of visited points for the current path.
#     - depth: Current depth of recursion.

#     Returns:
#     - TreeNode representing the root of the tree structure with all paths.
#     """
#     if visited is None:
#         visited = set()
#     visited.add(start)

#     # Create a tree node for the current start point
#     root = TreeNode(start)

#     # If the start is the end, or if we've reached the max depth, return the node
#     if start == end and depth >= min_length:
#         print("hit end")
#         return root
#     if depth >= max_length:
#         # print("hit depth")
#         return None

#     # Explore each neighbor that hasn't been visited
#     for neighbor in get_neighbors(start):
#         if neighbor not in visited:
#             child_node = find_paths(
#                 neighbor, end, board, min_length, max_length, visited.copy(), depth + 1
#             )
#             if child_node:
#                 root.add_child(child_node)

#     return root


scores_1 = {}
scores_2 = {}


def handle_path(path):
    path = [Point(x, y) for x, y, in path]
    score = k._calculate_score(path=path)
    if score not in scores_1:
        scores_1[score] = path

    alt_path = [Point(x, 6 - 1 - y) for x, y in path]
    score = k._calculate_score(path=alt_path)
    if score not in scores_2:
        scores_2[score] = alt_path


def find_paths(
    start,
    end,
    board,
    max_length,
    current_path=None,
    visited=None,
    depth=0,
    all_paths=None,
):
    """
    Perform DFS to find all paths from start to end within a max length, without constructing a tree.

    Parameters:
    - start: The starting point (tuple).
    - end: The endpoint (tuple).
    - board: The 2D board array.
    - max_length: Maximum allowed path length.
    - current_path: The path being built as a list of points.
    - visited: Set of visited points for the current path.
    - depth: Current depth of recursion.
    - all_paths: List to store all complete paths from start to end.

    Returns:
    - List of all paths from start to end point.
    """
    if current_path is None:
        current_path = []
    if visited is None:
        visited = set()
    if all_paths is None:
        all_paths = []

    # Add the current point to the path and mark as visited
    current_path.append(start)
    visited.add(start)

    # If we have reached the end point, add the path to all_paths
    if start == end:
        all_paths.append(current_path.copy())
        handle_path(current_path)
    elif depth < max_length:  # Continue exploring if max depth not reached
        for neighbor in get_neighbors(start):
            if neighbor not in visited:
                find_paths(
                    neighbor,
                    end,
                    board,
                    max_length,
                    current_path,
                    visited,
                    depth + 1,
                    all_paths,
                )

    # Backtrack: remove the current point from path and visited set
    current_path.pop()
    visited.remove(start)

    return all_paths


def dfs_collect_paths(node, end, current_path=None, all_paths=None):
    """
    Depth-First Search to collect all unique paths from start to end.

    Parameters:
    - node: The current TreeNode being visited.
    - end: The endpoint to stop path collection.
    - current_path: The path being built as a list of points.
    - all_paths: List to store all complete paths from start to end.

    Returns:
    - List of all paths from the start node to the end node.
    """
    if current_path is None:
        current_path = []
    if all_paths is None:
        all_paths = []

    # Add the current node's point to the path
    current_path.append(node.point)

    # If we've reached the end point, add the path to all_paths
    if node.point == end:
        all_paths.append(current_path.copy())
        handle_path(current_path)
    else:
        # Continue DFS on each child
        for child in node.children:
            dfs_collect_paths(child, end, current_path, all_paths)

    # Backtrack to explore other paths
    current_path.pop()

    return all_paths


# Usage example
board = [
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "A", "B", "B", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "A", "B", "B", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
    ["A", "B", "B", "C", "C", "C"],
]

# Define start and end points
start_point = (0, 0)
end_point = (5, 5)

min_path_length = 5
max_path_length = 7  # Maximum path length

# Generate the tree
# tree_root = find_paths(start_point, end_point, board, min_path_length, max_path_length)
all_paths = find_paths(start_point, end_point, board, max_path_length)

# Printing the root node to see the structure
# print(tree_root)

# Use DFS to collect all paths
# all_paths = dfs_collect_paths(tree_root, end_point)

logger.info(f"{scores_1=}")
logger.info(f"{scores_2=}")

# # Print all paths
# for path in all_paths:
#     print(path)


def check_scores(scores: dict):
    result = {}
    for score in scores:
        score_func = k.lambdify_score(score=score)

        for a, b, c in itertools.product(range(1, 6), range(1, 6), range(1, 6)):
            s = score_func(a, b, c)

            if s == 2024 and result.get((a, b, c)) is None:
                result[(a, b, c)] = scores[score]

    return result


results_1 = check_scores(scores_1)
results_2 = check_scores(scores_2)

solutions = results_1.keys() & results_2.keys()

for solution in solutions:
    a, b, c = solution
    output = f"""found solution
For {a=}, {b=}, {c=} where
# 
path_1s: {k._convert_path_to_output_format(results_1[solution])}
# 
path_2s: {k._convert_path_to_output_format(results_2[solution])}
# 
solution_string {k.solution_str(a=a, b=b, c=c, path_1=results_1[solution], path_2=results_2[solution])}
            """

    print(output)
    logger.info(output)

print("end")


# # logger.info("Run optimization")
# for score_1, score_2 in itertools.product(scores_1, scores_2):
#     score_func_1 = k.lambdify_score(score_1)
#     score_func_2 = k.lambdify_score(score_2)

#     for a, b, c in itertools.product(range(1, 6), range(1, 6), range(1, 6)):
#         s_1 = score_func_1(a, b, c)
#         s_2 = score_func_2(a, b, c)
#         if s_1 == 2024 and s_2 == 2024 and (a + b + c) <= 50:
#             print(a, b, c)
#             print(
#                 f"""found solution
# For {a=}, {b=}, {c=} where

# score_1: {score_1}

# score_2: {score_2}

# path_1s: {k._convert_path_to_output_format(scores_1[score_1])}

# path_2s: {k._convert_path_to_output_format(scores_2[score_2])}

# solution_string {k.solution_str(a=a, b=b, c=c, path_1=scores_1[score_1], path_2=scores_2[score_2])}
#             """
#             )

#             break
