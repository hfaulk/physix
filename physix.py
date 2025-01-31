from lib.graphix import Window, Point, Rectangle
from lib.graphix_plus import full_fill

class PhysixEnvironment:
    def __init__(self, local_g:float, top_left:Point, bottom_right:Point):
        self._env_space = None
        self._g:float = local_g
        self._top_left:Point = top_left
        self._bottom_right:Point = bottom_right
        self.objects:dict = {}

    def __repr__(self):
        return f"PhysixEnvironment({self._top_left}, {self._bottom_right})"

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if value > 0:
            self._g = value

    def zero(self):
        return self._top_left

    def draw(self, window: Window):
        self._env_space = Rectangle(self._top_left, self._bottom_right)
        full_fill(self._env_space, window.background_colour, "black")
        self._env_space.draw(window)

class PhysixObject:
    def __init__(self, mass):
        ...

class ResistanceObject:
    def __init__(self):
        ...

if __name__ == "__main__":
    win = Window("Physicsing", 800, 600)

    env = PhysixEnvironment(9.81, Point(10, 10), Point(200, 200))
    env.draw(win)

    print(env.g)

    while True:
        win.get_mouse()