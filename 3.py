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
    def __init__(self, resolution, polygon_1, polygon_2, debug=False):
        self.width, self.height = resolution
        self.polygon_1 = polygon_1
        self.polygon_2 = polygon_2
        self.intersection_vertices = []

        self._display = pygame.display.set_mode(resolution)
        self._timer = pygame.time.Clock()
        self.is_running = True
        self._debug = debug

        pygame.init()
        self._display.fill(COLORS['white'])
        
        self.draw_polygon(self.polygon_1)
        self.draw_polygon(self.polygon_2, color=COLORS['green'])
        self.draw_union_polygon()

    def start(self):
        while self.is_running:
            self.handle_events()
            pygame.display.update()
            self._timer.tick(1000)

    def draw_union_polygon(self):
        self.find_intersection_vertices()

        """ вывод координат на экран """
        self.print_all_vertices()

        if self._debug:
            print(f'лист точек пересечений без повторов: {list(set(self.intersection_vertices))}')
            print(f'первый полигон: {self.polygon_1}')
            print(f'второй полигон: {self.polygon_2}')

        if not self.intersection_vertices:
            if self.is_inside_polygon(self.polygon_1[0], self.polygon_2):
                self.draw_polygon(self.polygon_2, color=COLORS['blue'])
            elif self.is_inside_polygon(self.polygon_2[0], self.polygon_1):
                self.draw_polygon(self.polygon_1, color=COLORS['blue'])
            else:
                self.draw_polygon(self.polygon_1, color=COLORS['blue'])
                self.draw_polygon(self.polygon_2, color=COLORS['blue'])
            return

        union_polygon = []
        start_index = self.find_start(self.polygon_1, self.polygon_2)
        if start_index is not None:
            self.polygon_1 = self.rebuild_polygon(self.polygon_1, start_index)
            index = self.polygon_2.index(self.intersection_vertices[0])
            self.polygon_2 = self.rebuild_polygon(self.polygon_2, index)
            union_polygon = self.build_polygon(self.polygon_1, self.polygon_2)
        else:
            start_index = self.find_start(self.polygon_2, self.polygon_1)
            if start_index is not None:
                self.polygon_2 = self.rebuild_polygon(self.polygon_2, start_index)
                index = self.polygon_1.index(self.intersection_vertices[0])
                self.polygon_1 = self.rebuild_polygon(self.polygon_1, index)
                union_polygon = self.build_polygon(self.polygon_2, self.polygon_1)
            else:
                raise TypeError('Error! Start is not exist.')

        if self._debug:
            print(f'Объединение: {union_polygon}')

        self.draw_polygon(union_polygon, color=COLORS['blue'])

    def is_inside_polygon(self, point, polygon):
        x, y = point
        flag = False
        prev_x, prev_y = polygon[-1]
        for p_point in polygon:
            xp, yp = p_point
            if ((yp <= y < prev_y) or (prev_y <= y < yp)) and x > (prev_x - xp) * (y - yp) / (prev_y - yp) + xp:
                flag = not flag
            prev_x, prev_y = xp, yp
        return flag

    def find_intersection_vertices(self):
        temp_1, temp_2 = [], []
        """ заполняем первый полигон """
        for i in range(len(self.polygon_1)):
            temp = []
            for j in range(len(self.polygon_2)):
                intersection_point = self.get_line_intersection(
                    self.polygon_1[i - 1],
                    self.polygon_1[i],
                    self.polygon_2[j - 1],
                    self.polygon_2[j]
                )

                if self._debug:
                    print(f'(i={i}, j={j}): {intersection_point}')
                    print(f'для {(self.polygon_1[i - 1], self.polygon_1[i])}\nи {(self.polygon_2[j - 1], self.polygon_2[j])}\n')

                if intersection_point:
                    if intersection_point not in self.polygon_1:
                        temp.append((i, intersection_point, self.get_square_of_distance(self.polygon_1[i - 1], intersection_point)))
                    self.intersection_vertices.append(intersection_point)
            temp = sorted(temp, key=lambda p: p[2])
            for point in temp:
                temp_1.append((point[0], point[1]))

        """ заполняем второй полигон """
        for i in range(len(self.polygon_2)):
            temp = []
            for j in range(len(self.polygon_1)):
                intersection_point = self.get_line_intersection(
                    self.polygon_1[j - 1],
                    self.polygon_1[j],
                    self.polygon_2[i - 1],
                    self.polygon_2[i]
                )

                if self._debug:
                    print(f'(i={j}, j={i}): {intersection_point}')
                    print(f'для {(self.polygon_1[j - 1], self.polygon_1[j])}\nи {(self.polygon_1[j - 1], self.polygon_1[j])}\n')

                if intersection_point:
                    if intersection_point not in self.polygon_2:
                        temp.append((i, intersection_point, self.get_square_of_distance(self.polygon_2[i - 1], intersection_point)))
                    self.intersection_vertices.append(intersection_point)
            temp = sorted(temp, key=lambda p: p[2])
            for point in temp:
                temp_2.append((point[0], point[1]))

        temp_1.reverse()
        temp_2.reverse()

        for i, point in temp_1:
            self.polygon_1.insert(i, point)
        for i, point in temp_2:
            self.polygon_2.insert(i, point)

    def get_square_of_distance(self, point_1, point_2):
        x1, y1 = point_1
        x2, y2 = point_2
        return (x2 - x1)**2 + (y2 - y1) ** 2

    def get_line_intersection(self, p0, p1, p2, p3):
        s1 = (p1[0] - p0[0], p1[1] - p0[1])
        s2 = (p3[0] - p2[0], p3[1] - p2[1])

        try:
            s = (-s1[1] * (p0[0] - p2[0]) + s1[0] * (p0[1] - p2[1])) / (-s2[0] * s1[1] + s1[0] * s2[1])
            t = (s2[0] * (p0[1] - p2[1]) - s2[1] * (p0[0] - p2[0])) / (-s2[0] * s1[1] + s1[0] * s2[1])

            if 0 <= s <= 1 and 0 <= t <= 1:
                intersection = (int(p0[0] + (t * s1[0])), int(p0[1] + (t * s1[1])))
                return intersection
        except ZeroDivisionError:
            pass

    def find_start(self, polygon_1, polygon_2):
        for i in range(len(polygon_1)):
            if not self.is_inside_polygon(polygon_1[i], polygon_2) and polygon_1[i] not in self.intersection_vertices:
                return i
        
        return None

    def build_polygon(self, polygon_1, polygon_2):
        polygon_1 = self.remove_repeating_elements(polygon_1)
        polygon_2 = self.remove_repeating_elements(polygon_2)
        start = polygon_1[0]
        current = polygon_1[1]
        is_polygon_2 = False
        union_polygon = [start]
        while current != start:
            union_polygon.append(current)
            if is_polygon_2:
                next_p = self.get_next_point(polygon_2, current)
                if self.is_inside_polygon(self.get_middle_point(current, next_p), polygon_1):
                    is_polygon_2 = False
                    current = self.get_next_point(polygon_1, current)
                else:
                    current = next_p
            else:
                next_p = self.get_next_point(polygon_1, current)
                if self.is_inside_polygon(self.get_middle_point(current, next_p), polygon_2):
                    is_polygon_2 = True
                    current = self.get_next_point(polygon_2, current)
                else:
                    current = next_p

        return union_polygon

    def remove_repeating_elements(self, polygon):
        visited = set()
        result = []
        for point in polygon:
            if point not in visited:
                result.append(point)
                visited.add(point)
        return result

    def get_middle_point(self, point_1, point_2):
        x1, y1 = point_1
        x2, y2 = point_2
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def get_next_point(self, polygon, current):
        i = polygon.index(current)
        if i < len(polygon) - 1:
            return polygon[i + 1]
        return polygon[0]

    def rebuild_polygon(self, polygon, start_index):
        return polygon[start_index:] + polygon[:start_index]

    def print_all_vertices(self):
        points = list(set(self.intersection_vertices + self.polygon_1 + self.polygon_2))
        self.draw_coords(points)

    def draw_polygon(self, polygon, color=COLORS['red'], width=1):
        pygame.draw.polygon(self._display, color, polygon, width)

    def draw_coords(self, polygon):
        font = pygame.font.Font(None, 14)
        for p in polygon:
            text = font.render(f'({p[0]}, {p[1]})', True, COLORS['black'])
            self._display.blit(text, p)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_running = False


if __name__ == "__main__":
    """ Проверка на выпуклые полигоны """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 200), (200, 400)],
        polygon_2=[(100, 100), (400, 450), (300, 700)],
        debug=True
    )

    """ Проверка на невыпуклые полигоны + проверка на пересечение в вершине """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 200), (200, 400), (50, 350), (80, 250)],
        polygon_2=[(80, 250), (400, 450), (300, 700), (30, 300)],
        debug=True
    )

    """ Проверка на невыпуклые полигоны """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 200), (160, 400), (300, 250)],
        polygon_2=[(100, 100), (400, 450), (300, 700)],
        debug=True
    )

    """ Проверка на невыпуклые полигоны """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 200), (190, 400), (40, 250)],
        polygon_2=[(100, 100), (400, 450), (300, 700)],
        debug=True
    )

    """ Проверка на невыпуклые полигоны """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 50), (190, 400), (50, 250)],
        polygon_2=[(200, 50), (400, 450), (300, 700)],
        debug=True
    )

    """ Проверка на раздельные полигоны """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 200), (190, 400), (300, 250)],
        polygon_2=[(300, 600), (400, 700), (500, 700)]
    )

    """ Проверка на вложенный полигон """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (500, 200), (500, 600), (100, 450)],
        polygon_2=[(100, 100), (200, 200), (150, 300)]
    )

    """ экзотика (много случаев в одном графике) """
    painter = Painter(
        resolution=(600, 800),
        polygon_1=[(50, 50), (550, 50), (550, 600), (50, 600), (50, 500), (500, 500), (500, 100), (50, 100)],
        polygon_2=[(25, 25), (550, 550), (300, 550)],
        debug=True
    )

    painter.start()
