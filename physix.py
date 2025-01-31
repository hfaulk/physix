from lib.graphix import GraphixObject, Window, Point, Rectangle, Circle
from lib.graphix_plus import full_fill
from numpy import add as npadd

class PhysixEnvironment:
    def __init__(self, local_g:(float,float), top_left:Point, bottom_right:Point):
        self._env_space = None
        self._g:float = local_g
        self._top_left:Point = top_left
        self._bottom_right:Point = bottom_right
        self._objects:list = []

    def __repr__(self):
        return f"PhysixEnvironment({self._top_left}, {self._bottom_right})"

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if value > 0: self._g = value

    def dimensions(self):
        return self._top_left, self._bottom_right

    def add(self, physix_object):
        if issubclass(type(physix_object), GraphixObject):
            self._objects.append(physix_object)

    def draw(self, window: Window):
        self._env_space = Rectangle(self._top_left, self._bottom_right)
        full_fill(self._env_space, window.background_colour, "black")
        self._env_space.draw(window)

    def simulate(self):
        ...

class PhysixObject:
    def __init__(self, window:Window, environment:PhysixEnvironment, mass:float, radius:int):
        if type(environment) != PhysixEnvironment:
            raise Exception(f"Environment must be a PhysixEnvironment, not {environment}")
        if radius > (environment.dimensions()[1].x - environment.dimensions()[0].x) or \
           radius > (environment.dimensions()[1].y - environment.dimensions()[0].y):
            raise Exception(f"PhysixObject is too big for given PhysixEnvironment")
        self._physix_object = None
        self._position = None
        self._window = window
        self._environment = environment
        self._mass = mass
        self._radius = radius
        self._velocity = (0,0)

    def __repr__(self):
        return f"PhysixObject({self._environment, self._mass})"

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        if value > 0: self._mass = value

    def place(self, center:(int,int)):
        top_left = self._environment.dimensions()[0]
        bottom_right = self._environment.dimensions()[1]

        if top_left.x + center[0] + self._radius < bottom_right.x and \
           top_left.y + center[1] + self._radius < bottom_right.y:
            self._position = Point(top_left.x + center[0], top_left.y + center[1])
        else:
            raise Exception(f"Object exceeds PhysixEnvironment area")

        self._physix_object = Circle(self._position, self._radius)
        full_fill(self._physix_object, "red")
        self._physix_object.draw(self._window)
        self._environment.add(self._physix_object)

    def push(self, force:(float,float)):
        h_accel = force[0] // self._mass
        v_accel = force[1] // self._mass

        self._velocity = (int(self._velocity[0] + h_accel), int(self._velocity[1] + v_accel))

        self._physix_object.move(*self._velocity)

        self._position = Point(self._physix_object.get_centre().x, self._physix_object.get_centre().y)

    def update(self):
        ...

class ResistanceObject:
    def __init__(self):
        ...

if __name__ == "__main__":
    win = Window("Physicsing", 800, 600)

    env = PhysixEnvironment((0, 9.81), Point(10, 10), Point(790, 590))
    env.draw(win)

    obj = PhysixObject(win, env, 2, 100)
    obj.place((200, 150))

    while True:
        win.get_mouse()
        obj.push(env.g)