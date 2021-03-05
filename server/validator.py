import math

class Warehouse:
    def __init__(self, coords, products):
        self.coords = coords
        self.products = products

class Order:
    def __init__(self, coords, products):
        self.coords = coords
        self.products = products

class Drone:
    def __init__(self, coords):
        self.coords = coords
        self.instructions = []
        self.load = []
        self.delay = 0
        self.active = None

class Validator:

    def __init__(self):
        self.rows = None
        self.cols = None
        self.D = None
        self.deadline = None
        self.maxweight = None
        self.P = None
        self.weights = None
        self.W = None
        self.warehouses = []
        self.C = None
        self.orders = []
        self.Q = None
        self.drones = []
        self.score = 0

    def verify(self, in_lines, out_lines):
        self.rows, self.cols, self.D, self.deadline, self.maxweight = list(map(int, in_lines[0].split()))

        self.P = int(in_lines[1])
        self.weights = list(map(int, in_lines[2].split()))
        self.W = int(in_lines[3])

        for i in range(4, 2*self.W + 4, 2):
            coords = (int(in_lines[i].split()[0]), int(in_lines[i].split()[1]))
            products = list(map(int, in_lines[i + 1].split()))
            self.warehouses += [Warehouse(coords, products)]

        self.C = int(in_lines[4 + 2*self.W])

        for i in range(4 + 2*self.W + 1, 2*self.W + 3*self.C + 5, 3):
            coords = (int(in_lines[i].split()[0]), int(in_lines[i].split()[1]))
            products = list(map(int, in_lines[i + 2].split()))
            self.orders += [Order(coords, products)]

        self.Q = int(out_lines[0])

        for i in range(self.D):
            self.drones += [Drone(self.warehouses[0].coords)]

        for i in range(1, self.Q + 1):
            instruction = out_lines[i].split()
            self.drones[int(instruction[0])].instructions += [instruction[1:]]

        for t in range(self.deadline):
            for d in self.drones:
                if d.active and d.active[0] == 'U' and d.delay == 0:
                    self.exec(d, d.active, t)

            for d in self.drones:
                if d.delay == 0:
                    if d.active and d.active[0] != 'U':
                        self.exec(d, d.active, t)
                    if d.instructions:
                        d.active = d.instructions[0]
                        d.instructions = d.instructions[1:]
                        if d.active[0] == 'W':
                            d.delay = int(d.active[1])
                        elif d.active[0] == 'D':
                            d.delay = self.dist(d.coords, self.orders[int(d.active[1])].coords) + 1
                        else:
                            d.delay = self.dist(d.coords, self.warehouses[int(d.active[1])].coords) + 1
                d.delay -= 1

        return self.score

    def exec(self, d, instruction, t):
        if instruction[0] == 'L':
            whs, pdt, qty = list(map(int, instruction[1:]))
            if self.warehouses[whs].products[pdt] < qty:
                raise Exception(f'Drone {self.drones.index(d)} is unable to load quantity {qty} of product {pdt} from warehouse {whs} at time {t}. Product unavailable')

            d.load += qty*[pdt]
            self.warehouses[whs].products[pdt] -= qty

            weight = sum(map(lambda product: self.weights[product], d.load))

            if weight > self.maxweight:
                raise Exception(f'Drone {self.drones.index(d)} is unable to load quantity {qty} of product {pdt} from warehouse {whs} at time {t}. Drone is overweight.')
        elif instruction[0] == 'U':
            whs, pdt, qty = list(map(int, instruction[1:]))
            if d.load.count(pdt) < qty:
                raise Exception(f'Drone {self.drones.index(d)} is unable to unload quantity {qty} of product {pdt} into warehouse {whs} at time {t}. Drone does not carry enough of this product.')

            for i in range(qty):
                d.load.remove(pdt)
            self.warehouses[whs].products[pdt] += qty
        elif instruction[0] == 'D':
            cli, pdt, qty = list(map(int, instruction[1:]))
            if d.load.count(pdt) < qty:
                raise Exception(
                    f'Drone {self.drones.index(d)} is unable to deliver quantity {qty} of product {pdt} to client {cli} at time {t}. Drone does not carry enough of this product.')

            if self.orders[cli].products.count(pdt) < qty:
                raise Exception(
                    f'Drone {self.drones.index(d)} is unable to deliver quantity {qty} of product {pdt} to client {cli} at time {t}. Client does not want so much of this product.')

            for i in range(qty):
                d.load.remove(pdt)
                self.orders[cli].products.remove(pdt)

            if not self.orders[cli].products:
                self.add_score(t)

    def dist(self, origin, dest):
        return math.ceil(math.sqrt((origin[0]-dest[0])**2 + (origin[1]-dest[1])**2))

    def add_score(self, t):
        self.score += math.ceil(((self.deadline - t) / self.deadline) * 100)

if __name__ == "__main__":
    v = Validator()
    f = open("busy_day.in", "r")
    in_lines = list(map(lambda line: line.replace('\n', ''), f.readlines()))
    f.close()

    f = open("out.out", "r")
    out_lines = list(map(lambda line: line.replace('\n', ''), f.readlines()))
    f.close()

    v.verify(in_lines, out_lines)
