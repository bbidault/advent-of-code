import random

inputFile = open("input.txt", "r")
nodes = {}
Lines = inputFile.readlines()
for line in Lines:
   source, targets = line.split(":")
   targets = targets.split(" ")
   for target in targets:
      if source not in nodes:
         nodes[source] = set()
      nodes[source].add(target.strip())
      if target.strip() not in nodes:
         nodes[target.strip()] = set()
      nodes[target.strip()].add(source)


edges = []

while len(edges) != 3:

   edges.clear()

   for key, values in nodes.items():
      for value in values:
         if [value, key] not in edges and [key, value] not in edges:
            edges.append([key, value])

   nodesLeft = set()
   for edge in edges:
      nodesLeft.add(edge[0])
      nodesLeft.add(edge[1])
   while len(nodesLeft) > 2:
      # chose an edge at random
      chosenOne = random.randrange(len(edges))
      nodeA, nodeB = edges[chosenOne]

      # remove the chosen edge and its twins
      edges[:] = [edge for edge in edges if not ((edge[0] == nodeA and edge[1] == nodeB) or (edge[1] == nodeA and edge[0] == nodeB))]

      # replace instance of one node with the other (merge the nodes)
      for edge in edges:
         if edge[0] == nodeB:
            edge[0] = nodeA
         if edge[1] == nodeB:
            edge[1] = nodeA

      # generate a list of nodes left
      nodesLeft.clear()
      for edge in edges:
         nodesLeft.add(edge[0])
         nodesLeft.add(edge[1])
      # print(len(nodesLeft))

   print(len(edges))

print(edges)

inputFile.close()
