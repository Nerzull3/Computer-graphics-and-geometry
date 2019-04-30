import pygame
from math import sin, cos, sqrt


COLORS = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}

x1 = -5
x2 = 2
y1 = -3
y2 = 4

class Painter:
    def __init__(self, resolution, f, debug):
        self.width, self.height = resolution
        self.f = f

        self._display = pygame.display.set_mode(resolution)
        self._timer = pygame.time.Clock()
        self.is_running = True
        self._debug = debug
        self._display.fill(COLORS['white'])

        self.n, self.m = (50, int(self.width * 2))
        self.min_x, self.max_x = (-10, 10)
        self.min_y, self.max_y = self.min_x, self.max_x

        self.draw_3D_graphic()

        pygame.init()

    def start(self):
        while self.is_running:
            self.handle_events()
            pygame.display.update()
            self._timer.tick(1000)

    def draw_3D_graphic(self):
        self.set_minmax()
        self.draw_lines_by_direction(x1, x2, y1, y2, True)
        self.draw_lines_by_direction(x1, x2, y1, y2, False)

    def set_minmax(self):
        for i in range(self.n):
            x = x2 + i * (x1 - x2) / self.n
            for j in range(self.m):
                y = y2 + j * (y1 - y2) / self.m
                try:
                    z = self.f(x, y)
                except:
                    pass
                xx, yy = self.lead_to_izometric_projection(x, y, z)

                self.max_x, self.min_x = max(self.max_x, xx), min(self.min_x, xx)
                self.max_y, self.min_y = max(self.max_y, yy), min(self.min_y, yy)

    def draw_lines_by_direction(self, x1, x2, y1, y2, is_along):
        top = []
        bottom = []
        for i in range(self.width):
            top.append(self.height)
            bottom.append(0)

        for i in range(self.n):
            if is_along:
                x = x2 + i * (x1 - x2) / self.n
            else:
                y = y2 + i * (y1 - y2) / self.n
            for j in range(self.m):
                if is_along:
                    y = y2 + j * (y1 - y2) / self.m
                else:
                    x = x2 + j * (x1 - x2) / self.m
                try:
                    z = self.f(x, y)
                except:
                    pass
                xx, yy = self.lead_to_izometric_projection(x, y, z)
                xx = round((xx - self.min_x) / (self.max_x - self.min_x) * self.width)
                yy = round((yy - self.min_y) / (self.max_y - self.min_y) * self.height)
                if yy > bottom[xx]:
                    self.draw_point((xx, yy), COLORS['red'])
                    bottom[xx] = yy
                if yy < top[xx]:
                    self.draw_point((xx, yy), COLORS['blue'])
                    top[xx] = yy

    def lead_to_izometric_projection(self, x, y, z):
        return (y - x) * sqrt(3) / 2, (x + y) / 2 - z

    def draw_point(self, point, color):
        pygame.draw.line(self._display, color, point, point)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_running = False


funcs = {
    1: lambda x, y: x + y,
    2: lambda x, y: 1,
    3: lambda x, y: sqrt(x**2 + y**2) + 3 * cos(sqrt(x**2 + y**2)) + 5,
    4: lambda x, y: 2 * x**2 * y**2,
    5: lambda x, y: 100 - 3 / sqrt(x**2 + y**2) + sin(sqrt(x**2 + y**2)) + sqrt(200 - x**2 + y**2 + 10 * sin(x) + 10 * sin(y)) / 1000
}
    
if __name__ == "__main__":
    painter = Painter((600, 800), funcs[4], debug=True)
    painter.start()
