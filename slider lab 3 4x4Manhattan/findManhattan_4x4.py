import time
import random

start = time.clock()
puzzles = []
impossible = 0
stepCt = 0

grid = {} #4x4 grid w top left (0,0) and bottom right (3,3)
for k in range(16):
    grid[k] = [str(k//4),str(k%4)]

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

def mnhtDistTile(puzzle, goal, tile):
    tlAt = puzzle.find(tile)
    goTo = goal.find(tile)
    return (abs(int(grid[goTo][0])-int(grid[tlAt][0]))+(abs(int(grid[goTo][1])-int(grid[tlAt][1]))))

def mnhtPuzzle(puzzle, goal='abcdefghijklmno_'):
    dist = 0
    for k in puzzle:
        dist += mnhtDistTile(puzzle, goal, k)
    return dist

print(mnhtPuzzle('abcdefghijklmno_', 'oabcdefghijklmn_'))