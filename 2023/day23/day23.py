# https://adventofcode.com/2023/day/23


# Evaluate if a given location is reachable
#
# @param table: the table defining the search space
# @param row: the row of the cell of interest
# @param col: the column of the cell of interest
# @return: whether the given location is reachable or not
#
def isReachable(table, row, col):
   return (row >= 0) and (col >= 0) and (row < len(table)) and (col < len(table[row])) and (table[row][col] != "#")


# calculate and return the length of the longest non-repeating path on the given graph
#
# @param inputFilePath: the input file defining the graph
# @param part1: whether we should evaluate the path according to part 1 (True) or part 2 (False)
# @return: the length of the longest non-repeating path
#
def solve(inputFilePath: str, part1: bool):

   # ingest the given input file into a table
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   table = []
   for line in lines:
      if line.strip():
         subtable = []
         for char in line:
            if char in ".#><v^":
               subtable.append(char)
         table.append(subtable)

   # generate a topology graph from the input table
   edges = {}
   for row in range(len(table)):
      for col in range(len(table[row])):
         if table[row][col] == ".":
            # consider direction limitations for part 1.
            # E.g. a<b means we can go from cell b to cell a but not from a to b.
            if part1:
               if isReachable(table, row + 1, col):
                  if table[row + 1][col] == "^":
                     edges.setdefault((row + 2, col), set()).add((row, col, 2))
                  elif table[row + 1][col] == "v":
                     edges.setdefault((row, col), set()).add((row + 2, col, 2))
                  else:
                     edges.setdefault((row, col), set()).add((row + 1, col, 1))
                     edges.setdefault((row + 1, col), set()).add((row, col, 1))
               if isReachable(table, row - 1, col):
                  if table[row - 1][col] == "v":
                     edges.setdefault((row - 2, col), set()).add((row, col, 2))
                  elif table[row - 1][col] == "^":
                     edges.setdefault((row, col), set()).add((row - 2, col, 2))
                  else:
                     edges.setdefault((row, col), set()).add((row - 1, col, 1))
                     edges.setdefault((row - 1, col), set()).add((row, col, 1))
               if isReachable(table, row, col + 1):
                  if table[row][col + 1] == "<":
                     edges.setdefault((row, col + 2), set()).add((row, col, 2))
                  elif table[row][col + 1] == ">":
                     edges.setdefault((row, col), set()).add((row, col + 2, 2))
                  else:
                     edges.setdefault((row, col), set()).add((row, col + 1, 1))
                     edges.setdefault((row, col + 1), set()).add((row, col, 1))
               if isReachable(table, row, col - 1):
                  if table[row][col - 1] == ">":
                     edges.setdefault((row, col - 2), set()).add((row, col, 2))
                  elif table[row][col - 1] == "<":
                     edges.setdefault((row, col), set()).add((row, col - 2, 2))
                  else:
                     edges.setdefault((row, col), set()).add((row, col - 1, 1))
                     edges.setdefault((row, col - 1), set()).add((row, col, 1))
            else:  # ignore direction limitations for part 2
               for cStep in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                  if isReachable(table, row + cStep[0], col + cStep[1]):
                     edges.setdefault((row, col), set()).add((row + cStep[0], col + cStep[1], 1))
                     edges.setdefault((row + cStep[0], col + cStep[1]), set()).add((row, col, 1))

   if not part1:
      # collapse the graph for optimization
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

   # perform depth first search
   queue = [(0, 1, 0)]  # entrance
   visited = set()
   answer = 0
   while queue:
      row, col, totalPathLen = queue.pop()
      # remove the cell of interest from the set of visited cell to
      # enable visiting again in the next branch of DFS
      if totalPathLen == -1:
         visited.remove((row, col))
         continue
      # if we reached the exit
      if (row, col) == (len(table) - 1, len(table[0]) - 2):
         answer = max(answer, totalPathLen)
         continue
      # if the cell of interest has already been visited, stop the search
      if (row, col) in visited:
         continue
      visited.add((row, col))
      # set the cell of interest total distance to -1 so we can remove it
      # from the set of visited cells for the next branch of DFS
      queue.append((row, col, -1))
      for targetRow, targetCol, targetDist in edges[(row, col)]:
         queue.append((targetRow, targetCol, totalPathLen + targetDist))
   return answer


print("Part 1 test:", solve("test_input.txt", True))
print("Part 1 solution:", solve("input.txt", True))
print("Part 2 test:", solve("test_input.txt", False))
print("Part 2 solution:", solve("input.txt", False))
