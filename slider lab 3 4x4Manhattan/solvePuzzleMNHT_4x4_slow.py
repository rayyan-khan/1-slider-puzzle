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
            puzzStr = parseMe._get().getPuzzle()
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

'''
#print(solve('_fcdbelgjaokinmh'))
p = solve('oabcdefghijklmn_')
printList(p)
print('length:',len(p))
print('Time:', time.clock()-start)
'''

'''
Distance: 0 1 Time: 8.447992791046152e-05
Distance: 1 12 Time: 3.583996941655942e-05
Distance: 2 3 Time: 0.0005747195095726851
Distance: 3 12 Time: 3.669330202171566e-05
Distance: 4 12 Time: 3.285330529851282e-05
Distance: 5 12 Time: 3.285330529851282e-05
Distance: 6 12 Time: 3.1999972693356636e-05
Distance: 7 8 Time: 0.006366287900767658
Distance: 8 9 Time: 0.01263785588236298
Distance: 9 12 Time: 6.698660950476068e-05
Distance: 10 12 Time: 6.101328126866673e-05
Distance: 11 292 Time: 2.2938877492157874
Distance: 12 12 Time: 5.119995630931129e-05
Distance: 13 12 Time: 4.3093296560492433e-05
Distance: 14 15 Time: 0.32320868419525617
Distance: 15 12 Time: 4.266663025775941e-05
Distance: 16 12 Time: 3.541330311396251e-05
Distance: 17 334 Time: 10.454017319238554
Distance: 18 239 Time: 2.550482303588433
'''