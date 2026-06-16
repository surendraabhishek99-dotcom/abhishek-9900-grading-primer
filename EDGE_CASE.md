# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation

for course and name we need to check whether its string typed or not. IF not I am throwing 400 error

for mark if mark is not between 1 and 100 we throw a non-valid error

for /stats when there are no valid marks The API returns safe default stats instead of causing a divide-by-zero error.