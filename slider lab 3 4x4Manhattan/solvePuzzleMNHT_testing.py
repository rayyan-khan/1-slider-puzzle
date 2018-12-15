import time
import random
from queue import PriorityQueue

start = time.clock()
puzzles = []
impossible = 0
stepCt = 0

grid = {} #4x4 grid w top left (0,0) and bottom right (3,3)
for k in range(16):
    grid[k] = str(k//4)+str(k%4)

class Puzzle():
    puzzle = ''
    level = 0
    mnhtDist = 0

    def __init__(self, puzzle, mnhtDist):
        self.puzzle = puzzle
        self.mnhtDist = mnhtDist

    def __lt__(self, other):
        return self.mnhtDist < other.mnhtDist

    def getPuzzle(self):
        return self.puzzle

    def getLevel(self):
        return self.level

    def getMnht(self):
        return self.mnhtDist

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
#    print('inv = ', inv)
    if space%2==inv%2:
        return 1
    else:
        return 0

def solvable(puzzle, goal = 'abcdefghijklmno_'):
    if(solvable1(puzzle) == solvable1(goal)):
        return True
    else:
        return False

def solve(puzzle, goal = 'abcdefghijklmno_'):
    if solvable(puzzle, goal) == False:
        return "No solution."
    else:
        pzl = Puzzle(puzzle,0)
        parseMe = PriorityQueue()
        parseMe.put(pzl)
        dictSeen = {puzzle: ''}
        pathList = []
        if puzzle == goal:
            return [puzzle]
        while parseMe:
            last = mnhtPuzzle(puzzle)
            puzz = parseMe._get()
            current = puzz.getMnht()
            puzzStr = puzz.getPuzzle()
            if puzzStr==goal:
                key = puzzStr
                while key != '':
                    pathList.insert(0, key)
                    key = dictSeen[key]
                return pathList
            else:
                for k in neighbors(puzzStr):
                    if k not in dictSeen:
                        parseMe.put(Puzzle(k, mnhtPuzzle(k)))
                        dictSeen[k] = puzzStr
        return "No solution."

def mnhtDistTile(puzzle, goal, tile):
    tlAt = puzzle.find(tile)
    goTo = goal.find(tile)
    return (abs(int(grid[goTo][0]) - int(grid[tlAt][0])) + (abs(int(grid[goTo][1]) - int(grid[tlAt][1]))))

def mnhtPuzzle(puzzle, goal='abcdefghijklmno_'):
    dist = 0
    for k in puzzle:
        dist += mnhtDistTile(puzzle, goal, k)
    return dist

#print(solve('_fcdbelgjaokinmh'))
p = solve('oabcdefghijklmn_')
printList(p)
print('length:',len(p))
print('Time:', time.clock()-start)