import math
import random

class Grid:
    """
    """
    def __init__(self, width, height=None):
        """
        """
        if height == None:
            height = width
        self.dimension = (width, height)
        self.create_nodes()
        self.create_edges()

    def create_nodes(self):
        """
        """
        width, height = self.dimension
        self.nodes = {}

        count = 1
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                self.nodes[(i, j)] = (count, "(%d,%d)" % (i, j))
                count += 1

    def create_edges(self):
        """
        """
        width, height = self.dimension
        self.edges = []

        for (i, j) in self.nodes:
            delta = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
            for (a, b) in delta:
                if (a, b) in self.nodes:
                    x, xi = self.nodes[(i, j)]
                    y, yi = self.nodes[(a, b)]
                    self.edges.append((x, y, "%s>%s" % (xi, yi)))

    def to_tgf(self):
        """
        """
        content = []
        obstacles = []
        for (i, j) in self.nodes:
            content.append("%d %s" % self.nodes[(i, j)])
            if self.nodes[(i, j)][1].endswith(" (Obstacle)"):
                obstacles.append(self.nodes[(i, j)][0])
        content.append('#')
        for (i, j, info) in self.edges:
            if i in obstacles or j in obstacles:
                continue
            content.append("%d %d %s" % (i, j, info))
        return '\n'.join(content)

    def add_random_obstacles(self, num_obstacles):
        """
        """
        width, height = self.dimension
        for _ in range(num_obstacles):
            i = random.randint(1, width)
            j = random.randint(1, height)
            node = self.nodes[(i, j)][0]
            self.nodes[(i, j)] = (node, "(%d,%d)" % (i, j) + " (Obstacle)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        w, h, num_obstacles = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        g = Grid(w, h)
        g.add_random_obstacles(num_obstacles)
        print(g.to_tgf())
