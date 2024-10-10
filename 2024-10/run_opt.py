import logging

from sympy import lambdify
from solution import KnightsMoves, run_optimization, board

score = KnightsMoves(b=board).calculate_score(path=[
    (0,0),
    (2,5),
    (4,4),
    (3,2),
    (5,1)
])
    
logging.debug(f"Score function {score}")
    
print(run_optimization(score, score))

"""Cant use this because it doesnt allow to restrict to only integer solutions"""