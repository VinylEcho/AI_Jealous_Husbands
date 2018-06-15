# The new Jealous Husbands problem!
# Input: asks for number of pairs (ex: pairs 3 = 3 husbands, 3 wives), and boat capacity (ex: boat 2 = 2 people per trip)

from collections import deque
import itertools

boatSize = 0
numPairs = 0


class State(object):
    def __init__(self, initial, goal, boat):
        # creates a representation of the state of each shore with
        # initial = starting shore, goal = goal shore
        self.initial = initial
        self.goal = goal
        # Boat indicates which side of the river the boat is on, 0 for starting shore, 1 for goal shore
        self.boat = boat

    # Uses a string representation of the current board as a hash key (used to avoid loops)
    def __hash__(self):
        return hash("%s,%s,%d" % (self.initial, self.goal, self.boat))

    def __eq__(self, other):
        return other.goal == self.goal and other.initial == self.initial and other.boat == self.boat

    # Generates all possible moves from the given state by creating all possible subsets for the given boat
    # If the generated goal and initial states are valid, then creates a new state and a description of the move
    def nextStates(self):
        if self.boat == 0:
            shuffle = set(powerset(self.initial))
            for i in shuffle:
                i = set(i)
                tempInitial = set(self.initial).difference(i)
                tempGoal = set(self.goal).union(i)
                if valid(tempGoal) and valid(tempInitial):
                    temp = State(tempInitial, tempGoal, 1)
                    action = "Take %s to goal" % ', '.join(i)
                    yield (action, temp)
        else:
            shuffle = set(powerset(self.goal))
            for i in shuffle:
                i = set(i)
                tempInitial = self.initial.union(i)
                tempGoal = self.goal.difference(i)
                if valid(tempGoal) and valid(tempInitial):
                    temp = State(tempInitial, tempGoal, 0)
                    action = "Take %s back to start" % ', '.join(i)
                    yield (action, temp)

    # Checks if the starting shore is empty, the goal state is full and the boat is on the far side
    def isGoal(self):
        return len(self.initial) == 0 and len(self.goal) == numPairs*2 and self.boat == 1


# Used to check if the given set represents a valid state by seeing if every woman in the set is accompanied by her husband
# if the woman is without a husband, then checks if there is any other husband present, returning false if another is found
def valid(set):
    for i in set:
        if i[0] == "W":
            temp = i.replace("W", "H")
            if temp not in set:
                for j in range(1, numPairs+1):
                    m = "H"+str(j)
                    if m in set:
                        return False
    return True


# Tree node which stores the game state in state, parent node in parent
# a string representation of the move which led to this node in action, and finally the depth of the node in depth
class Node(object):
    def __init__(self, parent, state, action, depth):
        self.parent = parent
        self.state = state
        self.action = action
        self.depth = depth

    # Used to generate all possible child nodes from the current node, then returns a list generator
    def expand(self):
        for (action, nextState) in self.state.nextStates():
            nextNode = Node(parent=self,
                           state=nextState,
                           action=action,
                           depth=self.depth + 1)
            yield nextNode

    # Traces back up the tree to produce the list of steps taken to reach the solution
    def find_solution(self):
        solution = []
        node = self
        while node.parent is not None:
            solution.append(node.action)
            node = node.parent
        solution.reverse()
        return solution


# Creates all possible "boat" combinations, from 1 occupant to a full boat
def powerset(iterable):
    s = set(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, boatSize+1))


# Fairly typical breadth-first search, stores a list of visited states
def breadthFirstSearch(initial):
    rootNode = Node(parent=None, state=initial, action=None, depth=0)
    queue = deque([rootNode])
    visited = set()
    depth = -1
    i = 0
    while True:
        if not queue:
            return None
        node = queue.popleft()
        # Prints the current search depth each time a new layer of the tree is reached
        if node.depth > depth:
            depth = node.depth
            print "depth = %d" % depth
        # If a goal state is found, prints out the sequence of steps taken to reach it
        if node.state.isGoal():
            print i
            solution = node.find_solution()
            return solution
        # Generates new nodes, and adds unique nodes to the queue
        newNodes = node.expand()
        i+=1
        for n in newNodes:
            if n.state not in visited:
                queue.append(n)
                visited.add(n.state)
    return None


def main():
    global numPairs
    global boatSize
    done = False
    print "Welcome to the Jealous husbands solver!"
    while not done:
        validPairs = False
        validBoat = False
        # Loops until the user enters a valid number of pairs and boat size is entered
        while not validPairs:
            numPairs = input("Please enter the number of pairs: ")
            if numPairs > 0:
                validPairs = True
            else:
                print "Invalid number of pairs (must be greater than 0)"
        while not validBoat:
            boatSize = input("Please enter the size of the boat: ")
            if boatSize > 1:
                validBoat = True
            else:
                print "Invalid boat size (must be greater than 1)"
        if boatSize >= (2 * numPairs):
            # Short circuits if all members can be transported in one trip
            print "Problem solved in one trip"
        else:
            # Creates a new set of players (W1, H1, W2, H2, etc)
            initial = set()
            for i in range(1, numPairs+1):
                initial = initial.union(("W"+str(i), "H"+str(i)))
            # Creates a starting state for the board, then passes the state to the searching tree builder
            startState = State(initial, set(), 0)
            solution = breadthFirstSearch(startState)
            # Prints out the sequence of moves taken if a solution is found, or prints an error if a loop is found
            if solution is None:
                print "Solution not found"
            else:
                i = 1
                for step in solution:
                    print("%d: %s"% (i, step))
                    i += 1
        ans = raw_input("Play another round? (y/n): ")
        if ans.lower() == "n":
            done = True

main()