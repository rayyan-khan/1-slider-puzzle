import time
import random
import math
from queue import PriorityQueue

start = time.clock()
puzzles = []
impossible = 0
stepCt = 0

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

def printList(p): #not working
    sl = int(math.sqrt(len(p))) #side length
    for k in range(len(p)//10):
        for x in range(sl):
            for n in range(0, 10):
                print(p[k*10 + n][sl*x:sl*(x+1)], "   ", end = "")
            print("")
    for n in range(0, len(p)%10):
        for m in range(sl):
            print(p[(len(p)//10)*10 + n][sl*m:sl*(m+1)], "   ", end = "")
        print("")

def createLookup(s):
    sl = int(math.sqrt(len(s)))
    lookup = [[]]*len(s)
    #corners
    lookup[0] = [1,sl] #top left
    lookup[sl-1] = [sl-2,sl*2-1] #top right
    lookup[len(s)-sl] = [len(s)-sl+1,len(s)-2*sl] #bottom left
    lookup[len(s)-1] = [len(s)-2,len(s)-sl-1]#bottom right
    for n in range(len(s)):
        if not lookup[n]: #if not empty
            #edges
            if n<sl: #top edge
                lookup[n] = [n-1,n+sl,n+1] #ctr clockwise (no reason)
            elif n>len(s)-sl:#bottom edge
                lookup[n]=[n-1,n+1,n-sl]
            elif n%sl==0:#left edge
                lookup[n]=[n+sl,n+1,n-sl]
            elif n%sl==sl-1:#right edge
                lookup[n]=[n-sl,n-1,n+sl]
            else:#center (has four neighbors)
                lookup[n]=[n-sl,n-1,n+sl,n+1]
    return lookup

def neighbors(s,lookup):
    space = s.find("_")
    neighbors = []
    newS=''
    for num in lookup[space]:
        try:
            newS = s[0:space] + s[num] + s[space + 1:]
            newS = newS[0:num] + "_" + newS[num + 1:]
        except:
            print(s,space,num,lookup[space])
        neighbors.append(newS)
    return neighbors

def solvable1(puzzle):
    inv = 0
    if int(math.sqrt(len(puzzle)))%2==0:
        for n in puzzle:
            for k in puzzle[puzzle.index(n):]:
                if n>k and n !='_' :
                    inv = inv + 1
        if len(puzzle)%2==0:
            return puzzle.find('_')%2==inv%2
        else:
            return inv%2==0

def solvable(puzzle, goal = 'abcdefghijklmno_'):
    if(solvable1(puzzle) == solvable1(goal)):
        return True
    else:
        return False

def solve(puzzle, goal = 'abcdefghijklmno_'):
    if solvable(puzzle, goal) == False:
        return "No solution."
    else:
        lookup = createLookup(puzzle)
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
                for k in neighbors(puzzStr,lookup):
                    if k not in dictSeen:
                        parseMe.put(Puzzle(k, mnhtPuzzle(k,goal)))
                        dictSeen[k] = puzzStr
        return "No solution."

def mnhtDistTile(puzzle, goal, tile):
    grid = {}  #top left = (0,0)
    sideLen = int(math.sqrt(len(puzzle)))
    for k in range(len(puzzle)):
        grid[k] = [k%sideLen, k//sideLen]
    tlAt = puzzle.find(tile)
    goTo = goal.find(tile)
    return (abs(int(grid[goTo][0]) - int(grid[tlAt][0])) + (abs(int(grid[goTo][1]) - int(grid[tlAt][1]))))

def mnhtPuzzle(puzzle, goal='abcdefghijklmno_'):
    dist = 0
    for k in puzzle:
        dist += mnhtDistTile(puzzle, goal, k)
    return dist

pzlist=['abcdefghijklmno_', 'abcdefghijk_mnol', 'abcdefg_ijkhmnol', 'abc_efgdijkhmnol', 'ab_cefgdijkhmnol', 'a_bcefgdijkhmnol', '_abcefgdijkhmnol', 'eabc_fgdijkhmnol', 'eabcf_gdijkhmnol', 'e_bcfagdijkhmnol', '_ebcfagdijkhmnol', 'febc_agdijkhmnol', 'febciagd_jkhmnol', 'febciagdj_khmnol', 'febci_gdjakhmnol', 'f_bciegdjakhmnol', '_fbciegdjakhmnol', 'ifbc_egdjakhmnol', 'ifbce_gdjakhmnol']
for n in range(len(pzlist)):
    start = time.clock()
    ln = len(solve(pzlist[n]))
    print('Distance:', n, 'length: ', ln,'Time:',time.clock()-start)

'''
#print(len(solve('_fcdbelgjaokinmh')))
start = time.clock()
x = len(solve('_87654321','12345678_'))
finish3s=time.clock()
print('path', x, 'time 3x3:',finish3s-start)
x = len(solve('oabcdefghijklmn_'))
finish4s=time.clock()
print('path', x, 'time 4x4:',finish4s-finish3s)
x = len(solve('abcdefghijklmnopqrs_tuvwx','abcdefghijklmnopqrstuvwx_'))
finish5s=time.clock()
print('path', x, 'time 5x5:',finish5s-finish4s)
#print(mnhtPuzzle('8672543_1','12345678_'))
'''

'''
Distance: 0 length:  1 Time: 0.003355730469776666
Distance: 1 length:  12 Time: 8.447992791046129e-05
Distance: 2 length:  3 Time: 0.0012582389263027832
Distance: 3 length:  12 Time: 7.551993555632124e-05
Distance: 4 length:  12 Time: 7.167993883311873e-05
Distance: 5 length:  12 Time: 7.253327143827513e-05
Distance: 6 length:  12 Time: 7.167993883311873e-05
Distance: 7 length:  8 Time: 0.024353259218552133
Distance: 8 length:  9 Time: 0.02908925517716892
Distance: 9 length:  12 Time: 7.850659967436474e-05
Distance: 10 length:  12 Time: 7.039993992538629e-05
Distance: 11 length:  292 Time: 2.6402729469670856
Distance: 12 length:  12 Time: 5.2479955217066276e-05
Distance: 13 length:  12 Time: 4.3093296560492433e-05
Distance: 14 length:  15 Time: 0.2574504469756187
Distance: 15 length:  12 Time: 4.8639958493801316e-05
Distance: 16 length:  12 Time: 4.266663025775941e-05
Distance: 17 length:  334 Time: 14.393939717171442
Distance: 18 length:  239 Time: 2.98014167027911
'''