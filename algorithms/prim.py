from config import *
from graph import Graph, Edge, Vertex
import heapq
from collections import defaultdict
import time


class PriorityQueue:
    def __init__(self, items: list, priority: callable):
        self.heap = []
        self.priority = priority
        self._init_(items)

    def _init_(self, items):
        for item in items:
            self.push(item)

    def pop(self):
        return heapq.heappop(self.heap)

    def push(self, item):
        heapq.heappush(self.heap, (self.priority(item), item))

    def hasItem(self, item):
        for _, v in self.heap:
            if v == item:
                return True
        return False

    def isEmpty(self):
        return not self.heap


def order(left: Vertex, right: Vertex):
    if left.idx < right.idx:
        return left, right
    else:
        return right, left


def doPrims(V: list, Adj: dict, Edges: dict, r: Vertex):
    key = {}
    p = {}
    r.color = BLUE
    for v in V:
        key[v.idx] = float("inf")
        p[v.idx] = None
    key[r.idx] = 0
    Q = PriorityQueue(V, lambda z: z.idx)
    while not Q.isEmpty():
        _, x = Q.pop()
        x.color = GREEN
        for y in Adj[x.idx]:
            if Q.hasItem(y) and Edges[order(x, y)].weight < key[y.idx]:
                time.sleep(0.5)
                y.color = YELLOW
                p[y.idx] = x
                key[y.idx] = Edges[order(x, y)].weight
                Edges[order(x, y)].color = YELLOW
    return p


def solve(G: Graph, r: Vertex):
    try:
        Adj = defaultdict(lambda: list())
        Edges = {}

        for edge in G.edges:
            Adj[edge.start.idx].append(edge.end)
            Adj[edge.end.idx].append(edge.start)
            Edges[order(edge.start, edge.end)] = edge

        parents = doPrims(G.vertices, Adj, Edges, r)

        for idx, parent in parents.items():
            if parent:
                Edges[order(G.vertices[idx], parent)].color = RED
    except Exception as e:
        print(e.__str__())
