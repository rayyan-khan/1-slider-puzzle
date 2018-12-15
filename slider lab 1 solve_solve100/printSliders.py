import sys

puzzList = []

def puzzFormatter(s):
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


for k in range(1,len(sys.argv)):
    newPuzz = puzzFormatter(sys.argv[k])
    puzzList.append(newPuzz)


def printList(p):
    print("\n", "SLIDER PUZZLES: ")
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


printList(puzzList)














