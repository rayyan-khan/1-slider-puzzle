import sys

if len(sys.argv) == 1:
    inputPuzzle = sys.argv[1]
else:
    inputPuzzles[] = sys.argv

#Part A part 1 - takes one string puzzle and puts into matrix. Doesn't print in 2D.
def format(s):
    if len(s) > 9:
        print("Not a slider puzzle.")
    top = []
    mid = []
    bot = []
    matr = [top,mid,bot]
    for i in range(0, len(s)):
        if i < 3:
            top.append(s[i])
        elif i < 6:
            mid.append(s[i])
        else:
            bot.append(s[i])
    return matr

#Part A part 2 - prints single formatted puzzle in 2D.
def printPuzz(s):
    if isinstance(s, str):
        s = format(s)
    for row in s:
        for column in row:
            print(column, end="")
        print(end="\n")

#Part B - print list of puzzles and display in order, all in 2D. 5 displayed per row.
def printList(p):
    print("\n")
    for i in range(len(p)):
        p[i] = format(p[i])
    for k in range(len(p)//5):
        for n in range(0, 5):
            print(p[k*5 + n][0], "     ", end = "")
        print("")
        for m in range(0, 5):
            print(p[k*5 + m][1], "     ", end = "")
        print("")
        for o in range(0, 5):
            print(p[k*5 + o][2], "     ", end = "")
        print("\n", "\n")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][0], "     ", end = "")
    print("")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][1], "     ", end = "")
    print("")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][2], "     ", end = "")
    print("")

def printList1(p):
    print('\n')
    for k in range(len(p)//5):
        for n in range(0, 5):
            print(p[k*5 + n][0:3], "   ", end = "")
        print("")
        for m in range(0, 5):
            print(p[k * 5 + m][3:6], "  ", end="")
        print("")
        for o in range(0, 5):
            print(p[k * 5 + o][6:], "     ", end="")
        print("\n", "\n")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][0:3], "  ", end = "")
    print("")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][3:6], "  ", end = "")
    print("")
    for r in range(0, len(p)%5):
        print(p[(len(p)//5)*5 + r][6:], "  ", end = "")
    print("")

#Part C should come after Part E

#Part D - find neighbors of given puzzle state.
def neighbors(s):
    space = s.find("_")
    lookup = [[1,3],[0,2,4],[1,5],[0,4],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]]
    neighbors = []
    for i in lookup[space]:
        newS = s[0:space] + s[i] + s[space + 1:]
        newS = newS[0:i] + "_" + newS[i+1:]
        neighbors.append(newS)
    return neighbors

#printPuzz(inputPuzzle)
#printList(neighbors(inputPuzzle))
printList1()