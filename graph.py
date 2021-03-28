import pygame
import numpy


def drawTextCenter(text, surface, x, y):
    font = pygame.font.SysFont('calibri', 20)
    text_object = font.render(text, True, (0, 0, 0))
    text_rectangle = text_object.get_rect(center=(int(x), int(y)))
    surface.blit(text_object, text_rectangle)


class Vertex:
    def __init__(self, center, radius, idx):
        self.center = center
        self.radius = radius
        self.color = (0, 0, 0)
        self.idx = idx

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)


class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.color = (0, 0, 0)
        self.weight = weight

    def setColor(self, color):
        self.color = color

    def draw(self, surface):
        step = 10
        avg = ((self.start.center[0] + self.end.center[0]) // 2, (self.start.center[1] + self.end.center[1]) // 2)

        if self.end.center[0] != self.start.center[0]:
            direction = (self.end.center[1] - self.start.center[1]) / (self.end.center[0] - self.start.center[0])
        else:
            direction = "inf"

        # TODO: be smarter about linear algebra
        if direction == 0:
            point = (avg[0], avg[1] + step)
        elif direction == "inf":
            point = (avg[0] + step, avg[1])
        else:
            point = avg

        pygame.draw.line(surface, self.color, self.start.center, self.end.center, 4)
        drawTextCenter(f"{self.weight}", surface, point[0], point[1])


class Graph(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vertices = []
        self.edges = []

    def setEdgeSet(self, edges):
        self.edges = edges

    def setVertexSet(self, grid):
        self.vertices = grid

    def insertItem(self, item):
        self.vertices.append = item

    @classmethod
    def createFromJson(cls, data):
        # TODO: this
        return cls(0, 0, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self)

        for edge in self.edges:
            edge.draw(surface)

        for v in self.vertices:
            v.draw(surface)
