# https://adventofcode.com/2023/day/25
# implementing Karger's algorithm to find the minimum 3 edge cut in the given graph.
# return the product of the two post-cut graphs size has a solution.

import copy
import random

# ingest the input file, populate a dictionary of nodes with targets
inputFile = open("input.txt", "r")
lines = inputFile.readlines()
inputFile.close()
nodes = {}
for line in lines:
   source, targets = line.split(":")
   targets = targets.split(" ")
   for target in targets:
      if source not in nodes:
         nodes[source] = set()
      nodes[source].add(target.strip())
      if target.strip() not in nodes:
         nodes[target.strip()] = set()
      nodes[target.strip()].add(source)

# generate the topology graph
topology = []
for key, values in nodes.items():
   for value in values:
      if [value, key] not in topology and [key, value] not in topology:
         topology.append([key, value])

# Karger's algortihm is an algorithm "with high probability" which means it has a high probability of
# returning the right answer. Since we know the size of the answer and we assume there is only one
# valid answer, we can implement the algorithm and let it recompute until it finds the right answer.
edges = []
while len(edges) != 3:
   edges = copy.deepcopy(topology)

   # prepare a set of "nodes left" to calculate the size of the two post-cut graphs when the algorithm completes
   nodesLeft = set()
   for edge in edges:
      nodesLeft.add(edge[0])
      nodesLeft.add(edge[1])
   nodesAndSizeleft = {}
   for node in nodesLeft:
      nodesAndSizeleft[node] = 1

   while len(nodesAndSizeleft) > 2:
      # choose an edge at random
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
      # add the size of sub-graph B to the sise of sub-graph A
      nodesAndSizeleft[nodeA] += nodesAndSizeleft[nodeB]
      del nodesAndSizeleft[nodeB]

sizes = list(nodesAndSizeleft.values())
print("Part 1 solution:", sizes[0] * sizes[1])
print("No part 2! Merry Christmas!")
