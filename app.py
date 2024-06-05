import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class City:
    def __init__(self, name, point):
        self.name, self.point = name, point

class Node:
    def __init__(self, boundary):
        self.boundary = boundary
        self.cities = []
        self.NW = self.NE = self.SW = self.SE = None

class Quadtree:
    def __init__(self, boundary, capacity=1):
        self.root = Node(boundary)
        self.capacity = capacity
        self.found_city = None

    def insert(self, city):
        self._insert(self.root, city)

    def _insert(self, node, city):
        if not self._in_boundary(node.boundary, city.point):
            return
        if len(node.cities) < self.capacity and not node.NW:
            node.cities.append(city)
        else:
            if not node.NW: self._subdivide(node)
            for child in [node.NW, node.NE, node.SW, node.SE]:
                self._insert(child, city)

    def _subdivide(self, node):
        x_min, y_min, x_max, y_max = node.boundary
        x_mid, y_mid = (x_min + x_max) / 2, (y_min + y_max) / 2
        node.NW, node.NE = Node((x_min, y_mid, x_mid, y_max)), Node((x_mid, y_mid, x_max, y_max))
        node.SW, node.SE = Node((x_min, y_min, x_mid, y_mid)), Node((x_mid, y_min, x_max, y_mid))
        for city in node.cities:
            self._insert(node, city)
        node.cities.clear()

    def _in_boundary(self, boundary, point):
        x_min, y_min, x_max, y_max = boundary
        return x_min <= point.x < x_max and y_min <= point.y < y_max

    def find(self, point):
        self.found_city = None
        return self._find(self.root, point)

    def _find(self, node, point):
        if not self._in_boundary(node.boundary, point):
            return None
        for city in node.cities:
            if city.point.x == point.x and city.point.y == point.y:
                self.found_city = city
                return city
        if node.NW:
            for child in [node.NW, node.NE, node.SW, node.SE]:
                if self._in_boundary(child.boundary, point):
                    return self._find(child, point)
        return None

    def draw(self):
        fig, ax = plt.subplots()
        self._draw_node(self.root, ax)
        plt.gca().invert_yaxis()
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Quadtree Visualization')
        plt.show()

    def _draw_node(self, node, ax):
        x_min, y_min, x_max, y_max = node.boundary
        ax.add_patch(Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=None, edgecolor='black'))
        for city in node.cities:
            ax.plot(city.point.x, city.point.y, 'go' if self.found_city and city.name == self.found_city.name else 'ro')
            ax.text(city.point.x, city.point.y, f' {city.name}', verticalalignment='bottom', horizontalalignment='right')
        if node.NW:
            for child in [node.NW, node.NE, node.SW, node.SE]:
                self._draw_node(child, ax)

def main():
    quadtree = Quadtree((0, 0, 100, 100))
    for _ in range(int(input("Number of cities: "))):
        name, x, y = input("City name, x, y: ").split(',')
        quadtree.insert(City(name.strip(), Point(float(x), float(y))))
    while input("Find city? (yes/no): ").strip().lower() == 'yes':
        coordinates = input("Enter x, y: ").replace(',', ' ').split()
        x, y = map(float, coordinates)
        found_city = quadtree.find(Point(x, y))
        print(f"Found city: {found_city.name}" if found_city else "City not found")
    quadtree.draw()

if __name__ == "__main__":
    main()
