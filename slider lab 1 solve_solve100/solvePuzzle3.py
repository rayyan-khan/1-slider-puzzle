import sys

inputPuzzles = sys.argv

def printList(p):
    print('\n')
    print('\n')
    if p == "No solution.":
        print(p)
    for k in range(len(p)//5):
        for n in range(0, 5):
            print(p[k*5 + n][0:3], "   ", end = "")
        print("")
        for m in range(0, 5):
            print(p[k * 5 + m][3:6], "   ", end="")
        print("")
        for o in range(0, 5):
            print(p[k * 5 + o][6:], "   ", end="")
        print("\n", "\n")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][0:3], "   ", end = "")
    print("")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][3:6], "   ", end = "")
    print("")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][6:], "   ", end = "")
    print("")

#Part D - find neighbors of given puzzle state.
def neighbors(s):
    space = s.find("_")
    lookup = [[1,3],[0,2,4],[1,5],[0,4,6],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]]
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
    print("No solution.")

if len(sys.argv) == 3:
    solution = solve(inputPuzzles[1],inputPuzzles[2])
    if isinstance(solution, list):
        printList(solution)
        print("\n Number of steps: ", len(solution))
else:
    solution = solve(inputPuzzles[1])
    if isinstance(solution, list):
        printList(solution)
        print("\n Number of steps: ", len(solution)-1)