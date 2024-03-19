from heapq import heappush, heappop
import copy

maxX = 0
maxY = 0
maxZ = 0


class brick:
   def __init__(self, name: int, begin: list, end: list):
      global maxX, maxY, maxZ
      # print(str(name) + " " + str(begin) + " " + str(end))
      self.name = int(name)
      self.beginx = int(begin[0])
      self.beginy = int(begin[1])
      self.beginz = int(begin[2]) - 1
      self.endx = int(end[0])
      self.endy = int(end[1])
      self.endz = int(end[2]) - 1
      if self.beginx > self.endx:
         print("ERROR")
      if self.beginy > self.endy:
         print("ERROR")
      if self.beginz > self.endz:
         print("ERROR")
      if self.endx > maxX:
         maxX = self.endx
      if self.endy > maxY:
         maxY = self.endy
      if self.endz > maxZ:
         maxZ = self.endz


queue = []
carried = []

inputFile = open("input.txt", "r")
idx = 0
Lines = inputFile.readlines()
for line in Lines:
   ends = line.strip().split("~")
   begin = ends[0].split(",")
   end = ends[1].split(",")
   heappush(queue, (int(begin[2]), idx, brick(idx, begin, end)))
   carried.append(set())
   idx += 1


queueCopy = []
for idx in range(len(queue)):
   queueCopy.append(heappop(queue))

# for idx in range(len(queueCopy)):
#    print(queueCopy[idx])

# for idx in queueCopy:
#     z, name, brick = idx
#     print("x: (" + str(brick.beginx) + ", " + str(brick.endx) + ") " +
#           "y: (" + str(brick.beginy) + ", " + str(brick.endy) + ") " +
#           "z: (" + str(brick.beginz) + ", " + str(brick.endz) + ")")

space = [[[-1 for k in range(maxX + 1)] for j in range(maxY + 1)] for i in range(maxZ)]

# move the bricks downward
for idx in queueCopy:
   z, name, brick = idx
   while brick.beginz > 0:
      occupied = False
      for y in range(brick.beginy, brick.endy + 1):
         for x in range(brick.beginx, brick.endx + 1):
            if space[brick.beginz - 1][y][x] != -1:
               occupied = True
      if occupied:
         break
      brick.beginz -= 1
      brick.endz -= 1
   for z in range(brick.beginz, brick.endz + 1):
      for y in range(brick.beginy, brick.endy + 1):
         for x in range(brick.beginx, brick.endx + 1):
            # print(str(z) + " " + str(y) + " " +  str(x) + " " + str(brick.endz) + " " + str(brick.endy) + " " +  str(brick.endx))
            space[z][y][x] = brick.name

# print()
# for idx in queueCopy:
#     z, name, brick = idx
#     print("x: (" + str(brick.beginx) + ", " + str(brick.endx) + ") " +
#           "y: (" + str(brick.beginy) + ", " + str(brick.endy) + ") " +
#           "z: (" + str(brick.beginz) + ", " + str(brick.endz) + ")")

# identify which brick carry which brick
for idx in range(len(queueCopy)):
   z, name, brick = queueCopy[idx]
   if brick.beginz == 0:
      continue
   else:
      for y in range(brick.beginy, brick.endy + 1):
         for x in range(brick.beginx, brick.endx + 1):
            if space[brick.beginz - 1][y][x] != -1:
               carried[idx].add(space[brick.beginz - 1][y][x])

coCarriers = set()

# identify co carriers, bricks that share the carry of a brick with 1 or more other brick
for idx in range(len(carried)):
   # print(str(idx) + " " + str(carried[idx]))
   if len(carried[idx]) == 0 and queueCopy[idx][2].beginz != 0:
      print("ERROR")
   if len(carried[idx]) > 1:
      for carrier in carried[idx]:
         coCarriers.add(carrier)

# need to check that some co carrier are not also single carriers
coCarriersList = list(coCarriers)
for idx in range(len(carried)):
   if len(carried[idx]) == 1:
      for brickName in carried[idx]:
         if brickName in coCarriersList:
            coCarriersList.remove(brickName)

# identify bricks that do not carry any other bricks
nonCarriers = set()
for idx in range(len(carried)):
   notCarrier = True
   for jdx in range(len(carried)):
      if idx in carried[jdx]:
         notCarrier = False
         break
   if notCarrier:
      nonCarriers.add(idx)

# print(nonCarriers)

# print()
# print("co carriers " + str(len(coCarriersList)))
# print("non carriers " + str(len(nonCarriers)))
# print("total " + str(len(nonCarriers) + len(coCarriersList)))

answer = 0

# part 2
for idx in range(len(queueCopy)):
   print(idx)
   spaceCopy = copy.deepcopy(space)
   deleted = [idx]
   for z in range(1, len(spaceCopy)):
      # print(deleted)
      for y in range(len(spaceCopy[z])):
         for x in range(len(spaceCopy[y])):
            if spaceCopy[z][y][x] != -1 and spaceCopy[z][y][x] not in deleted:
               if spaceCopy[z - 1][y][x] == -1 or spaceCopy[z - 1][y][x] in deleted:
                  # print("considering " + str(spaceCopy[z][y][x]))
                  allMinusOneOrDeleted = True
                  for yb in range(len(spaceCopy[z])):
                     for xb in range(len(spaceCopy[yb])):
                        # print(str(xb) + " " + str(yb) + " " + str(spaceCopy[z][yb][xb]) + " " + str(spaceCopy[z][y][x]) + " " + str(spaceCopy[z-1][yb][xb]))
                        if (spaceCopy[z][yb][xb] == spaceCopy[z][y][x]) and (spaceCopy[z - 1][yb][xb] != -1 and spaceCopy[z - 1][yb][xb] not in deleted):
                           # print("False")
                           allMinusOneOrDeleted = False
                  if allMinusOneOrDeleted:
                     # print(str(spaceCopy[z][y][x]) + " falls")
                     deleted.append(spaceCopy[z][y][x])
                     answer += 1

print(answer)
inputFile.close()
