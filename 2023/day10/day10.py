
inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
table = []
display = []
start = [0, 0]
for i in range(len(Lines)):
   subtable = []
   subDisplay = []
   for j in range(len(Lines[i])):
      subtable.append(Lines[i][j])
      subDisplay.append(" ")
      if Lines[i][j] == "S":
         start = [i, j]
   table.append(subtable)
   display.append(subDisplay)
display[start[0]][start[1]] = "#"
origin = start
location = [start[0] + 1, start[1]]
length = 1
while table[location[0]][location[1]] != "S":
   display[location[0]][location[1]] = "#"
   candidate1 = [0, 0]
   candidate2 = [0, 0]
   if table[location[0]][location[1]] == "|":
      candidate1 = [location[0] - 1, location[1]]
      candidate2 = [location[0] + 1, location[1]]
   elif table[location[0]][location[1]] == "-":
      candidate1 = [location[0], location[1] - 1]
      candidate2 = [location[0], location[1] + 1]
   elif table[location[0]][location[1]] == "L":
      candidate1 = [location[0] - 1, location[1]]
      candidate2 = [location[0], location[1] + 1]
   elif table[location[0]][location[1]] == "J":
      candidate1 = [location[0] - 1, location[1]]
      candidate2 = [location[0], location[1] - 1]
   elif table[location[0]][location[1]] == "7":
      candidate1 = [location[0], location[1] - 1]
      candidate2 = [location[0] + 1, location[1]]
   elif table[location[0]][location[1]] == "F":
      candidate1 = [location[0], location[1] + 1]
      candidate2 = [location[0] + 1, location[1]]
   if candidate1 == origin:
      origin = location
      location = candidate2
   else:
      origin = location
      location = candidate1
   length += 1
print(str(length / 2))


sum = 0
for i in range(len(display)):
   # print(str(len(table[i])) + " " + str(len(display[i])))
   out = True
   for j in range(len(display[i])):
      if display[i][j] == "#":
         if (table[i][j] == "|") or (table[i][j] == "7") or (table[i][j] == "F") or (table[i][j] == "S"):
            out = not out
      else:
         if (False == out):
            sum += 1
            display[i][j] = "I"
print(str(sum))

for i in range(len(display)):
   for j in range(len(display[i])):
      print(display[i][j], end="")
   print()

inputFile.close()
