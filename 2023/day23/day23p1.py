import copy
import sys
sys.setrecursionlimit(10000)


class square:
   def __init__(self):
      self.steps = -1
      self.labels = []


inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
table = []
visited = []
for line in Lines:
   if line.strip():
      subtable = []
      subvisited = []
      for char in line:
         if char in ".#><v^":
            subtable.append(char)
            subvisited.append(square())
      table.append(subtable)
      visited.append(subvisited)

# for i in range(len(table)):
#     for j in range(len(table[i])):
#         print(table[i][j], end='')
#     print()

topLabel = 0


def isReachable(row, col):
   return (row >= 0) and (col >= 0) and (row < len(table)) and (col < len(table[row])) and (table[row][col] != "#")


def recurse(srcRow: int, srcCol: int, row: int, col: int, steps: int, subPathLabel: int, totalPathLabels: []):
   global topLabel
   noSharedLabels = True
   for pathLabel in totalPathLabels:
      if pathLabel in visited[row][col].labels:
         noSharedLabels = False
         break
   if noSharedLabels:  # and visited[row][col].steps < steps:
      # for i in range(steps):
      #     print(" ", end='')
      # print("recurse at " + str(row) + " " + str(col) + " subPath " + str(subPathLabel) + " of totalPathLabels " + str(totalPathLabels))
      visited[row][col].steps = steps
      visited[row][col].labels.append(subPathLabel)
      # if row == 22 and col == 21:
      if row == 140 and col == 139:
         if steps > 6000:
            print("Finished after " + str(steps))
      else:
         candidateSteps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
         validSteps = []
         for cStep in candidateSteps:
            if (row + cStep[0] != srcRow or col + cStep[1] != srcCol) and isReachable(row + cStep[0], col + cStep[1]):
               validSteps.append((row + cStep[0], col + cStep[1]))

         if len(validSteps) == 1:
            recurse(row, col, validSteps[0][0], validSteps[0][1], steps + 1, subPathLabel, totalPathLabels)
         elif len(validSteps) > 1:
            # print("split at " + str(row) + " " + str(col))
            for validStep in validSteps:
               topLabel += 1
               newLabel = copy.deepcopy(topLabel)
               newlabels = copy.deepcopy(totalPathLabels)
               newlabels.append(newLabel)
               recurse(row, col, validStep[0], validStep[1], steps + 1, newLabel, newlabels)


recurse(0, 0, 0, 1, 0, topLabel, [topLabel])

# and table[row+1][col] != "^":
# if (row-1 != srcRow or col != srcCol) and isReachable(row-1, col):# and table[row-1][col] != "v":
#     validSteps.append((row-1, col))
# if (row != srcRow or col+1 != srcCol) and isReachable(row, col+1):# and table[row][col+1] != "<":
#     validSteps.append((row, col+1))
# if (row != srcRow or col-1 != srcCol) and isReachable(row, col-1):# and table[row][col-1] != ">":
#     validSteps.append((row, col-1))

inputFile.close()
