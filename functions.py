import copy
import numpy as np
import random
import pygame
import math as m
import variables as v


def rotate(angle):
    matrix = np.array([[m.cos(angle), -m.sin(angle), 0],
                       [m.sin(angle), m.cos(angle), 0],
                       [0, 0, 1]])
    return matrix


def translate_to_observer(inverse_base, position, points):
    trans_points = points - position
    trans_points = inverse_base @ trans_points
    return trans_points


def perspective(trans_point):
    scaling_factor = v.screen_distance/trans_point[0]
    x = (v.screen_width / 2) + trans_point[1] * scaling_factor
    y = (v.screen_height / 2) - trans_point[2] * scaling_factor
    return [int(x), int(y)]


def corner_keys_from_center_key(key):
    keys = []
    str_coordinates = (key[1: -2].split(". "))
    crd = [int(str_coordinates[0]), int(str_coordinates[1]), int(str_coordinates[2])]
    corners = [[int(crd[0]) + 1., int(crd[1]) + 1., int(crd[2])],
               [int(crd[0]) + 1., int(crd[1]) - 1., int(crd[2])],
               [int(crd[0]) - 1., int(crd[1]) - 1., int(crd[2])],
               [int(crd[0]) - 1., int(crd[1]) + 1., int(crd[2])]]
    corners = np.array(corners)
    for i in range(4):
        keys.append(str(corners[i]))
    return keys


def add_forbidden_squares(nd_pos, forbidden, v_pos, squares_list):
    if not v.pure_game and not v.forbidden_tiles_added:
        index_list = []
        nd_position = len(nd_pos) // 2                                                         # add center square
        while len(forbidden) <= (len(nd_pos) // 9 - 1) * (1 + v.game_dimensions // 3):
            if nd_pos[nd_position] not in forbidden:
                forbidden.append(nd_pos[nd_position])
                index_list.append(nd_position)
            nd_position = random.randint(0, len(nd_pos) - 1)
        for i in range(len(forbidden)):
            forbidden_square = [10 ** 10, 0, forbidden[i], 0, v.forbidden_colour, 0, [0, 0], -1]
            forbidden_square[1] = str(v_pos[:, index_list[i]])
            forbidden_square[3] = corner_keys_from_center_key(forbidden_square[1])
            forbidden_square[5] = [[0, 0], [0, 0], [0, 0], [0, 0]]
            squares_list.append(forbidden_square)
    return True, forbidden, squares_list


def setup(dimensions):

    if dimensions == 0:
        nd_pos = [[0]]

    else:
        nd_coord = [[-1], [0], [1]]
        nd_pos = [[-1], [0], [1]]

        current_dimension = 1
        while current_dimension < dimensions:
            temp_nd_positions = []
            for i in range(len(nd_pos)):
                for j in range(3):
                    temp_nd_positions.append(nd_pos[i] + nd_coord[j])
            nd_pos = temp_nd_positions
            current_dimension += 1

    v_pos = []

    if len(nd_pos[0]) < 3:
        v_pos = copy.deepcopy(nd_pos)
        for i in range(len(v_pos)):
            for j in range(3 - len(nd_pos[i])):
                v_pos[i].append(0)

    else:
        for i in range(len(nd_pos)):
            v_point = copy.deepcopy([nd_pos[i][0], nd_pos[i][1], nd_pos[i][2]])
            for v_dim in range(3):
                n_dim, block = v_dim + 3, 6
                while n_dim < dimensions:
                    v_point[v_dim] += int(nd_pos[i][n_dim]) * block
                    n_dim += 3
                    block *= 5
            v_pos.append(v_point)

    v_pos = np.array(v_pos) * 2 * np.array([1, 1, 2.5])
    v_grid_points = np.concatenate((v_pos + ([1, 1, 0]), v_pos + ([1, -1, 0]),
                                    v_pos + ([-1, -1, 0]), v_pos + ([-1, 1, 0])))
    v_grid_points = np.unique(v_grid_points, axis=0)
    v_pos, v_grid_points = np.transpose(v_pos), np.transpose(v_grid_points)

    """
    line_values = [[], []]
    for i in range(2):
        counter = 0
        dimension_values = np.unique(v_grid_points[i, :])
        for j in range(dimension_values.shape[0]):
            if dimension_values[j] % 3 == 0:
                if counter % 2 == 0:
                    line_values[i].append(dimension_values[j])
                counter += 1

    lines = [['[-1. -1.  0.]', '[-1.  1.  0.]'],
             ['[ 1. -1.  0.]', '[1. 1. 0.]'],
             ['[-1. -1.  0.]', '[ 1. -1.  0.]'],
             ['[-1.  1.  0.]', '[1. 1. 0.]']]

    if dimensions == 1:
        lines += [['[-3. -1.  0.]', '[-3.  1.  0.]'], ['[ 3. -1.  0.]', '[3. 1. 0.]']]

    for i in range(2):
        line_end_adder = np.array([0, 0, 0])
        line_end_adder[i] = 6
        for j in range(v_grid_points.shape[1]):
            if v_grid_points[i][j] in line_values[i]:
                lines.append([(str(v_grid_points[:, j])), (str(v_grid_points[:, j] + line_end_adder))])
    """
    return v_grid_points, v_pos, nd_pos


def select(cursor_location, player, player_switch, square_order, forbidden, dictionaries, player_lists,
           trans_points_positions, grid_trans_points, squares_list, v_pos, mouse_input):

    squares = []
    keys = []
    center = 0
    points = [(0, 0), (0, 0), (0, 0), (0, 0)]
    square_in_question = [- 10 ** 10, (0, 0, 0), [[0, 0], [0, 0], [0, 0], [0, 0]]]

    for key in dictionaries[1].keys():
        center = perspective(trans_points_positions[:, dictionaries[1][key][0]])
        if abs(cursor_location[0] - center[0]) + abs(cursor_location[1] - center[1]) < 1500 // v.observer_dist:
            if dictionaries[1][key][1] not in forbidden:
                square_distance = determine_distance(v_pos[:, dictionaries[1][key][0]])
                squares.append([square_distance, key, dictionaries[1][key][1]])
    if len(squares):
        squares.sort()
        keys = corner_keys_from_center_key(squares[0][1])
        for i in range(4):
            points[i] = perspective(grid_trans_points[:, dictionaries[0][keys[i]]])
        square_in_question = [- squares[0][0], (v.select_colours[v.current_player]), points]
    if mouse_input.type == pygame.MOUSEBUTTONDOWN and mouse_input.button == 1 and len(squares):
        forbidden.append(squares[0][2])
        squares[0] += [keys]
        squares[0] += [(v.select_colours[v.current_player]), points, center]
        squares[0].append(square_order)
        square_order += 1
        squares_list.append(squares[0])
        player_lists[player].append(squares[0][2])
        player_switch = True
    return square_in_question, player_switch, square_order, forbidden, squares_list


def update_player(player, player_switch):
    if player_switch:
        player = 1 - player
        player_switch = False
    return player, player_switch


def determine_distance(point):
    observer_base, inverse_observer_base, observer_position = update_observer(v.observer_tilt, v.observer_dist)
    distance_vector = point - np.transpose(observer_position)
    distance = np.inner(distance_vector, distance_vector)
    return distance[0][0]


def update_observer(tilt, distance_from_origin):

    base = np.array([[m.cos(tilt), 0, -m.sin(tilt)],
                    [0, 1, 0],
                    [m.sin(tilt), 0, m.cos(tilt)]])

    inverse_base = np.linalg.inv(base)

    position = np.array([[-m.cos(tilt) * distance_from_origin],
                        [0],
                        [-m.sin(tilt) * distance_from_origin]])

    return base, inverse_base, position


def update_played_squares(squares_list, v_pos, dictionaries, trans_points_positions, trans_points_gridpoints):
    for i in range(len(squares_list)):
        squares_list[i][0] = - determine_distance(v_pos[:, dictionaries[1][squares_list[i][1]][0]])
        squares_list[i][6] = perspective(trans_points_positions[:, dictionaries[1][squares_list[i][1]][0]])
        for j in range(4):
            squares_list[i][5][j] = perspective(trans_points_gridpoints[:, dictionaries[0][squares_list[i][3][j]]])
    squares_list.sort()
    return squares_list


def third_point_finder(player, player_lists):
    points = player_lists[player]
    point_couples = []
    third_points = []
    elements = len(player_lists[player])
    for i in range((elements - 1) * int(len(points) >= 2)):
        for j in range(i + 1, elements):
            i_centrality, j_centrality = 0, 0
            third_point = []
            real_point_check = 0
            for d in range(v.game_dimensions):
                i_centrality += int(points[i][d] == 0)
                j_centrality += int(points[j][d] == 0)
            for d in range(v.game_dimensions):

                third_point.append((i_centrality == j_centrality) * (points[i][d] + points[j][d]) / 2

                                   + (i_centrality != j_centrality) * (points[i][d] == points[j][d])
                                   * points[i][d]

                                   + (i_centrality > j_centrality) * (points[i][d] != points[j][d])
                                   * (points[i][d] == 0) * (points[i][d] - points[j][d])

                                   + (i_centrality < j_centrality) * (points[i][d] != points[j][d])
                                   * (points[j][d] == 0) * (points[j][d] - points[i][d])

                                   + (i_centrality > j_centrality) * (points[i][d] != points[j][d])
                                   * (points[i][d] != 0) * 0.1

                                   + (i_centrality < j_centrality) * (points[i][d] != points[j][d])
                                   * (points[j][d] != 0) * 0.1)

            for d in range(v.game_dimensions):
                real_point_check += (third_point[d] == -1) + (third_point[d] == 0) + (third_point[d] == 1)
            for add in range(int(real_point_check == v.game_dimensions)):
                third_points.append(third_point)
                point_couples.append([points[i], points[j]])
    return third_points, point_couples


def win_check(game_won, player_lists, squares_list, surface):
    nd_trios = []
    for players in range(2):
        positions_to_check, corresponding_points = third_point_finder(players - v.current_player, player_lists)
        win_counter = [0, 0]
        for i in range(len(positions_to_check)):
            if positions_to_check[i] in player_lists[players - v.current_player]:
                overlap = False
                nd_trio = [positions_to_check[i], corresponding_points[i][0], corresponding_points[i][1]]
                for j in range(len(nd_trios)):
                    if nd_trio[0] in nd_trios[j] and nd_trio[1] in nd_trios[j] and nd_trio[2] in nd_trios[j]:
                        overlap = True
                if not overlap:
                    nd_trio.append(v.win_colours[players - v.current_player])
                    nd_trios.append(nd_trio)
                    for square in range(len(squares_list)):
                        if squares_list[square][2] in nd_trio:
                            squares_list[square][4] = nd_trio[-1]
                    win_counter[players - v.current_player] += 1
        if win_counter[0] >= v.win_threshold or win_counter[1] >= v.win_threshold:
            game_won = True
        if v.multiple_win:
            win_string = str(win_counter[players - v.current_player]) + ' / ' + str(v.game_dimensions - 1)
            wins_font = pygame.font.Font('JetBrainsMono-ExtraLight.ttf', 24)
            wins_txt = wins_font.render(win_string, False, v.win_colours[players - v.current_player])
            win_width, win_height = wins_txt.get_width(), wins_txt.get_height()
            win_pos = [40 + abs(players - v.current_player) * (v.screen_width - win_width - 80),
                       (v.screen_height - win_height) // 2]
            surface.blit(wins_txt, win_pos)
    return game_won, nd_trios, squares_list


def draw_transparent_square(points, colour, surface):

    x_min = min(points[0][0], points[1][0], points[2][0], points[3][0])
    x_max = max(points[0][0], points[1][0], points[2][0], points[3][0])
    y_min = min(points[0][1], points[1][1], points[2][1], points[3][1])
    y_max = max(points[0][1], points[1][1], points[2][1], points[3][1])

    temp_surface = pygame.Surface((x_max - x_min, y_max - y_min), pygame.SRCALPHA)

    adjusted_polygon_points = [[points[0][0] - x_min, points[0][1] - y_min],
                               [points[1][0] - x_min, points[1][1] - y_min],
                               [points[2][0] - x_min, points[2][1] - y_min],
                               [points[3][0] - x_min, points[3][1] - y_min]]

    pygame.draw.polygon(temp_surface, colour, adjusted_polygon_points)
    surface.blit(temp_surface, (x_min, y_min))


def draw_squares_back_to_front(squares_list, surface, preselect):
    if v.run:
        for plays in range(len(squares_list)):
            if squares_list[plays][0] < preselect[0]:
                if squares_list[plays][4] == v.forbidden_colour:
                    pygame.draw.polygon(surface, squares_list[plays][4], squares_list[plays][5])
                else:
                    draw_transparent_square(squares_list[plays][5], squares_list[plays][4], surface)
            else:
                break

        if not v.win_state:
            pygame.draw.polygon(surface, preselect[1], preselect[2])

        for plays in range(len(squares_list)):
            if squares_list[plays][0] >= preselect[0]:
                if squares_list[plays][4] == v.forbidden_colour:
                    pygame.draw.polygon(surface, squares_list[plays][4], squares_list[plays][5])
                else:
                    draw_transparent_square(squares_list[plays][5], squares_list[plays][4], surface)


def highlight_win(winning_trios, squares_list, surface):
    if v.run:
        lines = []
        for trio in range(len(winning_trios)):
            line = []
            for square in range(len(squares_list)):
                if squares_list[square][2] in winning_trios[trio]:
                    line.append(squares_list[square][6])
            line.append(winning_trios[trio][-1])
            lines.append(line)
        for line in range(len(lines)):
            for i in range(2):
                pygame.draw.line(surface, lines[line][-1], lines[line][i], lines[line][i + 1], 1)


def display_win_text(surface):
    if v.run and v.win_state:
        text = 'Player ' + str(1 - v.current_player + 1) + ' has won!'
        win_font = pygame.font.Font('JetBrainsMono-ExtraBold.ttf', 60)
        win_text = win_font.render(text, False, v.win_colours[1 - v.current_player])
        win_text_width = win_text.get_width()
        win_text_height = win_text.get_height()
        surface.blit(win_text, (v.screen_width // 2 - win_text_width // 2, v.screen_height // 2 - win_text_height))


def undo(player, squares_list, player_lists, forbidden):
    if len(player_lists[1 - player]) > 0:
        player = 1 - player
        player_lists[player].pop(-1)
        forbidden.pop(-1)
        squares_list = sorted(squares_list, key=lambda x: x[-1])
        if squares_list[-1][-1] >= 0:
            squares_list.pop(-1)
    game_won = False
    return player, squares_list, game_won, forbidden


def modify_variables(variable, value):
    if variable == 'v.game_dimensions':
        v.game_dimensions = value
    if variable == 'v.pure_game':
        v.pure_game = value
    if variable == 'v.multiple_win':
        v.multiple_win = value
        v.win_threshold = 1 + int(v.multiple_win) * (v.game_dimensions - 2)
    if variable == 'v.algorithm':
        v.algorithm = value
    if variable == 'v.player':
        v.player = value
