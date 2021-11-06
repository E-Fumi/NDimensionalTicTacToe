import pygame
import variables as v

text_colour = (255, 255, 255)

title_font = pygame.font.Font('JetBrainsMono-ExtraLight.ttf', 20)
menu_font = pygame.font.Font('JetBrainsMono-ExtraBold.ttf', 36)
regular_font = pygame.font.Font('JetBrainsMono-ExtraLight.ttf', 16)
question_mark_font = pygame.font.Font('JetBrainsMono-ExtraBold.ttf', 20)
option_font = pygame.font.Font('JetBrainsMono-ExtraLight.ttf', 14)
play_font = pygame.font.Font('JetBrainsMono-ExtraBold.ttf', 26)

text_items = []

text = [
        [['WELCOME TO N-DIMENSIONAL TIC TAC TOE'],
         title_font, [-1, 40], 0],

        [['MENU'],
         menu_font, [-1, 100], 0],

        [['SELECT DIMENSIONS:',
          'PURE GAME:',
          'MULTIPLE WINS:',
          # 'PLAY AGAINST PROGRAM:',
          # 'PLAY AS PLAYER:',
          'INSTRUCTIONS'],
         regular_font, [130, 180 + 45], 70],

        [['?',
          '?',
          '?',
          # '?',
          # '?',
          '?'],
         question_mark_font, [50, 177 + 45], 70],

        [['0   1   2   3   4   5   6   7',
          'Y   N',
          'Y   N'],
         # 'Y   N',
         # '1   2'],
         option_font, [400, 155 + 45], 70],

        [['PLAY'],
         play_font, [-1, 620], 0],

        [['TIC TAC TOE IS USUALLY PLAYED ON A 2D 3 X 3 GRID',
          'IT CAN ALSO BE PLAYED IN A 3D 3 X 3 X 3 CUBE',
          'OR IN A 4D 3 X 3 X 3 X 3 HYPERCUBE',
          'OR ANY ARBITRARY NUMBER OF DIMENSIONS',
          '',
          'ANY HIGHER DIMENSIONAL PLAYING FIELD CAN BE',
          'REPRESENTED BY THREE LOWER DIMENSIONAL (D - 1)',
          'PLAYING FIELDS THE SAME WAY A TIC TAC TOE CUBE',
          'COULD BE REPRESENTED AS THREE TIC TAC TOE ',
          'SQUARES LAID SIDE BY SIDE',
          '',
          'IN THIS REPRESENTATION PLAYING FIELDS OF ANY ',
          'DIMENSION ARE SHOWN AS A SET OF CUBES AND',
          'ANY THREE WINNING POSITIONS WILL ALWAYS',
          'BE IN A STRAIGHT LINE'],
         regular_font, [700, 180], 25],

        [['IN A PURE GAME, ALL POSITIONS IN THE',
          '3^N PLAYING FIELD ARE AVAILABLE',
          '',
          'THE NUMBER OF POTENTIAL WINNING',
          'TRIPLETS INCREASES EXPONENTIALLY',
          'WITH THE NUMBER OF DIMENSIONS',
          '',
          'THIS MAKES IT INCREASINGLY UNLIKELY',
          'FOR THE SECOND PLAYER TO WIN',
          '',
          'THE GAME CAN BE BALANCED BY',
          'BLOCKING OFF RANDOM POSITIONS'],
         regular_font, [700, 200], 25],

        [['THE NUMBER OF POSSIBLE TRIOS OF POSITIONS',
          'INCREASES EXPONENTIALLY WITH THE',
          'NUMBER OF DIMENSIONS',
          '',
          'HIGHER DIMENSIONAL GAMES CAN BE MADE',
          'MORE INTERESTING BY INCREASING THE',
          'NUMBER OF COMPLETED TRIOS',
          'REQUIRED FOR A WIN'],
         regular_font, [700, 225], 25],

        # [['WORK IN PROGRESS'],
        # regular_font, [700, 225], 25],

        # [['THIS OUGHT TO BE',
        # 'SELF-EXPLANATORY'],
        # regular_font, [700, 225], 25],

        [['SELECT SQUARE: MOUSE BUTTON 1',
          'ADJUST ANGLE: MOUSE BUTTON 1 + MOUSE MOVEMENT',
          'ZOOM IN: MOUSEWHEEL UP OR Q',
          'ZOOM OUT: MOUSEWHEEL DOWN OR E',
          'MODULATE ROTATION: A D',
          'RESTART GAME: ESC',
          'UNDO: Z'],
         regular_font, [700, 200], 50]
        ]

q_mark_pos = []
play_button = []
index = 0
indices = []
starting_snippets = ['TIC TAC TOE IS USUALLY PLAYED ON A 2D 3 X 3 GRID',
                     'IN A PURE GAME, ALL POSITIONS IN THE',
                     'THE NUMBER OF POSSIBLE TRIOS OF POSITIONS',
                     # 'WORK IN PROGRESS',
                     # 'THIS REALLY OUGHT TO BE',
                     'SELECT SQUARE: MOUSE BUTTON 1']

for i in range(len(text)):
    for j in range(len(text[i][0])):
        item_text = text[i][0][j]
        item = text[i][1].render(item_text, False, text_colour)

        if text[i][2][0] == -1:
            item_width = item.get_width()
            text[i][2][0] = v.screen_width // 2 - item_width // 2
        increment = text[i][3]
        item_position = (text[i][2][0], text[i][2][1] + (j * increment))
        text_items.append([item, item_position])

        if item_text == '?':
            q_mark_width = item.get_width()
            q_mark_height = item.get_height()
            q_mark_pos.append([item_position[0] + q_mark_width // 2,
                               item_position[1] + q_mark_height // 2])

        if item_text == 'PLAY':
            play_width = item.get_width()
            play_height = item.get_height()
            play_button = [item_position[0], item_position[0] + play_width,
                           item_position[1], item_position[1] + play_height]

        if item_text in starting_snippets:
            indices.append(index)
        index += 1

indices.append(index)
