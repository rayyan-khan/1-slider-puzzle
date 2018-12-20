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

def puzzlesPerDist(puzzle):
    p = Puzzle(puzzle,0) #puzzle class including the puzzle state and its level
    dictLevel = {0: {puzzle}} #level: list of puzzles at that level
    dictPuzzles = {puzzle: [0]} #puzzle and list of levels it may be found at
    parseMe = [p]
    while parseMe:
        puzz = parseMe.pop(0)
        newLevel = puzz.getLevel()+1 #level for each neighbor one more than the level of its parent
        for k in neighbors(puzz.getPuzzle()):
            if k not in dictPuzzles:
                newPuzz = Puzzle(k, newLevel)
                parseMe.append(newPuzz)
                dictPuzzles[k] = [newLevel]
                if newPuzz.getLevel() not in dictLevel:
                    dictLevel[newPuzz.getLevel()] = {k}
                else:
                    dictLevel[newPuzz.getLevel()].add(k)
            else:
                try: #receiving a KeyError:4132_8765 -- confusing because the key is supposed to be the newLevel
                    if newLevel in dictPuzzles[k]: #try-except to work around this while I try to understand
                        dictLevel[newLevel].remove(k)
                        parseMe.append(Puzzle(k, newLevel))
                except:
                    print('k:', k, 'newLevel:', newLevel)
    return dictLevel


dictLev = puzzlesPerDist("12345678_")
sum = 0
for k in dictLev:
    sum = sum + len(dictLev[k])
    print('Level: ', k, ' # Puzzles: ', len(dictLev[k]))

print('sum: ', sum)


