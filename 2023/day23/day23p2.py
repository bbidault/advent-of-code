

inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
inputFile.close()
table = []
for line in Lines:
   if line.strip():
      subtable = []
      for char in line:
         if char in ".#":
            subtable.append(char)
      table.append(subtable)


def isReachable(row, col):
   return (row >= 0) and (col >= 0) and (row < len(table)) and (col < len(table[row])) and (table[row][col] != "#")


edges = {}
for row in range(len(table)):
   for col in range(len(table[row])):
      if table[row][col] == ".":
         for cStep in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if isReachable(row + cStep[0], col + cStep[1]):
               edges.setdefault((row, col), set()).add((row + cStep[0], col + cStep[1], 1))
               edges.setdefault((row + cStep[0], col + cStep[1]), set()).add((row, col, 1))

while True:
   for source, targets in edges.items():
      if len(targets) == 2:
         target1, target2 = targets
         edges[target1[:2]].remove(source + (target1[2],))
         edges[target2[:2]].remove(source + (target2[2],))
         edges[target1[:2]].add((target2[0], target2[1], target1[2] + target2[2]))
         edges[target2[:2]].add((target1[0], target1[1], target1[2] + target2[2]))
         del edges[source]
         break
   else:
      break

queue = [(0, 1, 0)]
visited = set()
answer = 0
while queue:
   rowIdx, colIdx, d = queue.pop()
   if d == -1:
      visited.remove((rowIdx, colIdx))
      continue
   if (rowIdx, colIdx) == (len(table) - 1, len(table[0]) - 2):
      answer = max(answer, d)
      continue
   if (rowIdx, colIdx) in visited:
      continue
   visited.add((rowIdx, colIdx))
   queue.append((rowIdx, colIdx, -1))
   for ar, ac, l in edges[(rowIdx, colIdx)]:
      queue.append((ar, ac, d + l))
print(answer)
