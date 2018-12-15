import time
import sys
import heapq

# working on improving neighbors method
# switch .append to comprehension
# next: add neighbor positions when returning list of neighbors
# kind of a testing version -- actual one is AstarMNHT

file = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('eckel.txt', 'r')
goal = file.readline().strip()
if '0' in goal:
    goal = goal[0:goal.find('0')].lower() + '_' + goal[goal.find('0') + 1:].lower()

pzlSize = len(goal)
sideLen = int(pzlSize**.5)

# create lookup
lookup = [[] for i in range(pzlSize)]
# corners
lookup[0] = [1, sideLen]  # top left
lookup[sideLen - 1] = [sideLen - 2, sideLen * 2 - 1]  # top right
lookup[pzlSize - sideLen] = [pzlSize - sideLen + 1, pzlSize - 2 * sideLen]  # bottom left
lookup[pzlSize - 1] = [pzlSize - 2, pzlSize - sideLen - 1]  # bottom right
for n in range(pzlSize):
    if not lookup[n]:  # if not empty
        # edges
        if n < sideLen:  # top edge
            lookup[n] = [n - 1, n + sideLen, n + 1]
        elif n > pzlSize - sideLen:  # bottom edge
            lookup[n] = [n - 1, n + 1, n - sideLen]
        elif n % sideLen == 0:  # left edge
            lookup[n] = [n + sideLen, n + 1, n - sideLen]
        elif n % sideLen == sideLen - 1:  # right edge
            lookup[n] = [n - sideLen, n - 1, n + sideLen]
        else:  # center (has four neighbors)
            lookup[n] = [n - sideLen, n - 1, n + sideLen, n + 1]

# grid for manhattan distances
grid = {k:(k%sideLen,k//sideLen) for k in range(pzlSize)} #grid top left = (0,0)
# dict Δx + Δy for one swap
def getMnht(from_, to_):
    return abs((grid[from_][0]) - (grid[to_][0])) + (abs((grid[from_][1]) - (grid[to_][1])))
mnhtDict = {(from_, to_): getMnht(from_, to_) for to_ in range(pzlSize) for from_ in range(pzlSize)}


# helper methods
def solvable(puzzle, goal='_abcdefghijklmno'):
    inversions = len([item for sublist in[[k for k in puzzle[puzzle.find(n) + 1:] if k != '_' and n > k] for n in puzzle if n != '_'] for item in sublist])
    if sideLen % 2 == 0: #have to account for rows in even sided puzzles
        rowDifference = (puzzle.find('_') // sideLen - goal.find('_') // sideLen)
        return rowDifference % 2 == inversions % 2
    return inversions % 2 == 0

def mnhtPuzzle(puzzle, goal = '_abcdefghijklmno'):
    return sum([mnhtDict[puzzle.find(k), goal.find(k)] for k in puzzle if k != '_'])

def swapChars(num, space, puzzle):
    if num < space:
        return puzzle[0:num] + '_' + puzzle[num + 1: space] + puzzle[num] + puzzle[space + 1:]
    return puzzle[0:space] + puzzle[num] + puzzle[space + 1: num] + '_' + puzzle[num + 1:]

def neighbors(puzzle):
    space = puzzle.find('_')
    return [swapChars(num, space, puzzle) for num in lookup[space]]

def getPath(nbr,lvl,closedSet):
    pathList=[nbr]
    while lvl != 0:
        for n in neighbors(nbr):
            if n in closedSet and closedSet[n] == lvl - 1:
                nbr, lvl = n, closedSet[n]
                pathList.insert(0,nbr)
    return pathList


# A-star
def solve(puzzle, goal = '_abcdefghijklmno'):
    if puzzle == goal:
        return [puzzle]
    if not solvable(puzzle, goal):
        return []

    openSet = [(mnhtPuzzle(puzzle, goal), 0, puzzle)] # estimate, lvl, puzzle
    heapq.heapify(openSet)
    closedSet = {}

    while True:
        est, lvl, pzl = heapq.heappop(openSet)
        if pzl in closedSet:
            continue
        else:
            closedSet[pzl] = lvl

        for nbr in neighbors(pzl):
            if nbr == goal:
                return getPath(nbr, lvl + 1, closedSet)
            elif nbr in closedSet:
                continue
            else:
                newEst = lvl + 1 + mnhtPuzzle(nbr, goal)
                heapq.heappush(openSet, (newEst, lvl + 1, nbr))

pzlNum = 0
for pzl in file:
    if pzlNum == 52:
        quit()
    pzlNum += 1
    start = time.clock()
    if '0' in pzl:
        pzl = pzl[0:pzl.find('0')].lower() + '_' + pzl[pzl.find('0') + 1:].lower()
    printList = [n.find('_') for n in solve(pzl.strip(), goal)]
    elapsed = round(time.clock() - start, 3)
    print(pzl.strip(), ': ', len(printList) - 1, 'TIME:', elapsed, 'sec SEQUENCE:', printList) if printList else (pzl, 'is not solvable.')
