import copy

answer = 0


class xmas:
   def __init__(self, x, m, a, s):
      self.dict = {"x": x, "m": m, "a": a, "s": s}


class test:
   def __init__(self, category: str, logic: str, number: int, exi: str):
      self.category = category
      self.logic = logic
      self.number = number
      self.exi = exi

   def evaluate(self, xmas: xmas) -> str:
      if self.logic == ">":
         if xmas.dict[self.category] > self.number:
            return self.exi
      elif self.logic == "<":
         if xmas.dict[self.category] < self.number:
            return self.exi
      return "F"


inputFile = open("input.txt", "r")
testsDict = {}
Lines = inputFile.readlines()
for line in Lines:
   if not line.strip():
      break
   open = line.find("{")
   close = line.find("}")
   testsStr = line[open + 1:close].split(",")
   id = line[0:open]
   testsDict[id] = []
   for st in testsStr:
      if len(st) > 1 and st[1] in "><":
         # print(st)
         check, exi = st.split(":")
         testsDict[id].append(test(check[0], check[1], int(check[2:]), exi))
      else:
         testsDict[id].append(test("x", ">", -1, st))

# print("length " + str(len(testsDict)))
# for key, value in testsDict.items():
#     print("sub " + str(len(value)))

# parts = [xmas(787,2655,1222,2876),
#          xmas(1679,44,2067,496),
#          xmas(2036,264,79,2244),
#          xmas(2461,1339,466,291),
#          xmas(2127,1623,2188,1013)]


# part 1
# for part in parts:
#     print("New xmas")
#     testStr = "in"
#     testIdx = 0
#     while True:
#         testO = testsDict[testStr][testIdx]
#         result = testO.evaluate(part)
#         print(result)
#         if result == "A":
#             print("   Accepted")
#             answer += sum(part.dict.values())
#             break
#         elif result == "R":
#             print("   Rejected")
#             break
#         elif result == "F":
#             print("   Next condition")
#             testIdx += 1
#         else:
#             print("   Going to " + result)
#             testStr = result
#             testIdx = 0

def xmasSum(xmas: xmas):
   return (xmas.dict["x"][1] - xmas.dict["x"][0] + 1) * (xmas.dict["m"][1] - xmas.dict["m"][0] + 1) * (xmas.dict["a"][1] - xmas.dict["a"][0] + 1) * (xmas.dict["s"][1] - xmas.dict["s"][0] + 1)


def printXMAS(xmas: xmas):
   print(str(xmas.dict["x"][0]) + " - " + str(xmas.dict["x"][1]) + " / " +
         str(xmas.dict["m"][0]) + " - " + str(xmas.dict["m"][1]) + " / " +
         str(xmas.dict["a"][0]) + " - " + str(xmas.dict["a"][1]) + " / " +
         str(xmas.dict["s"][0]) + " - " + str(xmas.dict["s"][1]))


def recurse(testStr: str, testIdx: int, xmas: xmas):
   # sum = 0
   testO = testsDict[testStr][testIdx]
   if xmas.dict[testO.category][1] < testO.number:  # full range inferior
      if testO.logic == ">":
         # sum +=
         recurse(testStr, testIdx + 1, xmas)
      else:  # <
         if testO.exi == "A":
            # printXMAS(xmas)
            print(xmasSum(xmas))  # return xmasSum(xmas)
         elif testO.exi != "R":
            # sum +=
            recurse(testO.exi, 0, xmas)
   elif xmas.dict[testO.category][0] > testO.number:  # full range superior
      if testO.logic == ">":
         if testO.exi == "A":
            # printXMAS(xmas)
            print(xmasSum(xmas))  # return xmasSum(xmas)
         elif testO.exi != "R":
            # sum +=
            recurse(testO.exi, 0, xmas)
      else:  # <
         recurse(testStr, testIdx + 1, xmas)
   else:  # number in range
      xmasUp = copy.deepcopy(xmas)
      xmasDown = copy.deepcopy(xmas)
      if testO.logic == ">":
         xmasUp.dict[testO.category] = (testO.number + 1, xmas.dict[testO.category][1])
         xmasDown.dict[testO.category] = (xmas.dict[testO.category][0], testO.number)
         if testO.exi == "A":
            # printXMAS(xmasUp)
            print(xmasSum(xmasUp))  # return xmasSum(xmasUp) +
         elif testO.exi != "R":
            # sum +=
            recurse(testO.exi, 0, xmasUp)
         recurse(testStr, testIdx + 1, xmasDown)
      else:  # <
         xmasUp.dict[testO.category] = (testO.number, xmas.dict[testO.category][1])
         xmasDown.dict[testO.category] = (xmas.dict[testO.category][0], testO.number - 1)
         if testO.exi == "A":
            # printXMAS(xmasDown)
            print(xmasSum(xmasDown))  # return xmasSum(xmasDown) +
         elif testO.exi != "R":
            # sum +=
            recurse(testO.exi, 0, xmasDown)
         recurse(testStr, testIdx + 1, xmasUp)
   # return sum


answer = recurse("in", 0, xmas((1, 4000), (1, 4000), (1, 4000), (1, 4000)))

print(answer)
inputFile.close()

167409079868000
