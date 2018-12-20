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

def puzzlesPerDist(puzzle):
    p = Puzzle(puzzle,0)
    dictLevel = {0: {puzzle}}
    dictPuzzles = {puzzle: [0]}
    parseMe = [p]
    while parseMe:
        puzz = parseMe.pop(0)
        newLevel = puzz.getLevel()+1
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
                    if newLevel in dictPuzzles[k]: #try-except to work around this while I try to understand why
                        dictLevel[newLevel].remove(k)
                        parseMe.append(Puzzle(k, newLevel))
                except:
                    pass
    return dictLevel


dictLev = puzzlesPerDist("12345678_")
sum = 0
for k in dictLev:
    sum = sum + len(dictLev[k])
    print('Level: ', k, ' # Puzzles: ', len(dictLev[k]))

print('sum: ', sum)