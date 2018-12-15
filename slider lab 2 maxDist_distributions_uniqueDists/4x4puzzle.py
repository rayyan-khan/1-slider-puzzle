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
    for k in range(len(p)//10):
        for n in range(0, 10):
            print(p[k*10 + n][0:4], "   ", end = "")
        print("")
        for n in range(0, 10):
            print(p[k * 10 + n][4:8], "   ", end="")
        print("")
        for n in range(0, 10):
            print(p[k * 10 + n][8:12], "   ", end="")
        print("")
        for n in range(0, 10):
            print(p[k * 10 + n][12:], "   ", end="")
        print("\n", "\n")
    for n in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + n][0:4], "   ", end = "")
    print("")
    for n in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + n][4:8], "   ", end = "")
    print("")
    for n in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + n][8:12], "   ", end = "")
    print("")
    for n in range(0, len(p)%10):
        print(p[(len(p)//10)*10 + n][12:], "   ", end = "")
    print("")

def neighbors(s):
    space = s.find("_")
    lookup = [[1,4],[0,5,2],[1,6,3],[2,7],[0,5,8],[1,4,6,9],[2,5,7,10],[3,6,11],[4,9,12],[5,8,10,13],[6,9,11,14],[7,10,15],[8,13],[9,12,14],[10,13,15],[11,14]]
    neighbors = []
    for num in lookup[space]:
        newS = s[0:space] + s[num] + s[space + 1:]
        newS = newS[0:num] + "_" + newS[num + 1:]
        neighbors.append(newS)
    return neighbors

def solvable1(puzzle):
    inv = 0
    space = puzzle.find('_')
    for n in puzzle:
        for k in puzzle[puzzle.index(n):]:
            if n>k and n !='_' :
                inv = inv + 1
    return space%2==inv%2

def solvable(puzzle, goal = 'abcdefghijklmno_'):
    if(solvable1(puzzle) == solvable1(goal)):
        return True
    else:
        return False

def solve(puzzle, goal = 'abcdefghijklmno_'):
#    if solvable(puzzle, goal) == False:
#        return "No solution."
#    else:
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

def puzzlesPerDist(puzzle):
    p = Puzzle(puzzle,0)
    dictLevel = {0: [puzzle]}
    parseMe = [p]
    seen = set()
    seen.add(puzzle)
    while parseMe:
        puzz = parseMe.pop(0)
        if puzz.getLevel() == 20:
            return dictLevel
        for k in neighbors(puzz.getPuzzle()):
            if k not in seen:
                newPuzz = Puzzle(k, puzz.getLevel()+1)
                parseMe.append(newPuzz)
                seen.add(k)
                if newPuzz.getLevel() not in dictLevel:
                    dictLevel[newPuzz.getLevel()] = [k]
                else:
                    dictLevel[newPuzz.getLevel()].append(k)
    return dictLevel

dictLev = puzzlesPerDist('abcdefghijklmno_')
for k in dictLev:
    print('Level: ', k, ' # Puzzles: ', len(dictLev[k]))


print('TIME: ', time.clock()-start)