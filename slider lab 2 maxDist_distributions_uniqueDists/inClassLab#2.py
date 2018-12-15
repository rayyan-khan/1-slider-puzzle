import time
import random

start = time.clock()
puzzles = []
impossible = 0
stepCt = 0

class Puzzle():
    puzzle = ''
    level = 0

    def __init__(self, puzzle, level):
        self.puzzle = puzzle
        self.level = level

    def getPuzzle(self):
        return self.puzzle

    def getLevel(self):
        return self.level

def shuffleStr(s):
    chars = list(s)
    random.shuffle(chars)
    return ''.join(chars)

def printList(p):
    print('\n')
    for k in range(len(p)//10):
        for n in range(0, 10):
            print(p[k*10 + n][0:3], "   ", end = "")
        print("")
        for m in range(0, 10):
            print(p[k * 10 + m][3:6], "   ", end="")
        print("")
        for o in range(0, 10):
            print(p[k * 10 + o][6:], "   ", end="")
        print("\n", "\n")
    for r in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + r][0:3], "   ", end = "")
    print("")
    for r in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + r][3:6], "   ", end = "")
    print("")
    for r in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + r][6:], "   ", end = "")
    print("")

def neighbors(s):
    space = s.find("_")
    lookup = [[1,3],[0,2,4],[1,5],[0,4,6],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]]
    neighbors = []
    for i in lookup[space]:
        newS = s[0:space] + s[i] + s[space + 1:]
        newS = newS[0:i] + "_" + newS[i+1:]
        neighbors.append(newS)
    return neighbors

def solvable1(puzzle):
    inv = 0
    for n in puzzle:
        for k in puzzle[puzzle.index(n):]:
            if n>k and n !='_' :
                inv = inv + 1
    return inv%2

def solvable(puzzle, goal = '12345678_'):
    if(solvable1(puzzle) == solvable1(goal)):
        return True
    else:
        return False

def solve(puzzle, goal = "12345678_"):
    if solvable(puzzle, goal) == False:
        return "No solution."
    else:
        parseMe = [puzzle]
        dictSeen = {puzzle: ''}
        pathList = []
        if puzzle == goal:
            return [puzzle]
        while parseMe:
            puzz = parseMe.pop(0)
            if puzz == goal:
                key = puzz
                while key != '':
                    pathList.insert(0, key)
                    key = dictSeen[key]
                return pathList
            else:
                for k in neighbors(puzz):
                    if k not in dictSeen:
                        parseMe.append(k)
                        dictSeen[k] = puzz
        return "No solution."

def maxDist(puzzle):
    parseMe = [puzzle]
    dictSeen = {puzzle: ''}
    pathList = []
    while parseMe:
        puzz = parseMe.pop(0)
        for k in neighbors(puzz):
            if k not in dictSeen:
                parseMe.append(k)
                dictSeen[k] = puzz
    while puzz != '':
        pathList.insert(0, puzz)
        puzz = dictSeen[puzz]
    return pathList

for n in range(0, 100):
    puzzles.append(shuffleStr("12345678_"))

def puzzlesPerDist(puzzle='12345678_'):
    dictPuzzles = {puzzle:[0, 1]} #level, number of shorter paths
    parseMe = [puzzle]
    while parseMe:
        puzz = parseMe.pop(0)
        for k in neighbors(puzz):
            if k not in dictPuzzles:
                dictPuzzles[k] = [dictPuzzles[puzz][0]+1, 0]
                parseMe.append(k)
            if dictPuzzles[k][0] > dictPuzzles[puzz][0]:
                dictPuzzles[k][1] += 1
    return dictPuzzles

def parents(pzl, dctSeen):
    return[nbr for nbr in neighbors(pzl) if nbr in dctSeen and dctSeen[nbr][0]+1==dctSeen[pzl][0]]

def location(pzl):
    space = k.find('_')
    if space in {1, 3, 5, 7}:
        return 3
    elif space in {0, 2, 6, 8}:
        return 2
    else:
        return 4

def location1(k):
    return k.find('_') if k.find('_') == 4 else 2+k.find('_')%2

print(location1('_12345678'))
print(location1('1234_5678'))
print(location1('1_2345678'))

corners = 0
edges = 0
center = 0
d = puzzlesPerDist()

for k in d:
    print('{}: {}'.format(k, d[k]))

for k in d:
    if d[k][1] > 1:
        space = k.find('_')
        if space in [1,3,5,7]:
            edges += 1
        elif space in [0,2,6,8]:
            corners += 1
        else:
            center += 1

print('edges', edges)
print('corners', corners)
print('center', center)

