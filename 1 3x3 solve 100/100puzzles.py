import time
import sys
import random

start = time.clock()
puzzles = []
impossible = 0
stepCt = 0

def shuffleStr(s):
    chars = list(s)
    random.shuffle(chars)
    return ''.join(chars)

def printList(p):
    print('\n')
    if p == "No solution.":
        print(p)
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
    lookup = [[1,3],[0,2,4],[1,5],[0,4],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]]
    neighbors = []
    for i in lookup[space]:
        newS = s[0:space] + s[i] + s[space + 1:]
        newS = newS[0:i] + "_" + newS[i+1:]
        neighbors.append(newS)
    return neighbors

def solvable(puzzle):
    inv = 0
    for n in puzzle:
        for k in puzzle[puzzle.index(n):]:
            if n>k and n !='_' :
                inv = inv + 1
    if inv%2==0:
        return True
    else:
        return False

def solve(puzzle, goal = "12345678_"):
#    if goal == "12345678_" and solvable(puzzle) == False:
#        return "No solution."
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

for n in range(0, 100):
    puzzles.append(shuffleStr("12345678_"))

while puzzles:
    s = solve(puzzles.pop())
    if s == "No solution.":
        impossible = impossible + 1
    else:
        stepCt = stepCt + len(s)

print("Time: ", time.clock()-start)
print("Impossible puzzles: ", impossible)
print("Average solution length: ", stepCt/100)