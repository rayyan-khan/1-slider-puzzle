import time
import sys
import math

# bucket version

# working on improving neighbors method
# switch .append to comprehension
# same improvement already made to heapq version
# seems a little broken not sure why, but not trying to fix because decided not to use

file = open(sys.argv[1],'r') if len(sys.argv) == 2 else open('eckel.txt','r')
goal = file.readline().strip()

pzlSize = len(goal)
sideLen = int(math.sqrt(pzlSize))
#create lookup
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

#grid for manhattan distances -- coordinates
grid = {k:(k%sideLen,k//sideLen) for k in range(pzlSize)} #grid top left = (0,0)

# dict manhattan distance calculations
# dict = {(position from, position to): value of the manhattan distance}
def getMnht(from_, to_):
    return abs(int(grid[from_][0]) - int(grid[to_][0])) + (abs(int(grid[from_][1]) - int(grid[to_][1])))
mnhtDict = {(from_, to_): getMnht(from_, to_) for to_ in range(pzlSize) for from_ in range(pzlSize)}


#helper methods
def mnhtPuzzle(puzzle, goal = '_abcdefghijklmno'):
    return sum([mnhtDict[puzzle.find(k), goal.find(k)] for k in puzzle if k != '_'])

def swapChars(num, space, puzzle):
    if num < space:
        return puzzle[0:num] + '_' + puzzle[num + 1: space] + puzzle[num] + puzzle[space + 1:]
    return puzzle[0:space] + puzzle[num] + puzzle[space + 1: num] + '_' + puzzle[num + 1:]

def neighbors(puzzle):
    space = puzzle.find('_')
    return [swapChars(num, space, puzzle) for num in lookup[space]]

def solvable(puzzle, goal='_abcdefghijklmno'): #assumes side length 4
    inversions = len([item for sublist in[[k for k in puzzle[puzzle.find(n) + 1:] if k != '_' and n > k] for n in puzzle if n != '_'] for item in sublist])
    rowDifference = (puzzle.find('_') // 4 - goal.find('_') // 4)
    return rowDifference % 2 == inversions % 2

def getPath(nbr,lvl,closedSet):
    pathList=[nbr]
    while lvl != 0:
        for n in neighbors(nbr):
            if n in closedSet and closedSet[n] == lvl - 1:
                nbr, lvl = n, closedSet[n]
                pathList.insert(0,nbr)
    return pathList

def getPathRecursively(nbr, closedSet):
    lvl = closedSet[nbr]
    if lvl == 0:
        return [nbr]
    for n in neighbors(nbr):
        if n in closedSet and closedSet[n] == lvl - 1:
            return getPathRecursively(n, closedSet) + [nbr]

def solve(puzzle, goal = '_abcdefghijklmno'):
    if '0' in puzzle:
        puzzle = puzzle[0:puzzle.find('0')].lower()+'_'+puzzle[puzzle.find('0')+1:].lower()
    if puzzle == goal:
        return [puzzle]
    if not solvable(puzzle, goal):
        return []

    posInBucket = 0
    bucket = 0
    lvl = 0
    openSet = [[] for i in range(81)]
    openSet[0].append((lvl, puzzle)) #lvl, puzzle
    closedSet = {} #puzzle, level

    while openSet:
        if posInBucket < len(openSet[bucket]):
            lvl, pzl = openSet[bucket][posInBucket]
            posInBucket += 1
            if pzl in closedSet:
                continue
            closedSet[pzl] = lvl

            for nbr in neighbors(pzl):
                if nbr == goal:
                    closedSet[nbr] = lvl + 1
                    return getPathRecursively(nbr, closedSet)
                    #return getPath(nbr, lvl + 1, closedSet)
                if nbr in closedSet:
                    continue
                else:
                    openSet[mnhtPuzzle(pzl, goal) + lvl + 1].append((lvl + 1, nbr))
        else:
            openSet[bucket] = []
            bucket, posInBucket = bucket + 1, 0

for pzl in file:
    start = time.clock()
    printList = [n.find('_') for n in solve(pzl.strip())]
    elapsed = round(time.clock()-start,3)
    print(pzl.strip(),': ',len(printList)-1,'TIME:', elapsed,'sec SEQUENCE:', printList) if printList else (pzl,'is not solvable.')