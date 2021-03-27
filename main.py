import pygame
from graph import Graph, Vertex, Edge
from random import randint
from config import *
from algorithms import kruskal
from task_queue import TaskQueue

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

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            vertex = Vertex(
                (grid.x + stepX * i, grid.y + stepY * j),
                radius
            )
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
    start.color = BLUE
    grid.setVertexSet({id(v): v for _, v in vertices.items()})
    grid.setEdgeSet(edges)

    return grid, start


def main():
    WIN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("RSMT Algorithm Visualizer")
    pygame.init()

    task_queue = TaskQueue()
    grid, start = makeGrid()

    run = True
    while run:

        grid.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                task_queue.add_task(kruskal.solve, (grid), {})

            if event.type == pygame.QUIT:
                run = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
