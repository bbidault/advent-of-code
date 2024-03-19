
class Module:
   def __init__(self, name: str, targets: tuple):
      self.name = name
      self.targets = targets


class FlipFlop(Module):
   def __init__(self, name: str, targets: tuple):
      Module.__init__(self, name, targets)
      self.state = "off"

   def receive(self, source: str, msg: str, queue: list):
      if msg == "low":
         for target in self.targets:
            if self.state == "on":
               queue.append((self.name, target, "low"))
               # print("append source " + self.name + " target " + target)
            else:
               queue.append((self.name, target, "high"))
               # print("append source " + self.name + " target " + target)
         if self.state == "on":
            self.state = "off"
         else:
            self.state = "on"


class Conjunction(Module):
   def __init__(self, name: str, targets: tuple):
      Module.__init__(self, name, targets)
      self.memory = {}

   def addSource(self, source: str):
      self.memory[source] = "low"

   def receive(self, source: str, msg: str, queue: list):
      self.memory[source] = msg
      allHigh = True
      for key, value in self.memory.items():
         if value == "low":
            allHigh = False
            break
      for target in self.targets:
         if allHigh:
            queue.append((self.name, target, "low"))
            # print("append source " + self.name + " target " + target)
         else:
            queue.append((self.name, target, "high"))
            # print("append source " + self.name + " target " + target)


class Broadcaster(Module):
   def __init__(self, name: str, targets: tuple):
      Module.__init__(self, name, targets)

   def receive(self, source: str, msg: str, queue: list):
      for target in self.targets:
         queue.append((self.name, target, msg))
         # print("append source " + self.name + " target " + target)


outputs = ("rx")

inputFile = open("input.txt", "r")
modules = {}
Lines = inputFile.readlines()
for line in Lines:
   content = line.split(" -> ")
   name = content[0][1:]
   targets = content[1].strip().split(", ")
   # print(line[0] + " " + name + " " + str(targets))
   if line[0] == "%":
      modules[name] = FlipFlop(name, targets)
   elif line[0] == "&":
      modules[name] = Conjunction(name, targets)
   elif line[0] == "b":
      modules["broadcaster"] = Broadcaster("broadcaster", targets)

for line in Lines:
   content = line.split(" -> ")
   name = content[0][1:]
   targets = content[1].strip().split(", ")
   if line[0] == "%" or line[0] == "&":
      for target in targets:
         if target not in outputs and isinstance(modules[target], Conjunction):
            modules[target].addSource(name)
   elif line[0] == "b":
      for target in targets:
         if target not in outputs and isinstance(modules[target], Conjunction):
            modules[target].addSource("broadcaster")


# for key, value in modules.items():
#     print(key + ": " + value.name + " " + str(value.targets) )

highs = 0
lows = 0

# idx = 0
# while True:
#     idx += 1
#     queue = []
#     queue.append(("button", "broadcaster", "low"))
#     while queue:
#         source, target, msg = queue.pop(0)
#         if msg == "high":
#             highs += 1
#         elif msg == "low":
#             lows += 1
#         if target == "zp" and msg == "high" and source == "hf":
#             print(idx)
#         # print(str(source) + " -" + str(msg) + "-> " + str(target))
#         if target not in outputs:
#             modules[target].receive(source, msg, queue)

print(3797 * 3917 * 3733 * 3877)

# print(str(lows) + " " + str(highs))
# print(highs*lows)
inputFile.close()

# 3797 3917 3733 3877
