import copy

inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
area = 0
perimeter = 0
initLoc = [0, 0]
for line in Lines:
   # dir, num, col = line.split(" ")
   num = int(line[0:5], 16)
   nextLoc = copy.deepcopy(initLoc)
   if line[5] == "0":  # Right
      # if dir == "R":
      nextLoc[1] += int(num)
   elif line[5] == "1":  # Down
      # elif dir == "D":
      nextLoc[0] += int(num)
   elif line[5] == "2":  # Left
      # elif dir == "L":
      nextLoc[1] -= int(num)
   elif line[5] == "3":  # Up
      # elif dir == "U":
      nextLoc[0] -= int(num)
   area -= (initLoc[0] * nextLoc[1] - initLoc[1] * nextLoc[0]) / 2
   perimeter += int(num)
   initLoc = copy.deepcopy(nextLoc)

print(area + perimeter / 2 + 1)
inputFile.close()
