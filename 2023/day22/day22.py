# https://adventofcode.com/2023/day/22


# The brick class defines a rectangular cuboid defined by two coordinates
#
class brick:
   # Constructor from parameters
   #
   # @param id: the id of the brick
   # @param begin: a coordinate of the brick
   # @param end: a coordinate of the brick opposite to the begin coordinate
   #
   def __init__(self, id: int, begin: list, end: list):
      self.id = int(id)
      self.beginX = int(begin[0])
      self.beginY = int(begin[1])
      self.beginZ = int(begin[2]) - 1
      self.endX = int(end[0])
      self.endY = int(end[1])
      self.endZ = int(end[2]) - 1


# Ingest the input file and return a list of brick objects and a 3d array representing the pilled bricks
#
# @param inputFilePath: the input file
# @return: a list of brick objects and a 3d array representing the pilled bricks
#
def ingest(inputFilePath: str) -> tuple:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()

   # ingest the input file into a bricks of bricks
   idx = 0
   bricks = []
   for line in lines:
      ends = line.strip().split("~")
      begin = ends[0].split(",")
      end = ends[1].split(",")
      # append a tuple including the z coordinate of the brick so we can sort the bricks from bottom to top later
      bricks.append((int(begin[2]), idx, brick(idx, begin, end)))
      idx += 1

   # sort the bricks so the bricks are ordered from bottom to top
   bricks.sort()

   # initialize the state space where the bricks move
   space = [[[-1 for _ in range(max(brck[2].endX for brck in bricks) + 1)]
             for _ in range(max(brck[2].endY for brck in bricks) + 1)]
            for _ in range(max(brck[2].endZ for brck in bricks))]

   # move the bricks downward
   for idx in bricks:
      z, _, brck = idx
      while brck.beginZ > 0:
         occupied = False
         for y in range(brck.beginY, brck.endY + 1):
            for x in range(brck.beginX, brck.endX + 1):
               if space[brck.beginZ - 1][y][x] != -1:
                  occupied = True
         if occupied:
            break
         brck.beginZ -= 1
         brck.endZ -= 1
      for z in range(brck.beginZ, brck.endZ + 1):
         for y in range(brck.beginY, brck.endY + 1):
            for x in range(brck.beginX, brck.endX + 1):
               space[z][y][x] = brck.id

   return (bricks, space)


# Calculate and return the number of bricks that can be removed independantly without toppling the pile
#
# @param inputFilePath: the input file
# @return: the number of bricks that can be removed independantly without toppling the pile
#
def part1(inputFilePath: str) -> int:
   bricks, space = ingest(inputFilePath)
   carried = []

   # identify which brick carries which brick
   for idx in range(len(bricks)):
      _, _, brck = bricks[idx]
      carried.append(set())
      if brck.beginZ == 0:
         continue
      else:
         for y in range(brck.beginY, brck.endY + 1):
            for x in range(brck.beginX, brck.endX + 1):
               if space[brck.beginZ - 1][y][x] != -1:
                  carried[idx].add(space[brck.beginZ - 1][y][x])

   coCarriers = set()

   # identify co carriers, bricks that share the carry of a brick with 1 or more other brick
   for idx in range(len(carried)):
      if len(carried[idx]) == 0 and bricks[idx][2].beginZ != 0:
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

   # the number of bricks that can be removed independantly without toppling the pile is the number of bricks
   # that do no carry another brick + the number of bricks that only carry bricks also carried by another brick
   return len(nonCarriers) + len(coCarriersList)


# Calculate and return the sum of the numbers of bricks that would fall for each brick if it was removed
#
# @param inputFilePath: the input file
# @return: the sum of the numbers of bricks that would fall for each brick if it was removed
#
def part2(inputFilePath: str) -> int:
   bricks, space = ingest(inputFilePath)
   answer = 0
   for idx in range(len(bricks)):  # for each brick
      deleted = [idx]  # delete the brick
      for z in range(1, len(space)):
         for y in range(len(space[z])):
            for x in range(len(space[y])):
               # search the state space bottom to top, if a brick is not deleted
               if space[z][y][x] != -1 and space[z][y][x] not in deleted:
                  # if there is not brick bellow or it's been deleted
                  if space[z - 1][y][x] == -1 or space[z - 1][y][x] in deleted:
                     allEmptySpaceOrDeleted = True
                     for yb in range(len(space[z])):
                        for xb in range(len(space[yb])):
                           # perform the same test for all the bottom cells of the brick
                           if (space[z][yb][xb] == space[z][y][x] and
                               space[z - 1][yb][xb] != -1 and
                                   space[z - 1][yb][xb] not in deleted):
                              allEmptySpaceOrDeleted = False
                              break
                     if allEmptySpaceOrDeleted:  # the brick is not carried
                        deleted.append(space[z][y][x])  # delete the brick
                        answer += 1
   return answer


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
