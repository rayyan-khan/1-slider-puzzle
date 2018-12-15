import time
import math
import sys
from queue import PriorityQueue

start = time.clock()

def createLookup(s):
    sl = int(math.sqrt(len(s)))
    lookup = [[]]*len(s)
    #corners
    lookup[0] = [1,sl] #top left
    lookup[sl-1] = [sl-2,sl*2-1] #top right
    lookup[len(s)-sl] = [len(s)-sl+1,len(s)-2*sl] #bottom left
    lookup[len(s)-1] = [len(s)-2,len(s)-sl-1]#bottom right
    for n in range(len(s)):
        if not lookup[n]: #if not empty
            #edges
            if n<sl: #top edge
                lookup[n] = [n-1,n+sl,n+1] #ctr clockwise (no reason)
            elif n>len(s)-sl:#bottom edge
                lookup[n]=[n-1,n+1,n-sl]
            elif n%sl==0:#left edge
                lookup[n]=[n+sl,n+1,n-sl]
            elif n%sl==sl-1:#right edge
                lookup[n]=[n-sl,n-1,n+sl]
            else:#center (has four neighbors)
                lookup[n]=[n-sl,n-1,n+sl,n+1]
    return lookup

def neighbors(s,lookup):
    space = s.find("_")
    neighbors = []
    newS=''
    for num in lookup[space]:
        try:
            newS = s[0:space] + s[num] + s[space + 1:]
            newS = newS[0:num] + "_" + newS[num + 1:]
        except:
            print(s,space,num,lookup[space])
        neighbors.append(newS)
    return neighbors

def solvable(puzzle,goal='_abcdefghijklmno'): #assumes sidelen 4
    inv=0
    for n in puzzle:
        if n !='_':
            for k in puzzle[puzzle.find(n)+1:]:
                if k!='_' and n>k:
                    inv+=1
    return (puzzle.find('_')//4 - goal.find('_')//4)%2==inv%2

def getPath(nbr,lvl,closedSet):
    pathList=[nbr]
    lookup=createLookup(nbr)
    while(lvl != 0):
        for n in neighbors(nbr,lookup):
            if n in closedSet and closedSet[n]==lvl-1:
                nbr = n
                lvl = closedSet[n]
                pathList.insert(0,nbr)
    return pathList

def solve(puzzle, goal = '_abcdefghijklmno'):
    if '0' in puzzle: puzzle = puzzle[0:puzzle.find('0')].lower()+'_'+puzzle[puzzle.find('0')+1:].lower()
    if puzzle==goal:
        return [puzzle]
    elif solvable(puzzle, goal) == False:
        return []
    else:
        lookup = createLookup(puzzle)
        openSet = PriorityQueue() #parseMe
        openSet.put((mnhtPuzzle(puzzle,goal),0,puzzle))#PQ: estimate, level, puzzle
        closedSet = {} #dictSeen but not
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

def mnhtDistTile(puzzle, goal, tile):
    grid = {}  #top left = (0,0)
    sideLen = int(math.sqrt(len(puzzle)))
    for k in range(len(puzzle)):
        grid[k] = [k%sideLen, k//sideLen]
    tlAt = puzzle.find(tile)
    goTo = goal.find(tile)
    return (abs(int(grid[goTo][0]) - int(grid[tlAt][0])) + (abs(int(grid[goTo][1]) - int(grid[tlAt][1]))))

def mnhtPuzzle(puzzle, goal='_abcdefghijklmno'):
    dist = 0
    for k in puzzle:
        if k != '_':
            dist += mnhtDistTile(puzzle, goal, k)
    return dist

print(mnhtPuzzle('AEBCD_FGHIJKLMNO'.lower()))