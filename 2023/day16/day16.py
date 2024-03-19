import sys
sys.setrecursionlimit(10000)

inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
table = []
visited = []
for line in Lines:
   if line.strip():
      subtable = []
      subvisited = []
      for char in line:
         if char in ".-|BS":
            subtable.append(char)
            subvisited.append([])
      table.append(subtable)
      visited.append(subvisited)


def visit(i, j, origin):
   if i >= 0 and j >= 0 and i < len(table) and j < len(table[0]) and origin not in visited[i][j]:
      visited[i][j].append(origin)
      if table[i][j] == ".":
         if origin == "N":
            visit(i + 1, j, "N")
         elif origin == "S":
            visit(i - 1, j, "S")
         elif origin == "W":
            visit(i, j + 1, "W")
         elif origin == "E":
            visit(i, j - 1, "E")
      elif table[i][j] == "-":
         if origin == "N" or origin == "S":
            visit(i, j + 1, "W")
            visit(i, j - 1, "E")
         elif origin == "W":
            visit(i, j + 1, "W")
         elif origin == "E":
            visit(i, j - 1, "E")
      elif table[i][j] == "|":
         if origin == "N":
            visit(i + 1, j, "N")
         elif origin == "S":
            visit(i - 1, j, "S")
         elif origin == "W" or origin == "E":
            visit(i + 1, j, "N")
            visit(i - 1, j, "S")
      elif table[i][j] == "B":  # \
         if origin == "N":
            visit(i, j + 1, "W")
         elif origin == "S":
            visit(i, j - 1, "E")
         elif origin == "W":
            visit(i + 1, j, "N")
         elif origin == "E":
            visit(i - 1, j, "S")
      elif table[i][j] == "S":  # /
         if origin == "N":
            visit(i, j - 1, "E")
         elif origin == "S":
            visit(i, j + 1, "W")
         elif origin == "W":
            visit(i - 1, j, "S")
         elif origin == "E":
            visit(i + 1, j, "N")


answer = 0

for k in range(len(table)):
   visit(k, 0, "W")
   count = 0
   for i in range(len(visited)):
      for j in range(len(visited[i])):
         if visited[i][j]:
            count += 1
         visited[i][j] = []
   if count > answer:
      answer = count

for k in range(len(table)):
   visit(k, len(table) - 1, "E")
   count = 0
   for i in range(len(visited)):
      for j in range(len(visited[i])):
         if visited[i][j]:
            count += 1
         visited[i][j] = []
   if count > answer:
      answer = count

for k in range(len(table[0])):
   visit(0, k, "N")
   count = 0
   for i in range(len(visited)):
      for j in range(len(visited[i])):
         if visited[i][j]:
            count += 1
         visited[i][j] = []
   if count > answer:
      answer = count

for k in range(len(table[0])):
   visit(len(table) - 1, k, "S")
   count = 0
   for i in range(len(visited)):
      for j in range(len(visited[i])):
         if visited[i][j]:
            count += 1
         visited[i][j] = []
   if count > answer:
      answer = count

print(answer)
inputFile.close()
