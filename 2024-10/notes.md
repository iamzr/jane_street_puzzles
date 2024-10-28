After reading the problem it seems like there's a few steps required to solve the problem.

1. You need to solve how to calculate trips from one corner to the other corner
2. You need to be able to correctly calculate their weights


 After talking yesteday about symmetries I've hd sme thoughts and found the following:
 1. There are no even len solutions
 2. the scores for each path are not unique i.e. for all the different 7 length paths the scores are degenerate.

 For len(5) paths:
 the mid points are 
 (4,2)
 (1,3)
 (3,1)
 (2,4)

 for length 7
(2,3)
(1,0)
(1,4)
(3,2)
(5,2)
(3,0)
(5,0)


--- 
I've looked at all the solutions for the len 7 paths and found that half of the scores ( i think) are degenerate i,e, there's like 90 or so paths but on;y 52 unique solutions