import pygame
import math

COLORS = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255)
}


class Painter:
    def __init__(self, width, height, a, b, function):
        self.width = width
        self.height = height
        self.a = a
        self.b = b
        self.func = function

        self._display = pygame.display.set_mode((width, height))
        self._timer = pygame.time.Clock()
        self.is_running = True

        pygame.init()

    def start(self):
        while self.is_running:
            for e in pygame.event.get():
                self.is_running = not e.type == pygame.QUIT
            self._display.fill(COLORS['white'])
            self.draw_func()

            pygame.display.update()
            self._timer.tick(1000)

    def draw_func(self):
        max_x, max_y = self.width, self.height
        y_min = y_max = self.func(self.a)

        for xx in range(1, max_x - 1):
            x = self.a + xx * (self.b - self.a) / max_x
            y = self.func(x)

            y_min = y if y < y_min else y_min
            y_max = y if y > y_max else y_max
        if self.a * self.b <= 0:
            mid_x = - self.a * max_x / (self.b - self.a)
            self.draw_vertical_axis(mid_x)
        if y_min * y_max <= 0:
            mid_y = - y_min * max_y / (y_max - y_min)
            self.draw_horizontal_axis(max_y - mid_y)

        last_y = self.calculate_y(self.func(self.a), y_min, y_max, max_y)
        for xx in range(1, max_x - 1):
            x = self.a + xx * (self.b - self.a) / max_x
            y = self.calculate_y(self.func(x), y_min, y_max, max_y)
            self.draw_line((xx - 1, last_y), (xx, y), COLORS['black'])
            last_y = y

    def draw_horizontal_axis(self, mid_y):
        self.draw_line((0, mid_y), (self.width, mid_y), COLORS['red'])

    def draw_vertical_axis(self, mid_x):
        self.draw_line((mid_x, 0), (mid_x, self.height), COLORS['red'])

    def draw_line(self, point_1, point_2, color):
        pygame.draw.line(self._display, color, point_1, point_2)

    def calculate_y(self, y, min_y, max_y, y_max):
        return int((y - max_y) * y_max / (min_y - max_y))


if __name__ == '__main__':
    FUNCTIONS = {
        'sinx': lambda x: math.sin(x),
        'tmp': lambda x: x**3,
        'xsinx': lambda x: x * math.sin(x*x),
        'exp': lambda x: math.e ** x
    }

    painter = Painter(800, 800, -1, 5, FUNCTIONS['xsinx'])
    # painter = Painter(600, 600, -5, 7, FUNCTIONS['exp'])
    painter.start()
