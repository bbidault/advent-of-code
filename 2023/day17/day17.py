from heapq import heappush, heappop

inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
table = []
for line in Lines:
   if line.strip():
      subtable = []
      subvisited = []
      for char in line:
         if char in "0123456789":
            subtable.append(int(char))
      table.append(subtable)


def add(queue, cost, row, col, steps, origin):
   if row >= 0 and row < len(table) and col >= 0 and col < len(table[0]):
      heappush(queue, (cost + table[row][col], row, col, steps, origin))


visited = set()
queue = [(0, 0, 0, 0, "O")]

while queue:
   cost, row, col, steps, origin = heappop(queue)

   # print(str(row) + " " + str(col))

   if row == len(table) - 1 and col == len(table[row]) - 1:
      print(cost)
      break

   if (row, col, steps, origin) in visited:
      continue

   visited.add((row, col, steps, origin))

   if origin == "N":
      if steps >= 4:
         add(queue, cost, row, col - 1, 1, "E")
         add(queue, cost, row, col + 1, 1, "W")
      if steps < 10:
         add(queue, cost, row + 1, col, steps + 1, "N")
   elif origin == "S":
      if steps >= 4:
         add(queue, cost, row, col - 1, 1, "E")
         add(queue, cost, row, col + 1, 1, "W")
      if steps < 10:
         add(queue, cost, row - 1, col, steps + 1, "S")
   elif origin == "E":
      if steps >= 4:
         add(queue, cost, row + 1, col, 1, "N")
         add(queue, cost, row - 1, col, 1, "S")
      if steps < 10:
         add(queue, cost, row, col - 1, steps + 1, "E")
   elif origin == "W":
      if steps >= 4:
         add(queue, cost, row + 1, col, 1, "N")
         add(queue, cost, row - 1, col, 1, "S")
      if steps < 10:
         add(queue, cost, row, col + 1, steps + 1, "W")
   else:
      add(queue, 0, row + 1, col, 1, "N")
      add(queue, 0, row, col + 1, 1, "W")

inputFile.close()
