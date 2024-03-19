import sys
import copy

sys.setrecursionlimit(100000000)


maxSteps = 327

inputFile = open("input.txt", "r")
lines = inputFile.readlines()
table = []
for i in range(len(lines)):
   subtable = []
   for j in range(len(lines[i])):
      if lines[i][j] == "#":
         subtable.append(-1)
      elif lines[i][j] == ".":
         subtable.append(maxSteps + 1)
   table.append(subtable)


def recurse(loc, steps, amaxSteps, tableCopy, num):
   sum = 0
   if ((steps <= amaxSteps) and
       (loc[0] < len(tableCopy)) and
       (loc[0] >= 0) and
       (loc[1] < len(tableCopy[0])) and
       (loc[1] >= 0) and
           (tableCopy[loc[0]][loc[1]] > steps)):
      if tableCopy[loc[0]][loc[1]] == (maxSteps + 1) and (loc[0] + loc[1]) % 2 == num:
         sum = 1
      tableCopy[loc[0]][loc[1]] = steps
      sum += recurse((loc[0] + 1, loc[1]), steps + 1, amaxSteps, tableCopy, num)
      sum += recurse((loc[0] - 1, loc[1]), steps + 1, amaxSteps, tableCopy, num)
      sum += recurse((loc[0], loc[1] + 1), steps + 1, amaxSteps, tableCopy, num)
      sum += recurse((loc[0], loc[1] - 1), steps + 1, amaxSteps, tableCopy, num)
   return sum


def sign(a: int):
   if a < 0:
      return -1
   return 1

# maps = [(0, 0, 0)]
# toVisit = []

# def visit(row, col, steps):
#     print(str(row) + " " + str(col) + " " + str(steps))
#     if steps + 1 < totalSteps:
#         maps.append((row, col, steps))
#         if abs(row) > abs(col):
#             toVisit.append((row + sign(row), col, steps + 130))
#         elif abs(row) < abs(col):
#             toVisit.append((row, col + sign(col), steps + 130))
#         else:
#             toVisit.append((row + sign(row), col, steps + 195))
#             toVisit.append((row, col + sign(col), steps + 195))
#             toVisit.append((row + sign(row), col + sign(col), steps + 230))

# toVisit.append((1, 0, 65))
# toVisit.append((1, 1, 130))
# toVisit.append((0, 1, 65))
# toVisit.append((-1, 1, 130))
# toVisit.append((-1, 0, 65))
# toVisit.append((-1, -1, 130))
# toVisit.append((0, -1, 65))
# toVisit.append((1, -1, 130))
# while toVisit:
#     row, col, steps = toVisit.pop(0)
#     visit(row, col, steps)


startLoc = (327, 327)
print(recurse(startLoc, 0, 65, copy.deepcopy(table), 1))
print(recurse(startLoc, 0, 196, copy.deepcopy(table), 0))
print(recurse(startLoc, 0, 327, copy.deepcopy(table), 1))

# for i in range(len(table)):
#     for j in range(len(table[i])):
#         if table[i][j] == -1:
#             print("#", end="")
#         elif table[i][j] < (maxSteps + 1):
#             if table[i][j]%2 == 0:
#                 answer += 1
#                 print("+", end="")
#             else:
#                 print(".", end="")
#         else:
#             print(".", end="")
#     print()

# visitableGardens1 = 7791 #15579 #7791 #7787
# visitableGardens2 = 7787
# totalSteps = 26501365
# stepsLeftAtTip = (totalSteps - 65)%131
# # print("stepsLeftAtTip " + str(stepsLeftAtTip))
# fullSquareToBorder = int((totalSteps - 65)/131) - 1
# print("fullSquareToBorder " + str(fullSquareToBorder))

# answer = (visitableGardens1 + # square 0 0
#          ((fullSquareToBorder+1)/2) * visitableGardens2 * 4 + # full squares
#          ((fullSquareToBorder-1)/2) * visitableGardens1 * 4 + # full squares
#          (fullSquareToBorder - 2) * (fullSquareToBorder - 2) * (visitableGardens1 + visitableGardens2) + (fullSquareToBorder - 1) * visitableGardens1 * 4 + # full squares
#          recurse((0, 65), 0, stepsLeftAtTip, copy.deepcopy(table), 0) + # southern tip
#          recurse((1, 65), 0, stepsLeftAtTip + 131, copy.deepcopy(table), 1) + # southern tip
#          recurse((131, 65), 0, stepsLeftAtTip, copy.deepcopy(table), 0) + # northern tip
#          recurse((130, 65), 0, stepsLeftAtTip + 131, copy.deepcopy(table), 1) + # northern tip
#          recurse((65, 0), 0, stepsLeftAtTip, copy.deepcopy(table), 0) + # eastern tip
#          recurse((65, 1), 0, stepsLeftAtTip + 131, copy.deepcopy(table), 1) + # eastern tip
#          recurse((65, 131), 0, stepsLeftAtTip, copy.deepcopy(table), 0) + # western tip
#          recurse((65, 130), 0, stepsLeftAtTip + 131, copy.deepcopy(table), 1) + # western tip
#          ((fullSquareToBorder + 1)/2) * recurse((0, 0), 0, stepsLeftAtTip + 131 - 65, copy.deepcopy(table), 0) +  # south eastern side
#          ((fullSquareToBorder - 1)/2) * recurse((1, 0), 0, stepsLeftAtTip + 131 + 65, copy.deepcopy(table), 1) +  # south eastern side
#          ((fullSquareToBorder + 1)/2) * recurse((131, 0), 0, stepsLeftAtTip + 131 - 65, copy.deepcopy(table), 0) +  # north eastern side
#          ((fullSquareToBorder - 1)/2) * recurse((130, 0), 0, stepsLeftAtTip + 131 + 65, copy.deepcopy(table), 1) +  # north eastern side
#          ((fullSquareToBorder + 1)/2) * recurse((131, 131), 0, stepsLeftAtTip + 131 - 65, copy.deepcopy(table), 0) +  # north western side
#          ((fullSquareToBorder - 1)/2) * recurse((130, 131), 0, stepsLeftAtTip + 131 + 65, copy.deepcopy(table), 1) +  # north western side
#          ((fullSquareToBorder + 1)/2) * recurse((0, 131), 0, stepsLeftAtTip + 131 - 65, copy.deepcopy(table), 0) +  # south western side
#          ((fullSquareToBorder - 1)/2) * recurse((0, 130), 0, stepsLeftAtTip + 131 + 65, copy.deepcopy(table), 1) # south western side
# )

# print(answer)

n = (26501365 - 65) // 131
a = (97645 - (2 * 35223) + 3957) // 2
b = 35223 - 3957 - a
c = 3957
print((a * n**2) + (b * n) + c)

inputFile.close()
