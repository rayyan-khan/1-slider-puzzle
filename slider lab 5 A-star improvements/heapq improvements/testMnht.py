import time
import sys
import math
import heapq

#helper methods from Astar3, solve from Astar1, replaced PQ with heapq

file = open(sys.argv[1],'r') if len(sys.argv) == 2 else open('eckel.txt','r')
goal = file.readline().strip()

pzlSize = len(goal)
sideLen = int(math.sqrt(pzlSize))
#create lookup
lookup = [[]] * pzlSize
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

#grid for manhattan distances
grid = {k:(k%sideLen,k//sideLen) for k in range(pzlSize)} #grid top left = (0,0)

mnhtDict = {} # mnhtDict = {(from, to): manhattan distance}
for from_ in range(pzlSize): #come back and see if can be comprehension
    for to_ in range(pzlSize):
        mnhtDict[(from_,to_)] = abs(int(grid[from_][0]) - int(grid[to_][0])) + (abs(int(grid[from_][1]) - int(grid[to_][1])))

print('MNHTDICT', mnhtDict)

def mnhtPuzzle(puzzle, goal='_abcdefghijklmno'): #see if work then comprehension
    mnht = 0
    for k in puzzle:
        if k != '_':
            pos = (puzzle.find(k), goal.find(k))
            mnht += mnhtDict[pos]
    return mnht

def mnhtDistTile1(puzzle, goal, tile):
    pos = (puzzle.find(tile), goal.find(tile))
    print('T:', tile, ':', abs(int(grid[pos[1]][0]) - int(grid[pos[0]][0])) + (abs(int(grid[pos[1]][1]) - int(grid[pos[0]][1]))))
    return (abs(int(grid[pos[1]][0]) - int(grid[pos[0]][0])) + (abs(int(grid[pos[1]][1]) - int(grid[pos[0]][1]))))

def mnhtPuzzle1(puzzle, goal='_abcdefghijklmno'):
    return sum([mnhtDistTile1(puzzle, goal, k) for k in puzzle if k != '_'])

def neighbors(puzzle):
    space = puzzle.find("_")
    neighbors = []
    for num in lookup[space]:
        newS = puzzle[0:space] + puzzle[num] + puzzle[space + 1:]
        neighbors.append(newS[0:num] + "_" + newS[num + 1:])
    return neighbors

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
    if puzzle==goal:
        return [puzzle]
    if solvable(puzzle, goal) == False:
        return ['1']

    openSet = [(mnhtPuzzle(puzzle,goal),0,puzzle)]#estimate, lvl, puzzle
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
                return getPath(nbr,lvl+1,closedSet)
            elif nbr in closedSet:
                continue
            else:
                newEst = lvl+1+mnhtPuzzle(nbr,goal)
                heapq.heappush(openSet, (newEst,lvl+1,nbr))

pzl = 'AH0GDECKLBJFIMNO'
pzl = pzl[0:pzl.find('0')].lower() + '_' + pzl[pzl.find('0') + 1:].lower()
print('New:', mnhtPuzzle(pzl))
print('Old:', mnhtPuzzle1(pzl))

