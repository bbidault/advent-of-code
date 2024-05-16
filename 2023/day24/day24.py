# https://adventofcode.com/2023/day/24

import sympy


# The stone class defines a hail stone by its position and velocity
#
class stone():
   # Constructor with parameters
   #
   # @param id: the identifier of the stone
   # @param pos: the position of the stone
   # @param vel: the velocity of the stone
   #
   def __init__(self, id: int, pos: list, vel: list):
      self.id = id
      self.posX = int(pos[0])
      self.posY = int(pos[1])
      self.posZ = int(pos[2])
      self.velX = int(vel[0])
      self.velY = int(vel[1])
      self.velZ = int(vel[2])


# Evaluate if two given stone paths intersect on the XY 2D plane
#
# @param stone1: a stone
# @param stone2: another stone
# @param bounds: the intersection search area bounds
# @return: whether the stone paths intersect or not
#
def intersectXY(stone1: stone, stone2: stone, bounds: tuple) -> bool:
   m1 = stone1.velY / stone1.velX
   m2 = stone2.velY / stone2.velX
   if m1 == m2:   # they move in parallel and never meet
      return False
   b1 = stone1.posY - m1 * stone1.posX
   b2 = stone2.posY - m2 * stone2.posX
   x = (b2 - b1) / (m1 - m2)
   y = m1 * x + b1
   if (bounds[0] <= x <= bounds[1] and
       bounds[0] <= y <= bounds[1] and
       ((x > stone1.posX and stone1.velX > 0) or (x < stone1.posX and stone1.velX < 0)) and  # intersection needs to happen in the future
           ((x > stone2.posX and stone2.velX > 0) or (x < stone2.posX and stone2.velX < 0))):
      return True
   return False


# Ingest the given input file and returns a list of stones
#
# @param inputFilePath: a input file
# @return: a list of stones
#
def ingest(inputFilePath: str) -> list:
   stones = []
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   id = 0
   for line in lines:
      pos, vel = line.split(" @ ")
      pos = pos.split(",")
      vel = vel.split(",")
      stones.append(stone(id, pos, vel))
      id += 1
   return stones


# Calculate and return the number of intersecting paths of a given list stones on the XY 2D plane
#
# @param inputFilePath: a input file
# @param bounds: the intersection search area bounds
# @return: the number of intersecting paths of a given list stones
#
def part1(inputFilePath: str, bounds: tuple,) -> bool:
   stones = ingest(inputFilePath)
   answer = 0
   for stone1 in stones:
      for stone2 in stones:
         if stone1.id != stone2.id and intersectXY(stone1, stone2, bounds):
            answer += 1
   return answer / 2  # divide by 2 because if stone 1 intersect stone 2 then stone 2 intersect stone 1


# Calculate and return the sum of the initial position x, y and z coordinates a stone should have
# to intersect the path of all given stones
#
# @param inputFilePath: a input file
# @return: the sum of the initial position x, y and z coordinates the stone
#
def part2(inputFilePath: str) -> bool:
   stones = ingest(inputFilePath)

   # the system is overly constrained; we assume that the problem has a solution; finding a path intersecting
   # 3 stones becomes sufficient; we setup a system of 6 equations and 6 unknown
   Vsx, Vsy, Vsz, t0, t1, t2 = sympy.symbols('Vsx, Vsy, Vsz, t0, t1, t2')
   eq1 = sympy.Eq(stones[1].posX - stones[2].posX, +(stones[1].velX - Vsx) * t1 + (Vsx - stones[2].velX) * t2)
   eq2 = sympy.Eq(stones[1].posY - stones[2].posY, +(stones[1].velY - Vsy) * t1 + (Vsy - stones[2].velY) * t2)
   eq3 = sympy.Eq(stones[1].posZ - stones[2].posZ, +(stones[1].velZ - Vsz) * t1 + (Vsz - stones[2].velZ) * t2)
   eq4 = sympy.Eq(stones[1].posX - stones[0].posX, +(stones[1].velX - Vsx) * t1 + (Vsx - stones[0].velX) * t0)
   eq5 = sympy.Eq(stones[1].posY - stones[0].posY, +(stones[1].velY - Vsy) * t1 + (Vsy - stones[0].velY) * t0)
   eq6 = sympy.Eq(stones[1].posZ - stones[0].posZ, +(stones[1].velZ - Vsz) * t1 + (Vsz - stones[0].velZ) * t0)
   # use sympy library to solve the system of equations
   Vsx, Vsy, Vsz, t0, t1, t2 = sympy.solve([eq1, eq2, eq3, eq4, eq5, eq6], (Vsx, Vsy, Vsz, t0, t1, t2))[0]

   Psx = stones[1].posX + (Vsx - stones[1].velX) * t1
   Psy = stones[1].posY + (Vsy - stones[1].velY) * t1
   Psz = stones[1].posZ + (Vsz - stones[1].velZ) * t1

   return Psx + Psy + Psz


print("Part 1 test:", part1("test_input.txt", (7, 27)))
print("Part 1 solution:", part1("input.txt", (2e14, 4e14)))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
