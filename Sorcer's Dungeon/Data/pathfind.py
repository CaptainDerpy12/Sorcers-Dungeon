import pygame
from queue import Queue

class Pathfinder(object):
    def __init__(self):
        self.nodes = []
        self.graph = {}
        self.node_positions = {}
        self.path = []
        self.start = None
        self.goal = None

    def main(self, surface, scroll, debug):
        if debug:
            for node in self.node_positions.values():
                node_x, node_y = node[0], node[1]
                pygame.draw.rect(surface, (255, 0, 0), (node_x - scroll[0] - 4, node_y - scroll[1], 16, 16))
                # pygame.draw.rect(surface, (150, 25, 150), (node[0] - scroll[0], node[1] - scroll[1], 32, 32), 4)
        for node in self.node_positions.items():
            node_id, node_pos = node
            node_x, node_y = node_pos[0], node_pos[1]
            for node_in_path in self.path:
                if node_id == node_in_path:
                    pygame.draw.rect(surface, (255, 255, 100), (node_x - scroll[0] - 4, node_y - scroll[1], 16, 16))
            if node_id == self.goal:
                pygame.draw.rect(surface, (255, 255, 255), (node_x - scroll[0] - 4, node_y - scroll[1], 16, 16))

    def final_nodes(self):
        return self.nodes

    def place_nodes(self, tiles):
        x = 0
        for tile in tiles:
            x += 1
            self.nodes.append([tile[0], tile[1] - 35, x])

    def make_graph(self, surface, scroll, debug):
        self.graph = {}
        self.node_positions = {}
        for node in self.nodes:
            node_id = node[2]
            node_pos = [node[0], node[1]]
            self.graph[node_id] = []
            self.node_positions[node_id] = [node_pos[0], node_pos[1]]
        for node in self.node_positions.items():
            neighbors = []
            node_id, node_pos = node
            node_x, node_y = node_pos[0], node_pos[1]
            for some_node in self.node_positions.items():
                some_node_id, some_node_pos = some_node
                some_node_x_dis = node_pos[0] - some_node_pos[0]
                some_node_y_dis = node_pos[1] - some_node_pos[1]
                if some_node_x_dis >= -160 and some_node_x_dis <= 160 and some_node_y_dis >= -160 and some_node_y_dis <= 160:
                    neighbors.append(some_node_id)
                    self.graph[node_id] = neighbors
                    if debug:
                        pygame.draw.line(surface, (175, 0,0 ), (node_pos[0] - scroll[0], node_pos[1] - scroll[1]), (some_node_pos[0] - scroll[0], some_node_pos[1] - scroll[1]))


    def find_path(self, start, end):
        self.visited = {}
        self.level = {}
        self.parent = {}
        self.bfsto = []
        self.path = []
        self.goal = end
        self.queue = Queue()
        for node in self.graph.keys():
            self.visited[node] = False
            self.parent[node] = None
            self.level[node] = -1
        self.start = start
        self.visited[start] = True
        self.level[start] = 0
        self.queue.put(start)
        try:
            while not self.queue.empty():
                u = self.queue.get()
                self.bfsto.append(u)

                for v in self.graph[u]:
                    if self.visited[v] != 1:
                        self.visited[v] = True
                        self.parent[v] = u
                        self.level[v] = self.level[u] + 1
                        self.queue.put(v)

            while end is not None:
                self.path.append(end)
                end = self.parent[end]
            self.path.reverse()
        except KeyError:
            pass

    def clear_nodes(self):
        self.nodes.clear()
