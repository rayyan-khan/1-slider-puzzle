import time
import math
import sys
from queue import PriorityQueue

start = time.clock()

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
    for num in lookup[space]:
        newS = s[0:space] + s[num] + s[space + 1:]
        newS = newS[0:num] + "_" + newS[num + 1:]
        neighbors.append(newS)
    return neighbors

def solvable(puzzle,goal='_abcdefghijklmno'): #assumes sidelen 4
    inv=0
    for n in puzzle:
        if n !='_':
            for k in puzzle[puzzle.find(n)+1:]:
                if k!='_' and n>k:
                    inv+=1
    return (puzzle.find('_')//4 - goal.find('_')//4)%2==inv%2

def getPath(nbr,lvl,closedSet):
    pathList=[nbr]
    lookup=createLookup(nbr)
    while(lvl != 0):
        for n in neighbors(nbr,lookup):
            if n in closedSet and closedSet[n]==lvl-1:
                nbr = n
                lvl = closedSet[n]
                pathList.insert(0,nbr)
    return pathList

def solve(puzzle, goal = '_abcdefghijklmno'):
    if '0' in puzzle: puzzle = puzzle[0:puzzle.find('0')].lower()+'_'+puzzle[puzzle.find('0')+1:].lower()
    if puzzle==goal:
        return [puzzle]
    if solvable(puzzle, goal) == False:
        return []
    lookup = createLookup(puzzle)
    openSet = PriorityQueue() #parseMe
    openSet.put((mnhtPuzzle(puzzle,goal),0,puzzle))#PQ: estimate, level, puzzle
    closedSet = {} #dictSeen but not
    while openSet:
        est, lvl, pzl = openSet._get()
        if pzl in closedSet:
            continue
        else:
            closedSet[pzl] = lvl
        for nbr in neighbors(pzl,lookup):
            if nbr == goal:
                return getPath(nbr,lvl+1,closedSet)
            elif nbr in closedSet:
                continue
            else:
                newEst = lvl+1+mnhtPuzzle(nbr,goal)
                openSet.put((newEst,lvl+1,nbr))
    return []

def mnhtDistTile(puzzle, goal, tile):
    grid = {}  #top left = (0,0)
    sideLen = int(math.sqrt(len(puzzle)))
    for k in range(len(puzzle)):
        grid[k] = [k%sideLen, k//sideLen]
    tlAt = puzzle.find(tile)
    goTo = goal.find(tile)
    return (abs(int(grid[goTo][0]) - int(grid[tlAt][0])) + (abs(int(grid[goTo][1]) - int(grid[tlAt][1]))))

def mnhtPuzzle(puzzle, goal='_abcdefghijklmno'):
    dist = 0
    for k in puzzle:
        if k != '_':
            dist += mnhtDistTile(puzzle, goal, k)
    return dist

file = open(sys.argv[1],'r') if len(sys.argv) == 2 else open('eckel.txt','r')
for pzl in file:
    start = time.clock()
    printList = [n.find('_') for n in solve(pzl.strip())]
    elapsed = round(time.clock() - start, 3)
    print(pzl.strip(), ': ', len(printList) - 1, 'TIME:', elapsed, 'sec SEQUENCE:', printList) if printList else (pzl, 'is not solvable.')

'''
output:
Puzzle: 0ABCDEFGHIJKLMNO
 Depth: 1 Seconds: 9.813337520357375e-06
Solution sequence: [0]
Puzzle: A0BCDEFGHIJKLMNO
 Depth: 2 Seconds: 0.00030634679737463364
Solution sequence: [1, 0]
Puzzle: AEBCD0FGHIJKLMNO
 Depth: 3 Seconds: 0.0007206403074731978
Solution sequence: [5, 1, 0]
Puzzle: DABCEF0GHIJKLMNO
 Depth: 4 Seconds: 0.0011827205046274158
Solution sequence: [6, 5, 4, 0]
Puzzle: DABCHEFGIJ0KLMNO
 Depth: 5 Seconds: 0.0014007472643188324
Solution sequence: [10, 9, 8, 4, 0]
Puzzle: DBFCEA0GHIJKLMNO
 Depth: 6 Seconds: 0.0019264008219310172
Solution sequence: [6, 2, 1, 5, 4, 0]
Puzzle: AEBCDIFG0MJKHLNO
 Depth: 7 Seconds: 0.0016695473790068827
Solution sequence: [8, 12, 13, 9, 5, 1, 0]
Puzzle: DABCEIFGHMJ0LNOK
 Depth: 8 Seconds: 0.001979734178019917
Solution sequence: [11, 15, 14, 13, 9, 5, 4, 0]
Puzzle: DABCHEFGIJ0NLMOK
 Depth: 9 Seconds: 0.0033075214112091352
Solution sequence: [10, 11, 15, 14, 10, 9, 8, 4, 0]
Puzzle: D0BCEAFGHIMKLNJO
 Depth: 10 Seconds: 0.007247789759056966
Solution sequence: [1, 5, 9, 10, 14, 13, 9, 5, 4, 0]
Puzzle: DABCHEF0IJOGLMKN
 Depth: 11 Seconds: 0.0037077349153002287
Solution sequence: [7, 11, 10, 14, 15, 11, 10, 9, 8, 4, 0]
Puzzle: ABC0DEKGHIFOLMJN
 Depth: 12 Seconds: 0.0054314689840934335
Solution sequence: [3, 7, 6, 10, 14, 15, 11, 7, 3, 2, 1, 0]
Puzzle: DBFCEIAK0HGJLMNO
 Depth: 13 Seconds: 0.005807362477807991
Solution sequence: [8, 9, 5, 6, 10, 11, 7, 6, 2, 1, 5, 4, 0]
Puzzle: DACGHBEFLIJKMN0O
 Depth: 14 Seconds: 0.005658882414456501
Solution sequence: [14, 13, 12, 8, 4, 0, 1, 5, 6, 7, 3, 2, 1, 0]
Puzzle: HDAGF0CBIEJKLMNO
 Depth: 15 Seconds: 0.007778136652004969
Solution sequence: [5, 4, 0, 1, 2, 6, 7, 3, 2, 6, 5, 9, 8, 4, 0]
Puzzle: ABCEDIFGHMJ0LNOK
 Depth: 16 Seconds: 0.01763627419147698
Solution sequence: [11, 7, 3, 2, 6, 7, 11, 15, 14, 13, 9, 5, 6, 2, 1, 0]
Puzzle: DACGEIFBHK0OLJMN
 Depth: 17 Seconds: 0.018500701226965857
Solution sequence: [10, 9, 13, 14, 15, 11, 10, 6, 7, 3, 2, 6, 10, 9, 5, 4, 0]
Puzzle: IEACDMBGHFJKLN0O
 Depth: 18 Seconds: 0.04591575292405457
Solution sequence: [14, 10, 9, 5, 1, 0, 4, 5, 1, 2, 6, 10, 14, 13, 9, 5, 4, 0]
Puzzle: ABKCHDG0IFEJLMNO
 Depth: 19 Seconds: 0.07416664497776854
Solution sequence: [7, 6, 2, 3, 7, 6, 10, 9, 8, 4, 5, 6, 10, 11, 7, 3, 2, 1, 0]
Puzzle: AFICDB0GEHJOLMKN
 Depth: 20 Seconds: 0.07891416700337792
Solution sequence: [6, 10, 14, 15, 11, 10, 6, 5, 1, 2, 6, 5, 1, 0, 4, 8, 9, 5, 4, 0]
Puzzle: IBFCADJGEHONL0MK
 Depth: 21 Seconds: 0.03247916052444183
Solution sequence: [13, 14, 10, 11, 15, 14, 10, 6, 2, 1, 5, 4, 0, 1, 5, 4, 8, 9, 5, 4, 0]
Puzzle: EJBCAI0FMHKGDLNO
 Depth: 22 Seconds: 0.050374848159935204
Solution sequence: [6, 5, 9, 8, 12, 13, 9, 5, 1, 0, 4, 8, 9, 5, 6, 7, 11, 10, 9, 5, 1, 0]
Puzzle: EB0CADKGHFJMLNIO
 Depth: 23 Seconds: 0.13149104276951157
Solution sequence: [2, 3, 7, 6, 10, 11, 7, 3, 2, 1, 0, 4, 5, 9, 10, 14, 13, 9, 10, 6, 5, 1, 0]
Puzzle: DBCFEAIMLHJG0NOK
 Depth: 24 Seconds: 0.053707116248369546
Solution sequence: [12, 8, 9, 10, 6, 7, 3, 2, 1, 5, 6, 10, 9, 5, 6, 7, 11, 15, 14, 13, 9, 5, 4, 0]
Puzzle: 0ABCDEFGIJMOHLKN
 Depth: 25 Seconds: 1.6829605047298153
Solution sequence: [0, 1, 5, 6, 10, 14, 15, 11, 10, 9, 8, 12, 13, 14, 10, 6, 5, 9, 10, 14, 13, 9, 5, 1, 0]
Puzzle: F0JCAIBGEMDKHLNO
 Depth: 26 Seconds: 0.7881172429300238
Solution sequence: [1, 0, 4, 8, 12, 13, 9, 5, 6, 2, 1, 5, 4, 8, 9, 10, 6, 2, 1, 5, 9, 8, 4, 5, 1, 0]
Puzzle: BADCFEGKHI0NLMOJ
 Depth: 27 Seconds: 1.7047973140468544
Solution sequence: [10, 11, 15, 14, 10, 11, 7, 6, 5, 1, 0, 4, 5, 1, 2, 6, 5, 1, 0, 4, 5, 1, 2, 6, 5, 1, 0]
Puzzle: IABCNDHFEJKGLM0O
 Depth: 28 Seconds: 1.0688512293765244
Solution sequence: [14, 13, 9, 5, 4, 8, 9, 5, 6, 7, 11, 10, 9, 13, 14, 10, 9, 5, 4, 0, 1, 5, 4, 8, 9, 5, 1, 0]
Puzzle: AH0GDECKLBJFIMNO
 Depth: 29 Seconds: 2.5690468561266586
Solution sequence: [2, 6, 5, 1, 0, 4, 8, 12, 13, 14, 10, 9, 8, 4, 5, 6, 10, 11, 7, 3, 2, 6, 10, 14, 13, 12, 8, 4, 0]
Puzzle: DGBALHFCMEOJIN0K
 Depth: 30 Seconds: 1.1976666443377688
Solution sequence: [14, 10, 6, 2, 1, 5, 6, 2, 3, 7, 6, 5, 1, 2, 6, 10, 11, 15, 14, 13, 12, 8, 4, 5, 9, 13, 12, 8, 4, 0]
Puzzle: AC0KIFGBDNMJEHLO
 Depth: 31 Seconds: 0.9442320828723556
Solution sequence: [2, 6, 7, 3, 2, 1, 5, 4, 8, 12, 13, 14, 10, 9, 5, 1, 0, 4, 8, 12, 13, 14, 10, 11, 7, 3, 2, 6, 5, 4, 0]
Puzzle: AFB0DEGCMOJKHILN
 Depth: 32 Seconds: 15.875093280039799
Solution sequence: [3, 7, 6, 10, 9, 5, 1, 2, 3, 7, 11, 10, 6, 5, 9, 13, 14, 15, 11, 7, 3, 2, 1, 5, 9, 8, 12, 13, 9, 5, 1, 0]
Puzzle: EDBCN0MIJLGFAHOK
 Depth: 33 Seconds: 0.17324935391972218
Solution sequence: [5, 4, 8, 12, 13, 9, 5, 4, 8, 12, 13, 9, 5, 6, 7, 11, 10, 9, 5, 6, 7, 11, 15, 14, 13, 9, 5, 1, 0, 4, 5, 1, 0]
Puzzle: EFCKGDAJLMBH0NOI
 Depth: 34 Seconds: 0.3606887938938854
Solution sequence: [12, 8, 4, 5, 6, 10, 11, 15, 14, 13, 9, 8, 4, 5, 9, 10, 11, 7, 3, 2, 6, 5, 1, 0, 4, 8, 9, 10, 11, 7, 6, 5, 1, 0]
Puzzle: DGKEHABC0LFNJIMO
 Depth: 35 Seconds: 7.430371170291696
Solution sequence: [8, 12, 13, 9, 10, 11, 7, 6, 2, 1, 5, 9, 8, 12, 13, 14, 10, 6, 2, 3, 7, 11, 10, 9, 8, 4, 0, 1, 2, 3, 7, 6, 5, 1, 0]
Puzzle: FIEBDA0CONKGHLMJ
 Depth: 36 Seconds: 24.08606467672093
Solution sequence: [6, 10, 9, 8, 4, 5, 1, 0, 4, 8, 12, 13, 14, 10, 9, 5, 1, 2, 3, 7, 11, 10, 6, 5, 9, 13, 14, 15, 11, 10, 14, 13, 9, 5, 1, 0]
'''