import time
import sys
import math

def createLookup(s):
    sl = int(math.sqrt(len(s)))
    lookup = [[]] * len(s)
    # corners
    lookup[0] = [1, sl]  # top left
    lookup[sl - 1] = [sl - 2, sl * 2 - 1]  # top right
    lookup[len(s) - sl] = [len(s) - sl + 1, len(s) - 2 * sl]  # bottom left
    lookup[len(s) - 1] = [len(s) - 2, len(s) - sl - 1]  # bottom right
    for n in range(len(s)):
        if not lookup[n]:  # if not empty
            # edges
            if n < sl:  # top edge
                lookup[n] = [n - 1, n + sl, n + 1]
            elif n > len(s) - sl:  # bottom edge
                lookup[n] = [n - 1, n + 1, n - sl]
            elif n % sl == 0:  # left edge
                lookup[n] = [n + sl, n + 1, n - sl]
            elif n % sl == sl - 1:  # right edge
                lookup[n] = [n - sl, n - 1, n + sl]
            else:  # center (has four neighbors)
                lookup[n] = [n - sl, n - 1, n + sl, n + 1]
    return lookup

def neighbors(s,lookup):
    space = s.find("_")
    neighbors = []
    for num in lookup[space]:
        newS = s[0:space] + s[num] + s[space + 1:]
        neighbors.append(newS[0:num] + "_" + newS[num + 1:])
    return neighbors

def solvable(puzzle,goal='_abcdefghijklmno'): #assumes sidelen 4
    return (puzzle.find('_') // 4 - goal.find('_') // 4) % 2 == len([item for sublist in[[k for k in puzzle[puzzle.find(n) + 1:] if k != '_' and n > k] for n in puzzle if n != '_'] for item in sublist])%2

def mnhtDistTile(puzzle, goal, tile): #grid top left = (0,0), return abs(Δy)+abs(Δx) for single tile
    sideLen = int(math.sqrt(len(puzzle)))
    grid = {k:[k%sideLen,k//sideLen] for k in range(len(puzzle))}
    pos = (puzzle.find(tile), goal.find(tile))
    return (abs(int(grid[pos[1]][0]) - int(grid[pos[0]][0])) + (abs(int(grid[pos[1]][1]) - int(grid[pos[0]][1]))))

def mnhtPuzzle(puzzle, goal='_abcdefghijklmno'):
    return sum([mnhtDistTile(puzzle, goal, k) for k in puzzle if k != '_'])

def getPath(nbr,lvl,closedSet):
    pathList=[nbr]
    lookup = createLookup(nbr)
    while(lvl != 0):
        for n in neighbors(nbr,lookup):
            if n in closedSet and closedSet[n] == lvl-1:
                nbr, lvl = n, closedSet[n]
                pathList.insert(0,nbr)
    return pathList

def solve(puzzle, goal = '_abcdefghijklmno'):
    if '0' in puzzle: puzzle = puzzle[0:puzzle.find('0')].lower()+'_'+puzzle[puzzle.find('0')+1:].lower()
    if puzzle==goal: return [puzzle]
    if not solvable(puzzle, goal): return []

    pos = 0
    est = mnhtPuzzle(puzzle,goal)
    lookup = createLookup(puzzle)
    openSet = [(est,0,puzzle)]#estimate, level, puzzle
    closedSet = {}

    while openSet:
        if est != openSet[0][0]:
            openSet[:pos] = []
            openSet.sort()
            pos = 0
        est2, lvl, pzl = openSet[pos]
        pos+=1
        if pzl in closedSet: continue
        else: closedSet[pzl] = lvl
        for nbr in neighbors(pzl,lookup):
            if nbr == goal: return getPath(nbr,lvl+1,closedSet)
            if nbr in closedSet: continue
            else:
                est = lvl+1+mnhtPuzzle(nbr,goal)
                openSet.append((est,lvl+1,nbr))
    return []

for pzl in open('eckel.txt','r'): #change file to sys.argv[1] when done
    start = time.clock()
    printList = [n.find('_') for n in solve(pzl.strip())]
    elapsed = round(time.clock()-start,3)
    print(pzl.strip(),': ',len(printList)-1,'TIME:', elapsed,'sec SEQUENCE:', printList) if printList else (pzl,'is not solvable.')