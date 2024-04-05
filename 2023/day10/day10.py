# https://adventofcode.com/2023/day/10

# ingest the input file
inputFile = open("input.txt", "r")
lines = inputFile.readlines()
inputFile.close()
table = []  # the input in a table of character
pipe = []  # a table that capture main pipe element in a table of booleans, Pipe = true, no pipe = false
start = (0, 0)  # the "start" of the pipe
for row in range(len(lines)):
   subTable = []
   subPipe = []
   for col in range(len(lines[row])):
      subTable.append(lines[row][col])
      subPipe.append(False)
      if lines[row][col] == "S":
         start = (row, col)
   table.append(subTable)
   pipe.append(subPipe)
pipe[start[0]][start[1]] = True

# part 1, walk and measure the length of the loop from the start
origin = start
location = (start[0] + 1, start[1])  # we know by looking at the input that the cell bellow the start is on the pipe
length = 1
while table[location[0]][location[1]] != "S":
   pipe[location[0]][location[1]] = True
   candidates = ((0, 0), (0, 0))
   if table[location[0]][location[1]] == "|":
      candidates = ((location[0] - 1, location[1]), (location[0] + 1, location[1]))
   elif table[location[0]][location[1]] == "-":
      candidates = ((location[0], location[1] - 1), (location[0], location[1] + 1))
   elif table[location[0]][location[1]] == "L":
      candidates = ((location[0] - 1, location[1]), (location[0], location[1] + 1))
   elif table[location[0]][location[1]] == "J":
      candidates = ((location[0] - 1, location[1]), (location[0], location[1] - 1))
   elif table[location[0]][location[1]] == "7":
      candidates = ((location[0], location[1] - 1), (location[0] + 1, location[1]))
   elif table[location[0]][location[1]] == "F":
      candidates = ((location[0], location[1] + 1), (location[0] + 1, location[1]))
   if candidates[0] == origin:
      origin = location
      location = candidates[1]
   else:
      origin = location
      location = candidates[0]
   length += 1

print("Part 1 solution:", str(length / 2))  # the distance to the farthest point from the start is half the length of the full loop

# part 2, calculate the sum of cells inside the path loop
sum = 0
for idx in range(len(pipe)):
   out = True  # outside of the loop
   for jdx in range(len(pipe[idx])):
      if pipe[idx][jdx]:
         if ((table[idx][jdx] == "|") or
                 (table[idx][jdx] == "7") or
                 (table[idx][jdx] == "F") or
                 (table[idx][jdx] == "S")):  # The start pipe is 7 shaped
            out = not out
      else:
         if not out:
            sum += 1

print("Part 2 solution:", str(sum))
