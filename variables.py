import pygame

pygame.init()
pygame.display.set_caption('n-dimensional tic tac toe')
ScreenInfo = pygame.display.Info()
screen_width, screen_height = int(ScreenInfo.current_w // 1.25), int(ScreenInfo.current_h // 1.25)
screen_distance = 2 * screen_width

run = True
menu = True
setup_complete = False
FPS = 60

game_dimensions = 3
pure_game = True
multiple_win = False
algorithm = True
player = 0

win_threshold = 1 + int(multiple_win) * (game_dimensions - 2)
observer_dist = max(15, int(game_dimensions * 15 * (1 + (game_dimensions // 3) / 2) ** (game_dimensions // 3)))

current_player = 0
change_player = False
win_state = False
forbidden_tiles_added = False

RotAngle = 0.004
observer_tilt = - 0.25

mouse_position = (640, 637)
event = 0

forbidden_colour = (255, 255, 255, 255)
select_colours = [(50, 50, 255, 180), (255, 50, 50, 180)]
win_colours = [(170, 170, 255, 255), (255, 170, 170, 255)]

order = 0
