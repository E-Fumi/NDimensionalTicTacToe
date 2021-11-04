import numpy as np
import pygame
from pygame.locals import *
import variables as v
import functions as f
import text as t
import objects as o

pygame.init()
pygame.display.set_caption('n-dimensional tic tac toe')
ScreenInfo = pygame.display.Info()
clock = pygame.time.Clock()

all_squares = []
preselect_square = []
player_0_positions = []
player_1_positions = []
play_lists = [player_0_positions, player_1_positions]
forbidden_positions = []
winning_positions = []
screen = pygame.display.set_mode((v.screen_width, v.screen_height))
surface = pygame.Surface((v.screen_width, v.screen_height), pygame.SRCALPHA)

while v.run:

    while v.menu:                                                                                    # Start Menu Block

        v.event = pygame.event.poll()
        if v.event.type == QUIT:
            v.menu = False
            v.run = False

        on_play_button = False
        buttons_initialized = False
        v.mouse_position = pygame.mouse.get_pos()
        surface.fill((0, 0, 0))

        button_list = []

        if not buttons_initialized:
            for i in range(len(o.values)):
                position = [t.text[4][2][0] + o.offsets[i][0], t.text[4][2][1] + o.offsets[i][1]]
                button = o.Button(surface, position, o.variable_names[i], o.values[i])
                button_list.append(button)
            buttons_initialized = True

        for i in range(len(button_list)):
            button_list[i].all()

        for i in range(len(t.q_mark_pos)):
            pygame.draw.circle(surface, t.text_colour, t.q_mark_pos[i], 25, 1)

        for i in range(t.indices[0]):
            surface.blit(t.text_items[i][0], t.text_items[i][1])

        for i in range(len(t.q_mark_pos)):
            if (v.mouse_position[0] - t.q_mark_pos[i][0]) ** 2 + (v.mouse_position[1] - t.q_mark_pos[i][1]) ** 2 < 625:
                for j in range(t.indices[i], t.indices[i + 1]):
                    surface.blit(t.text_items[j][0], t.text_items[j][1])

        if v.event.type == pygame.KEYDOWN:
            if v.event.key == pygame.K_f:
                v.pure_game = True

        if t.play_button[0] < v.mouse_position[0] < t.play_button[1]:
            if t.play_button[2] < v.mouse_position[1] < t.play_button[3]:
                on_play_button = True

        if pygame.mouse.get_pressed()[0] and on_play_button:
            v.menu = False

        screen.blit(surface, (0, 0))
        pygame.display.update()                                                                        # End Menu Block

    event = pygame.event.poll()
    if event.type == QUIT:
        v.run = False

    while not v.setup_complete:                                                                     # Start Setup Block

        point_array, playable_positions, nd_positions = f.setup(v.game_dimensions)

        Grid_points = {}
        for entry in range(np.shape(point_array)[1]):
            Grid_points[str(point_array[:, entry])] = [entry]

        Center_points = {}
        for entry in range(np.shape(playable_positions)[1]):
            Center_points[str(playable_positions[:, entry])] = [entry, nd_positions[entry]]

        dicts = [Grid_points, Center_points]

        D = v.game_dimensions
        v.observer_dist = max(15, int(D * 15 * (1 + (D // 3) / 2) ** (D // 3)))

        v.setup_complete = True                                                                       # End Setup Block

    cursor = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    surface.fill((0, 0, 0))

    v.forbidden_tiles_added, forbidden_positions, all_squares = \
        f.add_forbidden_squares(nd_positions, forbidden_positions, playable_positions, all_squares)

    # Start Graphics Module

    observer_base, inverse_observer_base, observer_position = f.update_observer(v.observer_tilt, v.observer_dist)
    point_array = f.rotate(v.RotAngle) @ point_array
    playable_positions = f.rotate(v.RotAngle) @ playable_positions
    trans_points_grid = f.translate_to_observer(inverse_observer_base, observer_position, point_array)
    trans_points_pos = f.translate_to_observer(inverse_observer_base, observer_position, playable_positions)

    # End Graphics Module

    if v.run:
        for k in Grid_points.keys():
            tpg = trans_points_grid[:, Grid_points[k]]
            pygame.draw.circle(surface, (255, 255, 255), f.perspective(tpg), 1, 0)

    if not v.win_state:
        preselect_square, v.change_player, v.order, forbidden_positions, all_squares = \
            f.select(cursor, v.current_player, v.change_player, v.order, forbidden_positions, dicts, play_lists,
                     trans_points_pos, trans_points_grid, all_squares, playable_positions, event)

        v.current_player, v.change_player = f.update_player(v.current_player, v.change_player)

    v.win_state, winning_positions, all_squares = f.win_check(v.win_state, play_lists, all_squares, surface)
    all_squares = f.update_played_squares(all_squares, playable_positions, dicts, trans_points_pos, trans_points_grid)
    f.draw_squares_back_to_front(all_squares, surface, preselect_square)
    # f.highlight_win(winning_positions, all_squares, surface)
    f.display_win_text(surface)

    """
    for i in range(len(line_list)):
        start = perspective(trans_points[:, Grid_points[line_list[i][0]][0]])
        end = perspective(trans_points[:, Grid_points[line_list[i][1]][0]])
        pygame.draw.line(screen, (255, 255, 255), start, end, 2)
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            v.RotAngle += 0.002
        if event.key == pygame.K_d:
            v.RotAngle -= 0.002
        if event.key == pygame.K_w:
            v.observer_tilt -= 0.05
        if event.key == pygame.K_s:
            v.observer_tilt += 0.05
        if event.key == pygame.K_q:
            v.observer_dist -= 20
        if event.key == pygame.K_e:
            v.observer_dist += 20
        if event.key == pygame.K_z:
            v.current_player, all_squares, v.win_state, forbidden_positions = \
                f.undo(v.current_player, all_squares, play_lists, forbidden_positions)
        if event.key == pygame.K_ESCAPE:
            v.forbidden_tiles_added = False
            v.setup_complete = False
            v.win_state = False
            v.menu = True
            all_squares = []
            player_0_positions = []
            player_1_positions = []
            forbidden_positions = []
            winning_positions = []
            play_lists = [[], []]
            surface.fill((0, 0, 0))
            v.mouse_position = (640, 637)
            v.current_player = 0
        if event.key == pygame.K_p:
            print(v.multiple_win)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 5:
            v.observer_dist += 5
        if event.button == 4:
            if v.observer_dist >= 15:
                v.observer_dist -= 5
    if pygame.mouse.get_pressed(5)[0]:
        delta_x = 0.003 * (v.mouse_position[0] - pygame.mouse.get_pos()[0])
        delta_y = 0.003 * (v.mouse_position[1] - pygame.mouse.get_pos()[1])
        v.observer_tilt += delta_y
        point_array, playable_positions = f.rotate(delta_x) @ point_array, f.rotate(delta_x) @ playable_positions

    v.mouse_position = pygame.mouse.get_pos()
    observer_base, inverse_observer_base, observer_position = f.update_observer(v.observer_tilt, v.observer_dist)
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(v.FPS)
