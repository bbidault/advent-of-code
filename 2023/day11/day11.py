
inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
sum = 0

table = []
for line in Lines:
   subtable = []
   for i in range(len(line) - 1):
      subtable.append(line[i])
   table.append(subtable)

# for i in range(len(table)):
#     for j in range(len(table[i])):
#         print(table[i][j], end='')
#     print()

galaxies = []
for i in range(len(table)):
   for j in range(len(table[i])):
      if table[i][j] == "#":
         galaxies.append([i, j])

emptyRows = []
for i in range(len(table)):
   isEmpty = True
   for j in range(len(table[i])):
      if table[i][j] == "#":
         isEmpty = False
         break
   if isEmpty:
      print("row " + str(i))
      emptyRows.append(i)

emptyColumns = []
for j in range(len(table[0])):
   isEmpty = True
   for i in range(len(table)):
      if table[i][j] == "#":
         isEmpty = False
         break
   if isEmpty:
      print("column " + str(j))
      emptyColumns.append(j)

for galaxy in galaxies:
   add = 0
   for row in emptyRows:
      if galaxy[0] > row:
         add += 999999
   galaxy[0] += add

for galaxy in galaxies:
   add = 0
   for column in emptyColumns:
      if galaxy[1] > column:
         add += 999999
   galaxy[1] += add

for source in galaxies:
   for target in galaxies:
      sum += abs(source[0] - target[0]) + abs(source[1] - target[1])

print(sum / 2)
inputFile.close()
