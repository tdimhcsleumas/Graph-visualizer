from graph import Graph, Vertex, Edge
from config import *
import heapq
import time


class DisjointSet:
    def __init__(self):
        self.sets = []

    def makeSet(self, item):
        self.sets.append({item})

    # pre: find-set(left) != find-set(right)
    def union(self, left, right):
        left_set = None
        right_set = None
        for set in self.sets:
            if left in set:
                left_set = set
            if right in set:
                right_set = set

        assert (left_set != right_set and left_set and right_set)
        self.sets.remove(left_set)
        self.sets.remove(right_set)

        self.sets.append(left_set.union(right_set))

    def findSet(self, item):
        for set in self.sets:
            if item in set:
                return set
        raise Exception("asdf")


def solve(G: Graph, *args, **kwargs):
    F = set()
    D = DisjointSet()
    for _, x in G.vertices.items():
        D.makeSet(x)
    for edge in sorted(G.edges, key=lambda x: x.weight):
        time.sleep(1)
        if D.findSet(edge.start) != D.findSet(edge.end):
            F.add(edge)
            edge.setColor(BLUE)
            D.union(edge.start, edge.end)
