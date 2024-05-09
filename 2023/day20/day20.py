# https://adventofcode.com/2023/day/20

# The Module base class defines a module with a name and a list of target modules
#
class Module:
   # Constructor with parameters
   #
   # @param name: the name of the module
   # @param targets: the target modules of the module
   #
   def __init__(self, name: str, targets: list):
      self.name = name
      self.targets = targets


# The FlipFlop class inherits from the base class Module. The FlipFlop module as a state "on" (True) or "off" (False)
#
class FlipFlop(Module):
   # Constructor with parameters
   #
   # @param name: the name of the module
   # @param targets: the target modules of the module
   #
   def __init__(self, name: str, targets: list):
      Module.__init__(self, name, targets)
      self.state = False

   # The receive function of the FlipFlop module. If the received message is a "low" (False), the module sends
   # "low" (False) or "high" (True) messages to all its target modules depending on its state and flips its state
   #
   # @param source: the source of the message
   # @param msg: a "high" (True) or "low" (False) message
   # @param queue: a queue of messages
   #
   def receive(self, source: str, msg: bool, queue: list):
      if not msg:  # low
         for target in self.targets:
            queue.append((self.name, target, not self.state))
         self.state = not self.state


# The Conjunction class inherits from the base class Module.
# The Conjunction module keeps track of the messages received by source module.
#
class Conjunction(Module):
   # Constructor with parameters
   #
   # @param name: the name of the module
   # @param targets: the target modules of the module
   #
   def __init__(self, name: str, targets: list):
      Module.__init__(self, name, targets)
      self.memory = {}

   # Add a source module for the module
   #
   # @param source: the name of a source module
   #
   def addSource(self, source: str):
      self.memory[source] = False

   # The receive function of the Conjunction module. If all the recorded messages are "high" (True), the module sends
   # a "low" (False) message to all its target modules, otherwise it sends "high" (True) to all its target modules.
   #
   # @param source: the source of the message
   # @param msg: a "high" (True) or "low" (False) message
   # @param queue: a queue of messages
   #
   def receive(self, source: str, msg: bool, queue: list):
      self.memory[source] = msg
      allHigh = all([value for _, value in self.memory.items()])
      for target in self.targets:
         queue.append((self.name, target, not allHigh))


# The Broadcaster class inherits from the base class Module.
#
class Broadcaster(Module):
   # Constructor with parameters
   #
   # @param name: the name of the module
   # @param targets: the target modules of the module
   #
   def __init__(self, name: str, targets: list):
      Module.__init__(self, name, targets)

   # The receive function of the Broadcaster module. The Broadcaster module
   # forwards the received message to all its target modules.
   #
   # @param source: the source of the message
   # @param msg: a "high" (True) or "low" (False) message
   # @param queue: a queue of messages
   #
   def receive(self, source: str, msg: bool, queue: list):
      for target in self.targets:
         queue.append((self.name, target, msg))


# Ingest the given input file and return a list of Module objects
#
# @param inputFilePath: the input file
# @return: a list of Module objects
#
def ingest(inputFilePath: str) -> list:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   modules = {}
   for line in lines:
      content = line.split(" -> ")
      name = content[0][1:]
      targets = content[1].strip().split(", ")
      if line[0] == "%":
         modules[name] = FlipFlop(name, targets)
      elif line[0] == "&":
         modules[name] = Conjunction(name, targets)
      elif line[0] == "b":
         modules["broadcaster"] = Broadcaster("broadcaster", targets)

   for line in lines:
      content = line.split(" -> ")
      name = content[0][1:]
      targets = content[1].strip().split(", ")
      if line[0] == "%" or line[0] == "&":
         for target in targets:
            if target not in ("rx", "output") and isinstance(modules[target], Conjunction):
               modules[target].addSource(name)
      elif line[0] == "b":
         for target in targets:
            if target not in ("rx", "output") and isinstance(modules[target], Conjunction):
               modules[target].addSource("broadcaster")

   return modules


# Send 1000 "low" (False) message to the broadcaster module and return the product
# of all "high" (True) and "low" (False) messages sent on the network
#
# @param inputFilePath: the input file
# @return: the product of all "high" (True) and "low" (False) messages sent on the network
#
def part1(inputFilePath: str) -> int:
   modules = ingest(inputFilePath)
   highs = 0
   lows = 0
   for _ in range(1000):
      queue = []
      queue.append(("button", "broadcaster", False))
      while queue:
         source, target, msg = queue.pop(0)
         if msg:  # high
            highs += 1
         else:  # low
            lows += 1
         if target not in ("rx", "output"):
            modules[target].receive(source, msg, queue)
   return highs * lows


# Calculate and return the number of "low" (False) message necessary to send to
# the broadcaster module to send a single "high" (True) to the module named "zp"
#
# @param inputFilePath: the input file
# @return: the number of "low" (False) message necessary to send to the broadcaster module to send a single "high" (True) to the module named "zp"
#
def part2(inputFilePath: str) -> int:
   modules = ingest(inputFilePath)
   idx = 0
   sb = 0
   nd = 0
   ds = 0
   hf = 0
   while any(cycle == 0 for cycle in [sb, nd, ds, hf]):
      idx += 1
      queue = []
      queue.append(("button", "broadcaster", False))
      while queue:
         source, target, msg = queue.pop(0)
         if target == "zp" and msg:  # high
            if source == "sb":
               sb = idx
            elif source == "nd":
               nd = idx
            elif source == "ds":
               ds = idx
            elif source == "hf":
               hf = idx
         if target != "rx":
            modules[target].receive(source, msg, queue)
   return sb * nd * ds * hf


print("Part 1 test 1:", part1("test_input_1_part_1.txt"))
print("Part 1 test 2:", part1("test_input_2_part_1.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 solution:", part2("input.txt"))
