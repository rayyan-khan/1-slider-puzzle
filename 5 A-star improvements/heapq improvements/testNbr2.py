import sys

file = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('eckel.txt', 'r')
goal = file.readline().strip()
if '0' in goal:
    goal = goal[0:goal.find('0')].lower() + '_' + goal[goal.find('0') + 1:].lower()

pzlSize = len(goal)
sideLen = int(pzlSize**.5)

# create lookup
lookup = [[] for i in range(pzlSize)]
# corners
lookup[0] = [1, sideLen]  # top left
lookup[sideLen - 1] = [sideLen - 2, sideLen * 2 - 1]  # top right
lookup[pzlSize - sideLen] = [pzlSize - sideLen + 1, pzlSize - 2 * sideLen]  # bottom left
lookup[pzlSize - 1] = [pzlSize - 2, pzlSize - sideLen - 1]  # bottom right
for n in range(pzlSize):
    if not lookup[n]:  # if not empty
        # edges
        if n < sideLen:  # top edge
            lookup[n] = [n - 1, n + sideLen, n + 1]
        elif n > pzlSize - sideLen:  # bottom edge
            lookup[n] = [n - 1, n + 1, n - sideLen]
        elif n % sideLen == 0:  # left edge
            lookup[n] = [n + sideLen, n + 1, n - sideLen]
        elif n % sideLen == sideLen - 1:  # right edge
            lookup[n] = [n - sideLen, n - 1, n + sideLen]
        else:  # center (has four neighbors)
            lookup[n] = [n - sideLen, n - 1, n + sideLen, n + 1]



def swapChars(num, space, puzzle):
    if num < space:
        return puzzle[0:num] + '_' + puzzle[num + 1: space] + puzzle[num] + puzzle[space + 1:]
    return puzzle[0:space] + puzzle[num] + puzzle[space + 1: num] + '_' + puzzle[num + 1:]

def neighbors(puzzle, space):
    return [(swapChars(num, space, puzzle), num) for num in lookup[space]]
    # change is to store location of the space in a tuple with the neighbor so we don't need .find

print(neighbors('a_bcdefghijklmno', 1))

for n in neighbors('a_bcdefghijklmno', 1):
    print('{}: {}'.format(n[0], neighbors(n[0], n[1])))