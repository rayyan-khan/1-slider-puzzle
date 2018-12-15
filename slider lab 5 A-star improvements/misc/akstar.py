from time import time
from heapq import heappush, heappop, heapify
from collections import namedtuple

argv = ['0', 'abcedifghmj_lnok']

# Setting up static variables:
DIM = int(len(argv[1])**0.5) # Dimensions
INP = argv[1].lower() # Input
SINP = sorted(argv[1].lower(), key=lambda x: ord(x) if x != '_' else 0) # sorted input
START_LIST = [SINP.index(x) for x in INP] # Convert to numbers
GOALHASH = hash(tuple([0] + list(range(1, len(INP)))))  # e.g. hash((1,2,3,0))
PATTERN = {} # Pregenerate where you can swap, to reduce computations.
for i in range(DIM**2):
    swappable = []
    if i // DIM > 0: # up
        swappable.append(i - DIM)
    if i // DIM < DIM - 1: # down
        swappable.append(i + DIM)
    if i % DIM != 0: # left
        swappable.append(i - 1)
    if i % DIM != DIM - 1: # right
        swappable.append(i + 1)
    PATTERN[i] = tuple(swappable)

#Class definitions:
class Position(namedtuple("Position", "matrix root moves cost matHash")):
    def __new__(cls, matrix, root=None, moves=0):
        # Manhattan
        cost = sum(abs((val - 1)%DIM - k%DIM) + abs((val-1)//DIM - k//DIM) for k, val in enumerate(matrix) if val)
        return super(Position, cls).__new__( # Save values into namedtuple
            cls, tuple(matrix), root, moves, cost, hash(tuple(matrix)))

    def __bool__(self): # isGoal?
        return self.matHash == GOALHASH

    def __lt__(self, comp): # Comparisons for minheap
        return self.cost + self.moves < comp.cost + comp.moves

    def __eq__(self, comp):
        return self.cost + self.moves == comp.cost + comp.moves

    def __str__(self): # Pretty length
        prettyMatrix = [SINP[x] if x >= 0 else '*' for x in self.matrix] # Convert back to input format
        header = "-" * ((DIM * 2) - 1) # Create the header
        content = ('\n' + ' '.join(prettyMatrix[i : i + DIM]) for i in range(0, DIM**2, DIM))
        return "{0}{1}\n{0}".format(header, ''.join(content))

    def __hash__(self): # Hash for visisted
        return self.matHash

    def path(self, Count=0): # Recursive path printing
        pCount = 0
        if self.root is not None:
            pCount = 1 + self.root.path(Count+1)
            print("{}↓".format(' ' * (DIM-1)))
        print(self)
        return pCount

    def neighbors(self, doMoves=False): # Get the number of neighbors
        def swap(zero, coord):
            if zero < coord: # If the zero comes before the coord
                return self.matrix[:zero] + (self.matrix[coord],) + self.matrix[zero + 1:coord] + (0,) + self.matrix[coord + 1:]
            return self.matrix[:coord] + (0,) + self.matrix[coord + 1:zero] + (self.matrix[coord],) + self.matrix[zero + 1:]
        zeroIndex = self.matrix.index(0)
        for neighbor in PATTERN[zeroIndex]: # Generator fun
            yield Position(swap(zeroIndex, neighbor), root=self,
                           moves=self.moves + 1 if doMoves else 0)

# Checking for solvability:
invCount = sum((START_LIST[a] > START_LIST[b]) for a in range(1, (DIM**2)-1) for b in range(a+1, DIM**2) if START_LIST[a] and START_LIST[b])
rowCount = DIM - 1 - (START_LIST.index(0) // DIM) if DIM&1 == 0 else 0
#if (invCount + rowCount)&1 != 0:
#    print("Impossible! IC: {}, RC: {}".format(invCount, rowCount))
#    exit()

#Solvable! You may proceed to algorithm:
def astar(inp):
    openSet = [Position(inp)]
    closedSet = set()
    queueLen = 0

    while openSet:
        v = heappop(openSet) # Remove best choice
        queueLen += 1 # Add 1 to numNodesRemoved

        for child in v.neighbors(doMoves=True):
            if child: # If the node is the goal, return it
                return child, queueLen
            if child.__hash__ in closedSet: #If you've seen it before, pass
                continue
            else: # If you've not seen it before, add it
                heappush(openSet, child)
        closedSet.add(v.__hash__) # We have visited v

START = time()
node, queuelen = astar(START_LIST) if not Position(START_LIST) else (Position(START_LIST), 0)

print(f"Number of steps for solution: {node.path()}")
print(f"Number of items removed from queue: {str(queuelen)}")
print("Time taken: {:.5f}s".format(time() - START))
