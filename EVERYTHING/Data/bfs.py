import pygame
from queue import Queue

# graph = {
#     'a':['b', 'd'],
#     'b':['c', 'a'],
#     'c':['b'],
#     'd':['a', 'e', 'f'],
#     'e':['d', 'f', 'g'],
#     'f':['d', 'h', 'e'],
#     'g':['e', 'h'],
#     'h':['f', 'g']
# }
# visited = {}
# level = {}
# parent = {}
# bfsto = []
# queue = Queue()
#
# for node in graph.keys():
#     visited[node] = False
#     parent[node] = None
#     level[node] = -1
#
# s = 'c'
# visited[s] = True
# level[s] = 0
# queue.put(s)
#
# while not queue.empty():
#     u = queue.get()
#     bfsto.append(u)
#
#     for v in graph[u]:
#         if visited[v] != 1:
#             visited[v] = True
#             parent[v] = u
#             level[v] = level[u] + 1
#             queue.put(v)
#
# v = 'h'
# path = []
# while v is not None:
#     path.append(v)
#     v = parent[v]
# path.reverse()
# print(path)

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('BFS Test')

class Nodes(object):
    def __init__(self, s):
        self.graph = {
            'a':['b', 'd'],
            'b':['c', 'a'],
            'c':['b'],
            'd':['a', 'e', 'f'],
            'e':['d', 'f', 'g'],
            'f':['d', 'h', 'e'],
            'g':['e', 'h'],
            'h':['f', 'g']
        }
        self.visited = {}
        self.level = {}
        self.parent = {}
        self.node_positions = {
            'a':[200, 100],
            'b':[100, 100],
            'c':[100, 200],
            'd':[200, 200],
            'e':[300, 100],
            'f':[300, 200],
            'g':[400, 100],
            'h':[400, 200]

        }
        self.bfsto = []
        self.queue = Queue()
        for node in self.graph.keys():
            self.visited[node] = False
            self.parent[node] = None
            self.level[node] = -1
        self.start = s
        self.visited[s] = True
        self.level[s] = 0
        self.queue.put(s)

    def main(self, v):
        while not self.queue.empty():
            u = self.queue.get()
            self.bfsto.append(u)

            for v in self.graph[u]:
                if self.visited[v] != 1:
                    self.visited[v] = True
                    self.parent[v] = u
                    self.level[v] = self.level[u] + 1
                    self.queue.put(v)

        self.path = []
        self.goal = v
        while v is not None:
            self.path.append(v)
            v = self.parent[v]
        self.path.reverse()

    def render(self, surface):
        all_node_pos = []
        for node in self.node_positions.items():
            node_id, node_pos = node
            all_node_pos.append([node_id, node_pos[0], node_pos[1]])
            if node_id is self.goal:
                pygame.draw.circle(surface, (255, 0, 0), (node_pos[0], node_pos[1]), 10)
            elif node_id is self.start:
                pygame.draw.circle(surface, (0, 0, 255), (node_pos[0], node_pos[1]), 10)
            elif node_id in self.path:
                pygame.draw.circle(surface, (0, 255, 0), (node_pos[0], node_pos[1]), 10)
            else:
                pygame.draw.circle(surface, (255, 255, 255), (node_pos[0], node_pos[1]), 10)
        for node in all_node_pos:
            neighbors = self.graph[node[0]]
            for neighbor in neighbors:
                neighbor_pos = self.node_positions[neighbor]
                if neighbor not in self.path:
                    pygame.draw.line(surface, (255, 255, 255), (neighbor_pos[0], neighbor_pos[1]), (node[1], node[2]), 3)
                else:
                    pygame.draw.line(surface, (255, 255, 255), (neighbor_pos[0], neighbor_pos[1]), (node[1], node[2]), 3)


player_x = 50
player_y = 50
player = pygame.Rect(player_x, player_y, 50, 50)

nodes = Nodes('c')
clock = pygame.time.Clock()
running = True
goal_node = 'e'
while running:
    screen.fill((0, 0, 0))
    nodes.main(goal_node)
    nodes.render(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player_x += 10
            if event.key == pygame.K_a:
                player_x -= 10
            if event.key == pygame.K_w:
                player_y -= 10
            if event.key == pygame.K_s:
                player_y += 10
            if event.key == pygame.K_k:
                goal_node = 'h'

    pygame.display.update()
    clock.tick(60)
