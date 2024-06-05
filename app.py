import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class City:
    def __init__(self, name, point):
        self.name = name
        self.point = point

class Node:
    def __init__(self, boundary):
        self.boundary = boundary  # boundary is a tuple (x_min, y_min, x_max, y_max)
        self.cities = []
        self.NW = None  # Northwest quadrant
        self.NE = None  # Northeast quadrant
        self.SW = None  # Southwest quadrant
        self.SE = None  # Southeast quadrant

class Quadtree:
    def __init__(self, boundary, capacity=1):
        self.root = Node(boundary)
        self.capacity = capacity
        self.found_city = None  # Store the found city for visualization

    def insert(self, city):
        return self._insert(self.root, city)

    def _insert(self, node, city):
        if not self._in_boundary(node.boundary, city.point):
            return False

        if len(node.cities) < self.capacity and node.NW is None:
            node.cities.append(city)
            return True

        if node.NW is None:
            self._subdivide(node)

        if self._insert(node.NW, city): return True
        if self._insert(node.NE, city): return True
        if self._insert(node.SW, city): return True
        if self._insert(node.SE, city): return True

        return False

    def _subdivide(self, node):
        x_min, y_min, x_max, y_max = node.boundary
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2

        node.NW = Node((x_min, y_mid, x_mid, y_max))
        node.NE = Node((x_mid, y_mid, x_max, y_max))
        node.SW = Node((x_min, y_min, x_mid, y_mid))
        node.SE = Node((x_mid, y_min, x_max, y_mid))

        while node.cities:
            existing_city = node.cities.pop()
            self._insert(node, existing_city)

    def _in_boundary(self, boundary, point):
        x_min, y_min, x_max, y_max = boundary
        return x_min <= point.x < x_max and y_min <= point.y < y_max

    def find(self, point):
        self.found_city = None  # Reset the found city
        return self._find(self.root, point)

    def _find(self, node, point):
        if not self._in_boundary(node.boundary, point):
            return None

        for city in node.cities:
            if city.point.x == point.x and city.point.y == point.y:
                self.found_city = city  # Store the found city
                return city

        if node.NW is None:
            return None

        if self._in_boundary(node.NW.boundary, point):
            return self._find(node.NW, point)
        elif self._in_boundary(node.NE.boundary, point):
            return self._find(node.NE, point)
        elif self._in_boundary(node.SW.boundary, point):
            return self._find(node.SW, point)
        elif self._in_boundary(node.SE.boundary, point):
            return self._find(node.SE, point)

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
        rect = Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=None, edgecolor='black')
        ax.add_patch(rect)
        
        for city in node.cities:
            color = 'ro'
            if self.found_city and city.name == self.found_city.name:
                color = 'go'
            ax.plot(city.point.x, city.point.y, color)
            ax.text(city.point.x, city.point.y, f' {city.name}', verticalalignment='bottom', horizontalalignment='right')
        
        if node.NW is not None:
            self._draw_node(node.NW, ax)
            self._draw_node(node.NE, ax)
            self._draw_node(node.SW, ax)
            self._draw_node(node.SE, ax)

def main():
    boundary = (0, 0, 100, 100)  # Define the boundary of the quadtree
    quadtree = Quadtree(boundary)

    num_cities = int(input("Enter the number of cities: "))

    for _ in range(num_cities):
        name = input("Enter the name of the city: ")
        x = float(input(f"Enter the x coordinate of {name}: "))
        y = float(input(f"Enter the y coordinate of {name}: "))
        quadtree.insert(City(name, Point(x, y)))

    while True:
        x = float(input("Enter the x coordinate of the city to find: "))
        y = float(input("Enter the y coordinate of the city to find: "))
        found_city = quadtree.find(Point(x, y))
        if found_city:
            print(f"Found city: {found_city.name}")
        else:
            print("City not found")

        cont = input("Do you want to search for another city? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
    
    quadtree.draw()

if __name__ == "__main__":
    main()
