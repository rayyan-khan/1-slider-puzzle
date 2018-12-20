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

def solve(puzzle, goal = 'abcdefghijklmno_'):
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

def mnhtDistTile(puzzle, goal, tile):
    tlAt = puzzle.find(tile)
    goTo = goal.find(tile)
    return (abs(int(grid[goTo][0]) - int(grid[tlAt][0])) + (abs(int(grid[goTo][1]) - int(grid[tlAt][1]))))

def mnhtPuzzle(puzzle, goal='abcdefghijklmno_'):
    dist = 0
    for k in puzzle:
        dist += mnhtDistTile(puzzle, goal, k)
    return dist

def puzzlesPerDist(puzzle):
    p = Puzzle(puzzle,0)
    dictLevel = {0: [puzzle]}
    parseMe = [p]
    seen = set()
    seen.add(puzzle)
    while parseMe:
        puzz = parseMe.pop(0)
        if puzz.getLevel() == 15:
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

pzlist=['abcdefghijklmno_', 'abcdefghijk_mnol', 'abcdefg_ijkhmnol', 'abc_efgdijkhmnol', 'ab_cefgdijkhmnol', 'a_bcefgdijkhmnol', '_abcefgdijkhmnol', 'eabc_fgdijkhmnol', 'eabcf_gdijkhmnol', 'e_bcfagdijkhmnol', '_ebcfagdijkhmnol', 'febc_agdijkhmnol', 'febciagd_jkhmnol', 'febciagdj_khmnol', 'febci_gdjakhmnol', 'f_bciegdjakhmnol', '_fbciegdjakhmnol', 'ifbc_egdjakhmnol', 'ifbce_gdjakhmnol']
for n in range(len(pzlist)):
    start = time.clock()
    ln = len(solve(pzlist[n]))
    print('Distance:',n,ln,'Time:',time.clock()-start)

'''
Distance: 0 1 Time: 2.986664118046616e-06
Distance: 1 2 Time: 3.9253299837184146e-05
Distance: 2 3 Time: 7.637326816147785e-05
Distance: 3 4 Time: 0.00022186647734060599
Distance: 4 5 Time: 0.00042239963955230755
Distance: 5 6 Time: 0.0009454925265130441
Distance: 6 7 Time: 0.0010534391010653004
Distance: 7 8 Time: 0.0027276776723817197
Distance: 8 9 Time: 0.005544101935699681
Distance: 9 10 Time: 0.010034338104031485
Distance: 10 11 Time: 0.013713908297464918
Distance: 11 12 Time: 0.033960504353702944
Distance: 12 13 Time: 0.07225679167420444
Distance: 13 14 Time: 0.3079617638726282
Distance: 14 15 Time: 1.0978810898081366
Distance: 15 16 Time: 1.9382511460256886
Distance: 16 17 Time: 2.755739941768583
Distance: 17 18 Time: 9.898186326881003
Distance: 18 19 Time: 96.94716036508983
'''