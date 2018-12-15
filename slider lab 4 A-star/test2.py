import time
import math
import sys
from queue import PriorityQueue
def createLookup(s): #returned by method in slider lab 3 files, but only using 4x4 puzzles rn
    return [[1, 4], [0, 5, 2], [1, 6, 3], [2, 7], [8, 5, 0], [1, 4, 9, 6], [2, 5, 10, 7], [3, 6, 11], [12, 9, 4], [5, 8, 13, 10], [6, 9, 14, 11], [7, 10, 15], [13, 8], [12, 14, 9], [13, 15, 10], [14, 11]]
def neighbors(s,lookup):
    space = s.find("_")
    neighbors = []
    for num in lookup[space]:
        newS = s[0:space] + s[num] + s[space + 1:]
        neighbors.append(newS[0:num] + "_" + newS[num + 1:])
    return neighbors
def solvable(puzzle,goal='_abcdefghijklmno'): #assumes sidelen 4
    return (puzzle.find('_') // 4 - goal.find('_') // 4) % 2 == len([item for sublist in[[k for k in puzzle[puzzle.find(n) + 1:] if k != '_' and n > k] for n in puzzle if n != '_'] for item in sublist]) % 2
def mnhtDistTile(puzzle, goal, tile): #grid top left = (0,0), return abs(Δy)+abs(Δx) for single tile
    sideLen = int(math.sqrt(len(puzzle)))
    grid = {k:[k%sideLen,k//sideLen] for k in range(len(puzzle))}
    pos = (puzzle.find(tile), goal.find(tile))
    return (abs(int(grid[pos[1]][0]) - int(grid[pos[0]][0])) + (abs(int(grid[pos[1]][1]) - int(grid[pos[0]][1]))))
def mnhtPuzzle(puzzle, goal='_abcdefghijklmno'): #mnht dist puzzle = sum mnht distances of tiles
    return sum([mnhtDistTile(puzzle,goal,k) for k in puzzle if k!='_'])
def getPath(nbr,lvl,closedSet):
    pathList=[nbr]
    lookup=createLookup(nbr)
    while(lvl != 0):
        for n in neighbors(nbr,lookup):
            if n in closedSet and closedSet[n]==lvl-1:
                nbr, lvl = n, closedSet[n]
                pathList.insert(0,nbr)
    return pathList

def solve(puzzle, goal = '_abcdefghijklmno'):
    if '0' in puzzle: puzzle = puzzle[0:puzzle.find('0')].lower()+'_'+puzzle[puzzle.find('0')+1:].lower()
    if puzzle==goal: return [puzzle]
    if not solvable(puzzle, goal): return []
    lookup = createLookup(puzzle)
    openSet = PriorityQueue() #parseMe
    openSet.put((mnhtPuzzle(puzzle,goal),0,puzzle))#PQ: estimate, level, puzzle
    closedSet = {}
    if puzzle == goal:
        return [puzzle]
    while openSet:
        est, lvl, pzl = openSet._get()
        if pzl in closedSet:
            continue
        else:
            closedSet[pzl] = lvl
        for nbr in neighbors(pzl,lookup):
            if nbr == goal:
                return getPath(nbr,lvl+1,closedSet)
            elif nbr in closedSet:
                continue
            else:
                newEst = lvl+1+mnhtPuzzle(nbr,goal)
                openSet.put((newEst,lvl+1,nbr))
    return []

for pzl in open('eckel.txt','r'):
    start = time.clock()
    printList = [n.find('_') for n in solve(pzl.strip())]
    elapsed = round(time.clock()-start,3)
    print(pzl.strip(),':',len(printList)-1,'TIME:', elapsed,'sec SEQUENCE:', printList) if printList else (pzl,'is not solvable.')