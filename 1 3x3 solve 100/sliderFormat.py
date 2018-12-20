import sys
s = sys.argv[1]
top = []
mid = []
bot = []
for i in range(0, len(s)):
    if i < 3:
        top.append(s[i])
    elif i < 6:
        mid.append(s[i])
    else:
        bot.append(s[i])
matr = [top,mid,bot]

for row in matr:
    for column in row:
        print(column, end = "")
    print(end="\n")