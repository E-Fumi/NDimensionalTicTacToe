import pygame
import variables as v
import functions as f


class Button:
    def __init__(self, surface, position, variable_name, label):
        self.surface = surface
        self.position = position
        self.variable_name = variable_name
        if variable_name == 'v.game_dimensions':
            self.variable = v.game_dimensions
        if variable_name == 'v.pure_game':
            self.variable = v.pure_game
        if variable_name == 'v.multiple_win':
            self.variable = v.multiple_win
        if variable_name == 'v.algorithm':
            self.variable = v.algorithm
        if variable_name == 'v.player':
            self.variable = v.player
        self.label = label
        self.on_button = False
        self.size = 12
        self.width = 1
        self.colour = 0
        self.outer_points = [[position[0], position[1]],
                             [position[0] + self.size, position[1]],
                             [position[0] + self.size, position[1] + self.size],
                             [position[0], position[1] + self.size]]
        self.inner_points = [[position[0] + self.width, position[1] + self.width],
                             [position[0] + self.size - self.width, position[1] + self.width],
                             [position[0] + self.size - self.width, position[1] + self.size - self.width],
                             [position[0] + self.width, position[1] + self.size - self.width]]

    def hover_detect(self):
        if self.inner_points[0][0] < v.mouse_position[0] < self.inner_points[1][0]:
            if self.inner_points[0][1] < v.mouse_position[1] < self.inner_points[2][1]:
                self.on_button = True
                self.colour = 1
        else:
            self.on_button = False

    def draw(self):
        if self.variable == self.label:
            self.colour = 2
        elif self.on_button:
            self.colour = 1
        elif self.variable != self.label:
            self.colour = 0

        colours = [(0, 0, 0), (0, 128, 128), (0, 255, 255)]

        pygame.draw.polygon(self.surface, (255, 255, 255), self.outer_points)
        pygame.draw.polygon(self.surface, colours[self.colour], self.inner_points)

    def modify(self):
        if self.on_button:
            if v.event.type == 1026:
                f.modify_variables(self.variable_name, self.label)

    def all(self):
        self.hover_detect()
        self.draw()
        self.modify()


variable_names = ['v.game_dimensions',
                  'v.game_dimensions',
                  'v.game_dimensions',
                  'v.game_dimensions',
                  'v.game_dimensions',
                  'v.game_dimensions',
                  'v.game_dimensions',
                  'v.pure_game',
                  'v.pure_game',
                  'v.multiple_win',
                  'v.multiple_win']
                  # 'v.algorithm',
                  # 'v.algorithm',
                  # 'v.player',
                  # 'v.player']

values = [0, 1, 2, 3, 4, 5, 6,
          True, False,
          True, False]
          # True, False,
          # 0, 1]

offsets = [[-3, 27], [29, 27], [61, 27], [93, 27], [125, 27], [157, 27], [189, 27],
           [-3, 97], [29, 97],
           [-3, 167], [29, 167]]
           # [-3, 237], [29, 237],
           # [-3, 307], [29, 307]]
