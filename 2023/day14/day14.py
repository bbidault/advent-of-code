def evaluate(table):
   answer = 0
   for i in range(len(table[0])):
      for j in range(len(table)):
         if table[j][i] == "O":
            answer += len(table) - j
   return answer


def tiltNorth(table):
   newTable = [["."] * len(table[0]) for i in range(len(table))]
   for i in range(len(table[0])):
      wall = 0
      for j in range(len(table)):
         if table[j][i] == "O":
            newTable[wall][i] = "O"
            wall += 1
         elif table[j][i] == "#":
            newTable[j][i] = "#"
            wall = j + 1
   return newTable


def tiltSouth(table):
   newTable = [["."] * len(table[0]) for i in range(len(table))]
   for i in range(len(table[0])):
      wall = len(table) - 1
      for j in range(len(table) - 1, -1, -1):
         if table[j][i] == "O":
            newTable[wall][i] = "O"
            wall -= 1
         elif table[j][i] == "#":
            newTable[j][i] = "#"
            wall = j - 1
   return newTable


def tiltWest(table):
   newTable = [["."] * len(table[0]) for i in range(len(table))]
   for i in range(len(table)):
      wall = 0
      for j in range(len(table[0])):
         if table[i][j] == "O":
            newTable[i][wall] = "O"
            wall += 1
         elif table[i][j] == "#":
            newTable[i][j] = "#"
            wall = j + 1
   return newTable


def tiltEast(table):
   newTable = [["."] * len(table[0]) for i in range(len(table))]
   for i in range(len(table)):
      wall = len(table[0]) - 1
      for j in range(len(table[0]) - 1, -1, -1):
         if table[i][j] == "O":
            newTable[i][wall] = "O"
            wall -= 1
         elif table[i][j] == "#":
            newTable[i][j] = "#"
            wall = j - 1
   return newTable


inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
answer = 0
table = []
count = 0
for line in Lines:
   if line.strip():
      subtable = []
      for char in line:
         if char in ".#O":
            subtable.append(char)
      table.append(subtable)


oldTableTiltedNorth = tiltNorth(table)
combinations = []
cycles = []
for i in range(250000000):
   test = False
   table = tiltNorth(table)
   if table in combinations:
      print("cycle " + str(i) + " " + str(cycles[combinations.index(table)]))
      test = True
   else:
      combinations.append(table)
      cycles.append(i)
   table = tiltWest(table)
   table = tiltSouth(table)
   table = tiltEast(table)
   if test:
      print(evaluate(table))


for i in range(len(table)):
   for j in range(len(table[0])):
      print(table[i][j], end="")
   print()

# 98890 - 98898

98893
98894

print(evaluate(table))
inputFile.close()
