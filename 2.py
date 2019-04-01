import pygame

COLORS = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255)
}


class Painter:
    def __init__(self, resolution, a, b, func_obj):
        self.width, self.height = resolution
        print(self.width, self.height)
        self.a = a
        self.b = b
        self.f = func_obj.f
        self.func_obj = func_obj

        self._display = pygame.display.set_mode(resolution)
        self._timer = pygame.time.Clock()
        self.is_running = True

        pygame.init()
        self._display.fill(COLORS['white'])

        self.set_min_max()
        self.draw_axis()
        self.draw_asymptotes()
        print(self.get_intersection_point())
        self.draw_bisectrix()
        self.start()

    def start(self):
        while self.is_running:
            self.handle_events()
            
            self.draw_func()

            pygame.display.update()
            self._timer.tick(1000)

    def draw_func(self):
        pass
        # self.set_min_max()
        # self.draw_axis()
        # self.draw_asymptotes()
        # print(self.get_intersection_point())


    def draw_axis(self):
        origin = self.to_screen((0, 0))
        self.draw_line((0, origin[1]), (self.width, origin[1]))
        self.draw_line((origin[0], 0), (origin[0], self.height))
        self.draw_noches()
    
    def draw_noches(self):
        step = max(1, round(self.to_coords((32, 0))[0] - self.to_coords((0, 0))[0]))
        for x in range(step, max(abs(self.a), abs(self.b)), step):
            xx_right, yy = self.to_screen((x, 0))
            xx_left, yy = self.to_screen((-x, 0))
            self.draw_line((xx_right, yy - 2), (xx_right, yy + 2))
            self.draw_line((xx_left, yy - 2), (xx_left, yy + 2))
        
        step = max(1, round(self.to_coords((0, 0))[1] - self.to_coords((0, 32))[1]))
        for y in range(step, max(abs(round(self.ymin)), abs(round(self.ymax))), step):
            xx, yy_up = self.to_screen((0, y))
            xx, yy_down = self.to_screen((0, -y))
            self.draw_line((xx - 2, yy_up), (xx + 2, yy_up))
            self.draw_line((xx - 2, yy_down), (xx + 2, yy_down))

    def draw_asymptotes(self):
        if self.func_obj.c != 0:
            self.draw_line(
                self.to_screen((self.func_obj.vertical_asymp(), -self.height)),
                self.to_screen((self.func_obj.vertical_asymp(), self.height)),
                COLORS['blue']
            )

        self.draw_line(
            self.to_screen((self.a, self.func_obj.oblique_asymp(self.a))),
            self.to_screen((self.b, self.func_obj.oblique_asymp(self.b))),
            COLORS['blue']
        )

    def draw_line(self, point_1, point_2, color=COLORS['black']):
        pygame.draw.line(self._display, color, point_1, point_2)

    def to_screen(self, point):
        x, y = point
        return (
            round((x - self.a) * self.width / (self.b - self.a)),
            round((y - self.ymax) * self.height / (self.ymin - self.ymax))
        )

    def to_coords(self, point):
        x, y = point
        return (
            x * (self.b - self.a) / self.width + self.a,
            y * (self.ymin - self.ymax) / self.height + self.ymax
        )
    
    def set_min_max(self):
        self.ymin = self.ymax = self.a
        for xx in range(self.width):
            x = xx * (self.b - self.a) / self.width + self.a
            if x == -self.func_obj.d:
                continue
            y = self.f(x)
            self.ymin = min(self.ymin, y)
            self.ymax = max(self.ymax, y)

    def get_intersection_point(self):
        coefs = self.func_obj
        return (
            -coefs.d,
            -coefs.a * coefs.d + coefs.b,
        )

    def draw_bisectrix(self):
        self.draw_line(
            self.to_screen((self.a, self.func_obj.get_bisectrix(self.a, 1))), 
            self.to_screen((self.b, self.func_obj.get_bisectrix(self.b, 1))), 
            color=COLORS['green']
        )

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_running = False


class Function:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def f(self, x):
        return self.a * x + self.b + self.c / (x + self.d)

    def oblique_asymp(self, x):
        return self.a * x + self.b

    def vertical_asymp(self):
        return -self.d

    def get_bisectrix(self, x, sign):
        return sign * ((x + self.d) * (self.a**2 + 1)**0.5 + (self.a * x + self.b))

    @staticmethod
    def invert(value):
        return -value


# in future
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return self._x == other.x() and self._y == other.y()

    def __str__(self):
        return f'({self._x}, {self._y})'


if __name__ == '__main__':
    func_obj = Function(1, 2, 3, 4)
    painter = Painter((600, 600), -20, 20, func_obj)

# 1. нарисовать ассимптоты: y=ax+b и x=-d
# 2. найти точку пересечения ассимптот (1)
# 3. построить биссектрису через т.п.1
# 4. найти точку пересечения графика функции с биссектрисой (2)
# 5. расстояние от т.п.1 до т.п.2 равно t
# 6. найти дельту (расст. между т.п.2 и фокусом)
# 7. => построить фокусы
# 8. начать строить 4 части графика по алгоритму
# 9. profit.
# 10.
