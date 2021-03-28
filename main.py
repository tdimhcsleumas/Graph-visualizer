import pygame
from graph import Graph, Vertex, Edge
from random import randint
from config import *
from algorithms import kruskal, prim
from concurrent.futures import ThreadPoolExecutor

SIZE = (750, 750)


def makeGrid() -> tuple:
    grid = Graph(0, 0, SIZE[0], SIZE[1])
    radius = 5
    rows = 4
    columns = 4
    stepX = grid.width // (columns + 1)
    stepY = grid.height // (rows + 1)
    vertices = {}
    edges = []

    idx = 0
    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            vertex = Vertex(
                (grid.x + stepX * i, grid.y + stepY * j),
                radius,
                idx
            )
            idx += 1
            if i != 1:
                edges.append(Edge(vertex,
                                  vertices[i - 1, j],
                                  randint(0, 10)))

            if j != 1:
                edges.append(Edge(vertex,
                                  vertices[i, j - 1],
                                  randint(0, 10)))

            vertices[i, j] = vertex

    start = vertices[1, 1]
    grid.setVertexSet(list(vertices.values()))
    grid.setEdgeSet(edges)

    return grid, start

class State:
    def __init__(self):
        self.running = False

    def markStopped(self, *args, **kwargs):
        self.running = False

    def markStarted(self):
        self.running = True

    def isRunning(self):
        return self.running

def main():
    WIN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("RSMT Algorithm Visualizer")
    pygame.init()

    grid, start = makeGrid()
    task_queue = ThreadPoolExecutor(max_workers=1)
    state = State()

    run = True
    while run:

        grid.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if not state.isRunning():
                    if event.key == pygame.K_r:
                        grid, start = makeGrid()
                    elif event.key == pygame.K_k:
                        state.markStarted()
                        task_queue.submit(kruskal.solve, grid).add_done_callback(state.markStopped)
                    elif event.key == pygame.K_p:
                        state.markStarted()
                        task_queue.submit(prim.solve, grid, start).add_done_callback(state.markStopped)
                else:
                    print("currently running!")

            if event.type == pygame.QUIT:
                run = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
