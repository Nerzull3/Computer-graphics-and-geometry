import pygame

COLORS = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'purple': (127, 0, 255)
}


class Painter:
    def __init__(self, resolution, a, b, func_obj):
        # размеры экрана
        self.width, self.height = resolution
        # минимум и максимум по х
        self.a = a
        self.b = b
        # вычислительная функция и объект Function
        self.f = func_obj.f
        self.func_obj = func_obj

        # минимум и максимум по у
        self.ymin = self.a
        self.ymax = self.b

        self._display = pygame.display.set_mode(resolution)
        self._timer = pygame.time.Clock()
        self.is_running = True

        pygame.init()
        self._display.fill(COLORS['white'])
        self.draw_func()

        self.start()

    def start(self):
        while self.is_running:
            self.handle_events()

            pygame.display.update()
            self._timer.tick(1000)

    def draw_func(self):
        # вспомогательные построения
        self.draw_axis()
        self.draw_asymptotes()
        self.draw_bisectrix()
        self.draw_point(self.func_obj.get_points_btwn_bis_and_func())
        self.draw_line(
            self.to_screen((-self.width, self.func_obj.get_parallel_line(-self.width))),
            self.to_screen((self.width, self.func_obj.get_parallel_line(self.width))),
            color=COLORS['green']
        )
        self.draw_point(self.func_obj.get_points_btwn_bis_and_func())
        self.draw_point([self.func_obj.get_intersection_point_btwn_asymp_and_dir()])
        self.draw_circle(
            self.func_obj.get_intersection_point_btwn_asymptotes(),
            Function.get_distance(
                self.to_screen(self.func_obj.get_intersection_point_btwn_asymptotes()),
                self.to_screen(self.func_obj.get_intersection_point_btwn_asymp_and_dir())
            )
        )
        self.draw_point(self.func_obj.get_intersection_point_btwn_bis_and_circle())
        # рисуется сам график
        self.draw_branches()

    def draw_axis(self):
        origin = self.to_screen((0, 0))
        self.draw_line((0, origin[1]), (self.width, origin[1]))
        self.draw_line((origin[0], 0), (origin[0], self.height))
        self.draw_noches()
    
    def draw_noches(self):
        for x in range(1, max(abs(self.a), abs(self.b))):
            xx_right, yy = self.to_screen((x, 0))
            xx_left, yy = self.to_screen((-x, 0))
            self.draw_line((xx_right, yy - 2), (xx_right, yy + 2))
            self.draw_line((xx_left, yy - 2), (xx_left, yy + 2))
        
        for y in range(1, max(abs(round(self.ymin)), abs(round(self.ymax)))):
            xx, yy_up = self.to_screen((0, y))
            xx, yy_down = self.to_screen((0, -y))
            self.draw_line((xx - 2, yy_up), (xx + 2, yy_up))
            self.draw_line((xx - 2, yy_down), (xx + 2, yy_down))

    def draw_branches(self):
        f_point1, f_point2 = self.func_obj.get_points_btwn_bis_and_func()

        best_points = []
        self.draw_branch(best_points, f_point2, 'down')  # down
        self.draw_branch(best_points, f_point2, 'left')  # left
        self.draw_branch(best_points, f_point1, 'up')  # up
        self.draw_branch(best_points, f_point1, 'right')  # right

        for point in best_points:
            self._display.set_at(point, COLORS['red'])

    def draw_branch(self, best_points, first_point, direction=''):
        best_points.append(self.to_screen(first_point))
        for _ in range(self.width):
            linked_area = filter(lambda p: p not in best_points, self.func_obj.get_8_linked_area(best_points[-1], direction))
            points = list(map(lambda p: (p, self.func_obj.get_error(self.to_coords(p))), linked_area))
            best_points.append(min(points, key=lambda p: p[1])[0])

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

    def draw_point(self, points):
        for point in points:
            self._display.set_at(self.to_screen(point), COLORS['red'])

    def draw_line(self, point_1, point_2, color=COLORS['black'], width=1):
        pygame.draw.line(self._display, color, point_1, point_2, width)

    def draw_circle(self, point, radius, color=COLORS['black']):
        pygame.draw.circle(self._display, color, self.to_screen(point), int(radius), 1)

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

    def draw_bisectrix(self):
        self.draw_line(
            self.to_screen((self.a, self.func_obj.get_bisectrix(self.a, 1))), 
            self.to_screen((self.b, self.func_obj.get_bisectrix(self.b, 1))), 
            color=COLORS['green']
        )
        self.draw_line(
            self.to_screen((self.a, self.func_obj.get_bisectrix(self.a, -1))), 
            self.to_screen((self.b, self.func_obj.get_bisectrix(self.b, -1))), 
            color=COLORS['purple']
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

        self.focus1 = None
        self.focus2 = None
        self.double_const = None

    def f(self, x):
        return self.a * x + self.b + self.c / (x + self.d)

    def oblique_asymp(self, x):
        return self.a * x + self.b

    def vertical_asymp(self):
        return -self.d
    
    def get_intersection_point_btwn_asymptotes(self):
        return (-self.d, -self.a * self.d + self.b)

    def get_bisectrix(self, x, sign):
        return sign * (x + self.d) * (self.a**2 + 1)**0.5 + (self.a * x + self.b)

    def get_parallel_line(self, x):
        x_1, y_1 = self.get_points_btwn_bis_and_func()[0]
        b = y_1 - (self.a - (self.a**2 + 1)**0.5) * x_1
        return (self.a - (self.a**2 + 1)**0.5) * x + b

    def get_points_btwn_bis_and_func(self):
        a, c, d = self.a, self.c, self.d
        x = (abs(c) / (a**2 + 1)**0.5)**0.5
        point_1 = (x - d, self.f(x - d))
        point_2 = (-x - d, self.f(-x - d))
        self.double_const = self.get_distance(point_1, point_2)
        return [point_1, point_2]

    def get_intersection_point_btwn_asymp_and_dir(self):
        return -self.d, self.get_parallel_line(-self.d)

    """ focuses """
    def get_intersection_point_btwn_bis_and_circle(self): 
        """ y = k * x + b """
        """ Ax + By + C = 0 """
        """ A = -k, B = 1, C = -b """
        """ n1=(-B/(A^2 + B^2)**0.5, A/(A^2 + B^2)**0.5) * r, n2=(B/(A^2 + B^2)**0.5, -A/(A^2 + B^2)**0.5) * r """
        k = self.a + (self.a**2 + 1)**0.5
        """ (x - x0)**2 + (y - y0)**2 = r**2 """
        x0, y0 = self.get_circle_center()
        r = self.get_circle_radius()
        self.focus1 = (-1 / (k**2 + 1)**0.5 * r + x0, (-k) / (k**2 + 1)**0.5 * r + y0)
        self.focus2 = (1 / (k**2 + 1)**0.5 * r + x0, k / (k**2 + 1)**0.5 * r + y0)

        return [self.focus1, self.focus2]

    def get_circle_center(self):
        return self.get_intersection_point_btwn_asymptotes()

    def get_circle_radius(self):
        return self.get_distance(
            self.get_circle_center(),
            self.get_intersection_point_btwn_asymp_and_dir()
        )

    def get_8_linked_area(self, point, direction=''):
        px, py = point
        if direction == 'up':
            return [(px + x, py + y) for x in range(-1, 2) for y in range(-1, 1) if (x, y) not in [(0, 0), (1, 0)]]
        if direction == 'right':
            return [(px + x, py + y) for x in range(0, 2) for y in range(-1, 2) if (x, y) != (0, 0)]
        if direction == 'down':
            return [(px + x, py + y) for x in range(-1, 2) for y in range(0, 2) if (x, y) not in [(0, 0), (-1, 0)]]
        if direction == 'left':
            return [(px + x, py + y) for x in range(-1, 1) for y in range(-1, 2) if (x, y) != (0, 0)]
        return []

    def get_error(self, point):
        return abs(abs(self.get_distance(point, self.focus1) - self.get_distance(point, self.focus2)) - self.double_const)

    @staticmethod
    def get_distance(point_1, point_2):
        x1, y1 = point_1
        x2, y2 = point_2
        return ((x1 - x2)**2 + (y1 -y2)**2)**0.5


# ограничение: c > 0!!!
if __name__ == '__main__':
    func_obj = Function(0, 0, 1, 0)
    painter = Painter((600, 600), -20, 20, func_obj)        
