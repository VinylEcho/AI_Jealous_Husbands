# AI_Jealous_Husbands
A program for my AI class designed to solve a variant of the classic river crossing puzzle Missionaries and Cannibals (or the fox, lettuce, rabbit problem).

Rules:
1. The boat is not self driving, so there must be one person on board for each trip.
2. A wife cannot be on the same shore as another husband if her husband is not present.

Behavior:
- Prompts the user to enter the capacity of the boat (boatsize > 1).
- Prompts for the number of couples (numPairs > 1).
- If boatSize >= 2 * numPairs, reports that the problem will take only 1 trip.
- If the problem can be solved, prints the sequence of moves used to stdout.
- If no solution is found, reports no solution found.

