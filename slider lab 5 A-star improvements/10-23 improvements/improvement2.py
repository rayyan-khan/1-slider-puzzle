import time
import sys
import heapq

# changes from 10/21:
# notes after trying - wow this attempt really didn't work:
# it took 36s for 21 vs 0.005s in the last version (improvement1)
# funny observation: was adding 1 or -1 to the estimate, not the updated manhattan
# distance. It still worked though, and makes sense in hindsight.

# trying mnhtUpdate
# thought: not all keys in updateMnht are actually possible, and I could probably
# get only those pairs by going through the lookup table. Want to fix in the
# future, just don't feel like it right now because that's not the focus.
# the same applied to mnhtDict -- currently, they've both got 256 keys when they really
# only need 2(4) + 3(8) + 4(4) = 48. Definitely want to do that next though, just
# because it doesn't make sense to include things you don't need.

file = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('eckel.txt', 'r')
goal = file.readline().strip()
if '0' in goal:
    goal = goal[0:goal.find('0')].lower() + '_' + goal[goal.find('0') + 1:].lower()

pzlSize = len(goal)
sideLen = int(pzlSize**.5)
goalSpace = goal.find('_')

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
grid = [(k%sideLen,k//sideLen) for k in range(pzlSize)] #grid top left = (0,0)

# dict Δx + Δy for one swap
def getMnht(from_, to_):
    return abs((grid[from_][0]) - (grid[to_][0])) + (abs((grid[from_][1]) - (grid[to_][1])))
mnhtDict = {(from_, to_): getMnht(from_, to_) for to_ in range(pzlSize) for from_ in range(pzlSize)}

# goalDict = {letter: index}
goalDict = {k[1]: k[0] for k in enumerate(goal)}

# updateMnht= {(from, to): +- 1} --> (+) if mnht dist increases, (-) if decreases
# change should eliminate need to constantly recalculate mnhtPuzzle
# maybe comprehension later but it'd be unpleasant and not really change anything
updateMnht = {}
for from_ in range(pzlSize):
    for to_ in range(pzlSize):
        if mnhtDict[(from_, goalSpace)] > mnhtDict[(to_, goalSpace)]:
            updateMnht[(from_, to_)] = -1
        else:
            updateMnht[(from_, to_)] = 1


# helper methods
def solvable(puzzle, goal='_abcdefghijklmno'):
    inversions = len([item for sublist in[[k for k in puzzle[puzzle.find(n) + 1:] if k != '_' and n > k] for n in puzzle if n != '_'] for item in sublist])
    if sideLen % 2 == 0: # have to account for rows in even sided puzzles
        rowDifference = (puzzle.find('_') // sideLen - goal.find('_') // sideLen)
        return rowDifference % 2 == inversions % 2
    return inversions % 2 == 0

def mnhtPuzzle(puzzle, goal = '_abcdefghijklmno'):
    return sum([mnhtDict[index, goalDict[ch]] for index, ch in enumerate(puzzle) if ch != '_'])

def swapChars(num, space, puzzle): # space = to_, num = from_
    if num < space:
        return puzzle[0:num] + '_' + puzzle[num + 1: space] + puzzle[num] + puzzle[space + 1:]
    return puzzle[0:space] + puzzle[num] + puzzle[space + 1: num] + '_' + puzzle[num + 1:]

def neighbors(puzzle, space):
    return [(swapChars(num, space, puzzle), num) for num in lookup[space]]
    # change is to store location of the space in a tuple with the neighbor so we don't need .find

def getPath(nbr,lvl,closedSet):
    #print(nbr, lvl, closedSet)
    pathList=[nbr]
    while lvl != 0:
        for n in neighbors(nbr, nbr.find('_')):
            nPzl = n[0] # neighbors returns a list like
                        # [(neighbor puzzle, space location), (pzl, space) etc]
            if nPzl in closedSet and closedSet[nPzl] == lvl - 1:
                nbr, lvl = nPzl, closedSet[nPzl]
                pathList.insert(0, nPzl)
    return pathList


# A-star
def solve(puzzle, goal = '_abcdefghijklmno'):
    if puzzle == goal:
        return [puzzle]
    if not solvable(puzzle, goal):
        return []

    space = puzzle.find('_')
    openSet = [(mnhtPuzzle(puzzle, goal), 0, (puzzle, space))] # estimate, lvl, (puzzle, its space)
    heapq.heapify(openSet)
    closedSet = {}

    while True:
        est, lvl, pzl = heapq.heappop(openSet)
        pzStr, space = pzl #pzl = puzzle string, space location
        if pzStr in closedSet: #only want to put the string in closedSet
            continue
        else:
            closedSet[pzStr] = lvl

        #print('here', pzStr, space)
        for nbr in neighbors(pzStr, space):
            nbrPzl, nbrSpace = nbr
            if nbrPzl == goal:
                return getPath(nbrPzl, lvl + 1, closedSet)
            elif nbrPzl in closedSet:
                continue
            else:
                #print('nbr', nbr, nbrPzl)
                newEst = lvl + 1 + updateMnht[space, nbrSpace]
                heapq.heappush(openSet, (newEst, lvl + 1, nbr))

lvl = 0
countTotalTime = time.clock()
for pzl in file:
    if lvl == 51:
        print('Time for 1 - 51: {}'.format(round(time.clock() - countTotalTime)))
    start = time.clock()
    if '0' in pzl:
        pzl = pzl[0:pzl.find('0')].lower() + '_' + pzl[pzl.find('0') + 1:].lower()
    printList = [n.find('_') for n in solve(pzl.strip(), goal)]
    elapsed = round(time.clock() - start, 3)
    lvl = len(printList) - 1
    print(pzl.strip(), ': ', lvl, 'TIME:', elapsed, 'sec SEQUENCE:', printList) if printList else (pzl, 'is not solvable.')
