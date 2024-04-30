# https://adventofcode.com/2023/day/19

import copy


# The xmas class defines a machine part (part 1) or range of parts (part 2) with category ratings
#
class xmas:
   # Constructor from parameters
   #
   # @param x: The "Extremely cool looking" category rating of the part(s), a number (part 1) or a range/list (part 2)
   # @param m: The "Musical" category rating of the part(s), a number (part 1) or a range/list (part 2)
   # @param a: The "Aerodynamic" category rating of the part(s), a number (part 1) or a range/list (part 2)
   # @param s: The "Shiny" category rating of the part(s), a number (part 1) or a range/list (part 2)
   #
   def __init__(self, x, m, a, s):
      self.dict = {"x": x, "m": m, "a": a, "s": s}

   # Calculate and return the number of possible combinations of a given range of xmas parts (part 2 only)
   #
   # @return: the number of possible combinations of a given range of xmas parts
   #
   def combinations(self):
      return ((self.dict["x"][1] - self.dict["x"][0] + 1) *
              (self.dict["m"][1] - self.dict["m"][0] + 1) *
              (self.dict["a"][1] - self.dict["a"][0] + 1) *
              (self.dict["s"][1] - self.dict["s"][0] + 1))


# The rule class defines a filtering "rule" of a "workflow" for organizing machine parts
#
class rule:
   # Constructor with parameters
   #
   # @param category: The category of the part tested by the rule
   # @param logic: The logic used by the rule < or >
   # @param number: The number to test the category against
   # @param exit: The exit rule if the condition if met
   #
   def __init__(self, category: str, logic: str, number: int, exit: str):
      self.category = category
      self.logic = logic
      self.number = number
      self.exit = exit

   # Test a part defined by a xmas object through the rule
   #
   # @param xmas: The xmas part
   # @return: The exit rule or "F" if the test failed
   #
   def test(self, xmas: xmas) -> str:
      if self.logic == ">":
         if xmas.dict[self.category] > self.number:
            return self.exit
      elif self.logic == "<":
         if xmas.dict[self.category] < self.number:
            return self.exit
      return "F"


# Ingest the given input file and return a dictionary of rules and a list of xmas parts
#
# @param inputFilePath: the input file
# @return: the dictionary of rules and a list of xmas parts
#
def ingest(inputFilePath: str) -> tuple:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   rulesDict = {}
   idx = 0
   # ingest the workflows
   for line in lines:
      if not line.strip():
         break
      openB = line.find("{")
      closeB = line.find("}")
      rulesStr = line[openB + 1:closeB].split(",")
      id = line[0:openB]
      rulesDict[id] = []
      for st in rulesStr:
         if len(st) > 1 and st[1] in "><":
            check, exitt = st.split(":")
            rulesDict[id].append(rule(check[0], check[1], int(check[2:]), exitt))
         else:
            rulesDict[id].append(rule("x", ">", -1, st))
      idx += 1

   # ingest the parts definitions
   parts = []
   for jdx in range(idx + 1, len(lines)):
      cmds = lines[jdx][1:-2].split(",")
      parts.append(xmas(int(cmds[0][2:]), int(cmds[1][2:]), int(cmds[2][2:]), int(cmds[3][2:])))

   return (rulesDict, parts)


# Calculate and return the sum of the ratings of all the accepted parts
#
# @param inputFilePath: the input file
# @return: the sum of the ratings of all the accepted parts
#
def part1(inputFilePath: str) -> int:
   rulesDict, parts = ingest(inputFilePath)
   answer = 0
   for part in parts:
      workflow = "in"
      ruleIdx = 0
      while True:
         rule = rulesDict[workflow][ruleIdx]
         result = rule.test(part)
         if result == "A":  # part accepted
            answer += sum(part.dict.values())
            break
         elif result == "R":  # part rejected
            break
         elif result == "F":  # test failed, move on to the next rule in the workflow
            ruleIdx += 1
         else:
            workflow = result
            ruleIdx = 0
   return answer


# Evaluate a range of given xmas parts and return the number of possible combinations of valid given parts
# If the range is fully superior or inferior to the rule number it's compared against, the machine part is
# evaluated the same way as in part 1. Otherwise, the range is split and each half is evaluated sperately.
#
# @param rulesDict: the dictionary of rules to triage the parts
# @param workflow: the workflow to follow
# @param ruleIdx: the index of the rule to test within the given workflow
# @param xmas: a range of valid xmas parts
# @return: the number of possible combinations of valid given parts
#
def recurse(rulesDict: dict, workflow: str, ruleIdx: int, xmas: xmas):
   sum = 0
   rule = rulesDict[workflow][ruleIdx]
   if xmas.dict[rule.category][1] < rule.number:  # full range inferior
      if rule.logic == ">":
         sum += recurse(rulesDict, workflow, ruleIdx + 1, xmas)
      else:  # <
         if rule.exit == "A":
            sum += xmas.combinations()
         elif rule.exit != "R":
            sum += recurse(rulesDict, rule.exit, 0, xmas)
   elif xmas.dict[rule.category][0] > rule.number:  # full range superior
      if rule.logic == ">":
         if rule.exit == "A":
            sum += xmas.combinations()
         elif rule.exit != "R":
            sum += recurse(rulesDict, rule.exit, 0, xmas)
      else:  # <
         sum += recurse(rulesDict, workflow, ruleIdx + 1, xmas)
   else:  # number in range
      # split the range
      xmasUp = copy.deepcopy(xmas)
      xmasDown = copy.deepcopy(xmas)
      if rule.logic == ">":
         xmasUp.dict[rule.category] = (rule.number + 1, xmas.dict[rule.category][1])
         xmasDown.dict[rule.category] = (xmas.dict[rule.category][0], rule.number)
         if rule.exit == "A":
            sum += xmasUp.combinations()
         elif rule.exit != "R":
            sum += recurse(rulesDict, rule.exit, 0, xmasUp)
         sum += recurse(rulesDict, workflow, ruleIdx + 1, xmasDown)
      else:  # <
         xmasUp.dict[rule.category] = (rule.number, xmas.dict[rule.category][1])
         xmasDown.dict[rule.category] = (xmas.dict[rule.category][0], rule.number - 1)
         if rule.exit == "A":
            sum += xmasDown.combinations()
         elif rule.exit != "R":
            sum += recurse(rulesDict, rule.exit, 0, xmasDown)
         sum += recurse(rulesDict, workflow, ruleIdx + 1, xmasUp)
   return sum


# Calculate and return the number of valid combinations of xmas parts with each category ranging between 1 and 4000
#
# @param inputFilePath: the input file
# @return: the number of valid combinations of xmas parts
#
def part2(inputFilePath: str) -> int:
   rulesDict, _ = ingest(inputFilePath)
   return recurse(rulesDict, "in", 0, xmas((1, 4000), (1, 4000), (1, 4000), (1, 4000)))


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
