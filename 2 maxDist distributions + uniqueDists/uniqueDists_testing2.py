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

def puzzlesPerDist(puzzle='12345678_'):
    p = Puzzle(puzzle,0)
    dictLevel = {0: {puzzle}}
    dictPuzzles = {puzzle: [0]}
    dictParents = {puzzle:[]}
    parseMe = [p]
    r = 0
    sum = [0,0,0]
    while parseMe:
        puzz = parseMe.pop(0)
        newLevel = puzz.getLevel()
        puzzStr =puzz.getPuzzle()
        for k in neighbors(puzzStr):
            num = 0
            if k not in dictPuzzles:
                num += 1
                newPuzz = Puzzle(k, newLevel)
                parseMe.append(newPuzz)
                dictPuzzles[k] = [newLevel]
                if newPuzz.getLevel() not in dictLevel:
                    dictLevel[newPuzz.getLevel()] = {k}
                else:
                    dictLevel[newPuzz.getLevel()].add(k)
            else:
                try:
                    if newLevel in dictPuzzles[k]:
                        dictLevel[newLevel].remove(k)
                        parseMe.append(Puzzle(k, newLevel))
                        for x in neighbors(k):
                            if x not in dictPuzzles:
                                r += 1
                                if r > 78330:
                                    print(sum)
                                n = x.find('_')
                                if n in [0,2,6,8]:
                                    sum[0] +=1
                                elif n in [1,3,5,7]:
                                    sum[1] += 1
                                else:
                                    sum[2] +=1
                except:
                    pass
    return sum

dictParents = puzzlesPerDist("12345678_")
'''sum = 0
for k in dictLev:
    sum = sum + len(dictLev[k])
    print('Level: ', k, ' # Puzzles: ', len(dictLev[k]))

print('sum: ', sum)'''

'''sum = 0

print(len(dictParents['12345678_']))
for k in dictParents:
    if len(dictParents[k])>1:
        sum += 1
print(sum)'''
print(puzzlesPerDist())