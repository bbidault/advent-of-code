import math
import copy


class stone():
   def __init__(self, idx: int, posx: int, posy: int, posz: int, velx: int, vely: int, velz: int):
      self.idx = idx
      self.posx = posx
      self.posy = posy
      self.posz = posz
      self.velx = velx
      self.vely = vely
      self.velz = velz

   def print(self):
      print(str(self.posx) + " " + str(self.posy) + " " + str(self.posz) + " " + str(self.velx) + " " + str(self.vely) + " " + str(self.velz))


def intersectxy(stone1: stone, stone2: stone):
   m1 = stone1.vely / stone1.velx
   m2 = stone2.vely / stone2.velx
   if m1 == m2:   # they move in parallel and never meet
      return False
   b1 = stone1.posy - m1 * stone1.posx
   b2 = stone2.posy - m2 * stone2.posx
   x = (b2 - b1) / (m1 - m2)
   y = m1 * x + b1
   if (2e14 <= x <= 4e14 and
       2e14 <= y <= 4e14 and
       ((x > stone1.posx and stone1.velx > 0) or (x < stone1.posx and stone1.velx < 0)) and  # intersection needs to happen in the future
           ((x > stone2.posx and stone2.velx > 0) or (x < stone2.posx and stone2.velx < 0))):
      return True
   return False


def intersectxyz(stone1: stone, stone2: stone):
   m1 = stone1.vely / stone1.velx
   m2 = stone2.vely / stone2.velx
   m3 = stone1.velz / stone1.velx
   m4 = stone2.velz / stone2.velx
   m5 = stone1.vely / stone1.velz
   m6 = stone2.vely / stone2.velz
   if m1 == m2 and m3 == m4 and m5 == m6:
      return False
   posDif = [stone1.posx - stone2.posx, stone1.posy - stone2.posy, stone1.posz - stone2.posz]
   crossProduct = [stone1.vely * stone2.velz - stone1.velz * stone2.vely,
                   stone1.velx * stone2.velz - stone1.velz * stone2.velx, stone1.velx * stone2.vely - stone1.vely * stone2.velx]
   dotProduct = posDif[0] * crossProduct[0] + posDif[1] * crossProduct[1] + posDif[2] * crossProduct[2]
   if dotProduct == 0:
      return True
   return False


stones = []

inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
inputFile.close()
idx = 0
for line in Lines:
   pos, vel = line.split(" @ ")
   pos = pos.split(",")
   vel = vel.split(",")
   stones.append(stone(idx,
                       int(pos[0].strip()),
                       int(pos[1].strip()),
                       int(pos[2].strip()),
                       int(vel[0].strip()),
                       int(vel[1].strip()),
                       int(vel[2].strip())))
   idx += 1

# part 1
answer = 0
for stone1 in stones:
   for stone2 in stones:
      if stone1.idx != stone2.idx and intersectxy(stone1, stone2):
         answer += 1
print(answer / 2)

print()

# part 2
answer = 0
for stone1 in stones:
   for stone2 in stones:
      if stone1.idx != stone2.idx:
         count = 0
         if stone1.posx == stone2.posx:
            count += 1
         if stone1.posy == stone2.posy:
            count += 1
         if stone1.posz == stone2.posz:
            count += 1
         if stone1.velx == stone2.velx:
            count += 1
         if stone1.vely == stone2.vely:
            count += 1
         if stone1.velz == stone2.velz:
            count += 1
         if count > 1:
            print(count)

# dist = 9999999999999999999999999999999
# for stone1 in stones:
#     for stone2 in stones:
#         if stone1.idx != stone2.idx:
#             distance = ((stone1.posx - stone2.posx) * (stone1.posx - stone2.posx) +
#                         (stone1.posy - stone2.posy) * (stone1.posy - stone2.posy) +
#                         (stone1.posz - stone2.posz) * (stone1.posz - stone2.posz))
#             if distance < dist:
#                 dist = distance
#                 print("close!")
#                 stone1.print()
#                 stone2.print()

stoneA = stone(0, 379007729560472, 324179575229054, 237304102573018, -201, -67, 40)
stoneB = stone(1, 376945215322495, 321998487931571, 236756161317265, 74, -172, -179)

answer = 0

# for vx in range(1000):
# for vx in range(-1,-1000,-1):
#     if vx%10 == 0:
#         print("vx " + str(vx))
#     for vy in range(-1000,1000):
#         for vz in range(-1000,1000):
#             stoneA2 = copy.deepcopy(stoneA)
#             stoneA2.velx -= vx
#             stoneA2.vely -= vy
#             stoneA2.velz -= vz
#             stoneB2 = copy.deepcopy(stoneB)
#             stoneB2.velx -= vx
#             stoneB2.vely -= vy
#             stoneB2.velz -= vz
#             if (stoneA2.velx != 0 and
#                 stoneA2.vely != 0 and
#                 stoneA2.velz != 0 and
#                 stoneB2.velx != 0 and
#                 stoneB2.vely != 0 and
#                 stoneB2.velz != 0 and
#                 intersectxyz(stoneA2, stoneB2)):
#                 print(str(vx) + " " + str(vy) + " " + str(vz))
