# file: menu.py
# purpose: the menu screens for the game that the user is able to navigate through

import pygame
from settings import *
import datetime


class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()  # the display's surface

        # save colors so they are easy to access
        self.white = (255, 255, 255)
        self.dark = (70, 70, 70)

        # three main fonts used for title, captions, and buttons
        self.title_font = pygame.font.Font('freesansbold.ttf', 64)
        self.caption_font = pygame.font.Font('freesansbold.ttf', 32)
        self.button_font = pygame.font.Font('freesansbold.ttf', 20)

        # title and captions are used to display plain text
        self.title = self.title_font.render('Wandering in the Woods', True, self.white)  # rendered title
        self.caption = self.caption_font.render('Pick a level', True, self.white)  # initial caption on title screen
        self.caption2 = self.caption_font.render('', True, self.white)
        self.caption3 = self.caption_font.render('', True, self.white)
        self.caption4 = self.caption_font.render('', True, self.white)
        self.caption5 = self.caption_font.render('', True, self.white)

        # rectangle objects for title and captions
        self.titleRect = self.title.get_rect()
        self.captionRect = self.caption.get_rect()
        self.caption2Rect = self.caption2.get_rect()
        self.caption3Rect = self.caption3.get_rect()
        self.caption4Rect = self.caption4.get_rect()
        self.caption5Rect = self.caption5.get_rect()

        # used in situations where user is setting the value of one of the level settings
        self.value1 = self.caption_font.render('', True, self.white)
        self.value2 = self.caption_font.render('', True, self.white)

        # rectangle objects for values
        self.value1Rect = self.value1.get_rect()
        self.value2Rect = self.value2.get_rect()

        # options are the text displayed on buttons
        self.option1 = self.button_font.render('Grades K-2', True, self.white)  # button 1 text on title screen
        self.option2 = self.button_font.render('Grades 3-5', True, self.white)  # button 2 text on title screen
        self.option3 = self.button_font.render('Grades 6-8', True, self.white)  # button 3 text on title screen
        self.option4 = self.button_font.render('', True, self.white)
        self.option5 = self.button_font.render('', True, self.white)

        # rectangle objects for options
        self.option1Rect = self.option1.get_rect()
        self.option2Rect = self.option2.get_rect()
        self.option3Rect = self.option3.get_rect()
        self.option4Rect = self.option4.get_rect()
        self.option5Rect = self.option5.get_rect()

        self.button1Rect = self.option1.get_rect()
        self.button2Rect = self.option2.get_rect()
        self.button3Rect = self.option3.get_rect()
        self.button4Rect = self.option4.get_rect()
        self.button5Rect = self.option5.get_rect()

        # initialize size and positions for components used for title screen
        self.titleRect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200)
        self.captionRect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 50)

        self.option1Rect.center = ((SCREEN_WIDTH / 2) - 210, (SCREEN_HEIGHT / 2) + 70)
        self.option2Rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) + 70)
        self.option3Rect.center = ((SCREEN_WIDTH / 2) + 210, (SCREEN_HEIGHT / 2) + 70)

        self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 300, (SCREEN_HEIGHT / 2) + 10, 180, 120)
        self.button2Rect = pygame.Rect((SCREEN_WIDTH / 2) - 90, (SCREEN_HEIGHT / 2) + 10, 180, 120)
        self.button3Rect = pygame.Rect((SCREEN_WIDTH / 2) + 120, (SCREEN_HEIGHT / 2) + 10, 180, 120)

        self.started = False  # true when the player hits the confirm button on screen3
        self.level_selected = 0  # this value updates to match what options was picked on the title screen
        self.over = False  # true when the game is over
        self.instruction = False  # true when the player clicks the confirm button on the instruction screen
        self.playerNum = 2  # default number of players in a level is two, but is updated on screen1
        self.width = 5  # default grid width in tiles
        self.height = 5  # default grid height in tiles

        self.screen1 = False  # true when on screen1
        self.screen2 = False  # true when on screen2
        self.screen3 = False  # true when on screen3
        self.screen4 = False  # true when on screen4

        self.protocols = ['random', 'every other']  # two different protocol options
        self.pro_index = 0  # default is 0 for the 'random' protocol

        # these values are set by the level class and updated at the end of each game before a reset
        self.average_time = 0
        self.best_time = 0
        self.wander = ''
        self.best_width = 0
        self.best_height = 0

    # deals with all player interaction with the menu screens and buttons, which helps the menu navigate between screens
    def input(self, event_list):
        # the title screen is displayed when a level has not been selected
        if not self.level_selected:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP:
                    # K-2 button is clicked
                    if self.button1Rect.collidepoint(pygame.mouse.get_pos()):
                        self.button1Rect = pygame.Rect(0, 0, 0, 0)
                        self.button2Rect = pygame.Rect(0, 0, 0, 0)
                        self.button3Rect = pygame.Rect(0, 0, 0, 0)
                        self.display_surface.fill('black')
                        self.level_selected = 1
                    # 3-5 button is clicked
                    if self.button2Rect.collidepoint(pygame.mouse.get_pos()):
                        self.button1Rect = pygame.Rect(0, 0, 0, 0)
                        self.button2Rect = pygame.Rect(0, 0, 0, 0)
                        self.button3Rect = pygame.Rect(0, 0, 0, 0)
                        self.display_surface.fill('black')
                        self.level_selected = 2
                        self.screen1 = True
                    # 6-8 button is clicked
                    if self.button3Rect.collidepoint(pygame.mouse.get_pos()):
                        self.button1Rect = pygame.Rect(0, 0, 0, 0)
                        self.button2Rect = pygame.Rect(0, 0, 0, 0)
                        self.button3Rect = pygame.Rect(0, 0, 0, 0)
                        self.display_surface.fill('black')
                        self.level_selected = 3
                        self.screen1 = True

        # level 1 is selected but the game has not started yet, so the basic instruction screen is shown
        if self.level_selected == 1 and not self.started:
            # the two description lines
            self.caption_font = pygame.font.Font('freesansbold.ttf', 20)
            self.caption = self.caption_font.render('Two players will wander in the woods until they find each other. ',
                                                    True, self.white)
            self.captionRect = self.caption.get_rect()
            self.captionRect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 50)
            self.caption2 = self.caption_font.render('The time and the amount of moves they take is displayed on the '
                                                     'right side of the screen.', True, self.white)
            self.caption2Rect = self.caption.get_rect()
            self.caption2Rect.center = ((SCREEN_WIDTH / 2) - 115, (SCREEN_HEIGHT / 2) - 20)
            ###

            # the confirm button
            self.option1 = self.button_font.render('Confirm', True, self.white)
            self.option1Rect = self.option1.get_rect()
            self.button1Rect = self.option1.get_rect()
            self.option1Rect.center = ((SCREEN_WIDTH / 2) - 5, (SCREEN_HEIGHT / 2) + 52)
            self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 80, (SCREEN_HEIGHT / 2) + 10, 150, 80)
            ###

            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # the confirm button is clicked
                    if self.button1Rect.collidepoint(pygame.mouse.get_pos()):
                        self.button1Rect = pygame.Rect(0, 0, 0, 0)
                        self.display_surface.fill('black')
                        self.started = True

        # 3-5 or 6-8 levels are selected
        if self.level_selected == 2 or self.level_selected == 3:
            # screen 1
            # instruction caption
            self.caption_font = pygame.font.Font('freesansbold.ttf', 32)
            self.caption = self.caption_font.render('Select number of players.', True, self.white)
            self.captionRect = self.caption.get_rect()
            self.captionRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 50)
            ###

            # arrow buttons
            self.option1 = self.button_font.render('<-', True, self.white)
            self.option1Rect = self.option1.get_rect()
            self.button1Rect = self.option1.get_rect()
            self.option1Rect.center = ((SCREEN_WIDTH / 2) - 105, (SCREEN_HEIGHT / 2) + 60)
            self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 140, (SCREEN_HEIGHT / 2) + 40, 70, 40)

            self.option2 = self.button_font.render('->', True, self.white)
            self.option2Rect = self.option2.get_rect()
            self.button2Rect = self.option2.get_rect()
            self.option2Rect.center = ((SCREEN_WIDTH / 2) + 95, (SCREEN_HEIGHT / 2) + 60)
            self.button2Rect = pygame.Rect((SCREEN_WIDTH / 2) + 60, (SCREEN_HEIGHT / 2) + 40, 70, 40)
            ###

            # player number value
            self.caption_font = pygame.font.Font('freesansbold.ttf', 20)

            self.value1 = self.caption_font.render(str(self.playerNum), True, self.white)
            self.value1Rect = self.value1.get_rect()
            self.value1Rect.center = ((SCREEN_WIDTH / 2) - 7, (SCREEN_HEIGHT / 2) + 60)
            ###

            # confirm button
            self.option3 = self.button_font.render('Confirm', True, self.white)
            self.option3Rect = self.option3.get_rect()
            self.button3Rect = self.option3.get_rect()
            self.option3Rect.center = ((SCREEN_WIDTH / 2) - 5, (SCREEN_HEIGHT / 2) + 152)
            self.button3Rect = pygame.Rect((SCREEN_WIDTH / 2) - 80, (SCREEN_HEIGHT / 2) + 110, 150, 80)
            ###

            if self.screen1:
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONUP:
                        # left arrow button is clicked
                        if self.button1Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.playerNum > 2:
                                self.playerNum = self.playerNum - 1
                        # right arrow button is clicked
                        if self.button2Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.playerNum < 4:
                                self.playerNum = self.playerNum + 1
                        # confirm button is clicked
                        if self.button3Rect.collidepoint(pygame.mouse.get_pos()):
                            self.button1Rect = pygame.Rect(0, 0, 0, 0)
                            self.button2Rect = pygame.Rect(0, 0, 0, 0)
                            self.button3Rect = pygame.Rect(0, 0, 0, 0)

                            self.screen2 = True
                            self.display_surface.fill('black')

            if self.screen2:
                # screen 2
                # instruction caption
                self.caption_font = pygame.font.Font('freesansbold.ttf', 32)
                self.caption = self.caption_font.render('Select grid size.', True, self.white)
                self.captionRect = self.caption.get_rect()
                self.captionRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 50)
                ###

                # width caption
                self.caption_font = pygame.font.Font('freesansbold.ttf', 20)

                self.caption2 = self.caption_font.render('Width', True, self.white)
                self.caption2Rect = self.caption2.get_rect()
                self.caption2Rect.center = ((SCREEN_WIDTH / 2) - 200, (SCREEN_HEIGHT / 2) + 20)
                ###

                # height caption
                self.caption3 = self.caption_font.render('Height', True, self.white)
                self.caption3Rect = self.caption3.get_rect()
                self.caption3Rect.center = ((SCREEN_WIDTH / 2) + 190, (SCREEN_HEIGHT / 2) + 20)
                ###

                # width arrows
                self.option1 = self.button_font.render('<-', True, self.white)
                self.option1Rect = self.option1.get_rect()
                self.button1Rect = self.option1.get_rect()
                self.option1Rect.center = ((SCREEN_WIDTH / 2) - 300, (SCREEN_HEIGHT / 2) + 60)
                self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 335, (SCREEN_HEIGHT / 2) + 40, 70, 40)

                self.option2 = self.button_font.render('->', True, self.white)
                self.option2Rect = self.option2.get_rect()
                self.button2Rect = self.option2.get_rect()
                self.option2Rect.center = ((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) + 60)
                self.button2Rect = pygame.Rect((SCREEN_WIDTH / 2) - 135, (SCREEN_HEIGHT / 2) + 40, 70, 40)
                ###

                # width value
                self.value1 = self.caption_font.render(str(self.width), True, self.white)
                self.value1Rect = self.value1.get_rect()
                self.value1Rect.center = ((SCREEN_WIDTH / 2) - 202, (SCREEN_HEIGHT / 2) + 60)
                ###

                # height arrows
                self.option3 = self.button_font.render('<-', True, self.white)
                self.option3Rect = self.option3.get_rect()
                self.button3Rect = self.option3.get_rect()
                self.option3Rect.center = ((SCREEN_WIDTH / 2) + 90, (SCREEN_HEIGHT / 2) + 60)
                self.button3Rect = pygame.Rect((SCREEN_WIDTH / 2) + 55, (SCREEN_HEIGHT / 2) + 40, 70, 40)

                self.option4 = self.button_font.render('->', True, self.white)
                self.option4Rect = self.option4.get_rect()
                self.button4Rect = self.option4.get_rect()
                self.option4Rect.center = ((SCREEN_WIDTH / 2) + 290, (SCREEN_HEIGHT / 2) + 60)
                self.button4Rect = pygame.Rect((SCREEN_WIDTH / 2) + 255, (SCREEN_HEIGHT / 2) + 40, 70, 40)
                ###

                # height value
                self.value2 = self.caption_font.render(str(self.height), True, self.white)
                self.value2Rect = self.value2.get_rect()
                self.value2Rect.center = ((SCREEN_WIDTH / 2) + 192, (SCREEN_HEIGHT / 2) + 60)
                ###

                # confirm button
                self.option5 = self.button_font.render('Confirm', True, self.white)
                self.option5Rect = self.option5.get_rect()
                self.button5Rect = self.option5.get_rect()
                self.option5Rect.center = ((SCREEN_WIDTH / 2) - 5, (SCREEN_HEIGHT / 2) + 152)
                self.button5Rect = pygame.Rect((SCREEN_WIDTH / 2) - 80, (SCREEN_HEIGHT / 2) + 110, 150, 80)
                ###

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONUP:
                        # left width arrow is clicked
                        if self.button1Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.width > 2:
                                self.width = self.width - 1
                        # right width arrow is clicked
                        if self.button2Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.width < 12:
                                self.width = self.width + 1
                        # left height arrow is clicked
                        if self.button3Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.height > 2:
                                self.height = self.height - 1
                        # right height arrow is clicked
                        if self.button4Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.height < 12:
                                self.height = self.height + 1
                        # confirmed button is clicked
                        if self.button5Rect.collidepoint(pygame.mouse.get_pos()):
                            if not self.screen1:
                                self.button1Rect = pygame.Rect(0, 0, 0, 0)
                                self.button2Rect = pygame.Rect(0, 0, 0, 0)
                                self.button3Rect = pygame.Rect(0, 0, 0, 0)
                                self.button4Rect = pygame.Rect(0, 0, 0, 0)
                                self.button5Rect = pygame.Rect(0, 0, 0, 0)

                                # if level is 3-5 then go to screen 3
                                if self.level_selected == 2:
                                    self.screen2 = False
                                    self.screen3 = True
                                # if level 6-8 then go to screen 4
                                else:
                                    self.screen4 = True
                                self.display_surface.fill('black')
                            else:
                                self.screen1 = False

            if self.screen3:
                # screen 3
                # two captions used for instructions
                self.caption_font = pygame.font.Font('freesansbold.ttf', 20)
                self.caption = self.caption_font.render(
                    'Two players will wander in the woods until they find each other. ',
                    True, self.white)
                self.captionRect = self.caption.get_rect()
                self.captionRect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 50)

                self.caption2 = self.caption_font.render(
                    'The time and the amount of moves they take is displayed on the '
                    'right side of the screen.', True, self.white)
                self.caption2Rect = self.caption.get_rect()
                self.caption2Rect.center = ((SCREEN_WIDTH / 2) - 115, (SCREEN_HEIGHT / 2) - 20)
                ###

                # confirm button
                self.option1 = self.button_font.render('Confirm', True, self.white)
                self.option1Rect = self.option1.get_rect()
                self.button1Rect = self.option1.get_rect()
                self.option1Rect.center = ((SCREEN_WIDTH / 2) - 5, (SCREEN_HEIGHT / 2) + 152)
                self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 80, (SCREEN_HEIGHT / 2) + 110, 150, 80)
                ###

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # confirm button is clicked
                        if self.button1Rect.collidepoint(pygame.mouse.get_pos()):
                            # if level 3-5 is selected, start the level
                            if self.level_selected == 2:
                                if not self.screen2:
                                    self.button1Rect = pygame.Rect(0, 0, 0, 0)

                                    self.screen3 = False
                                    self.display_surface.fill('black')
                                    self.started = True
                                else:
                                    self.screen2 = False
                            # if level 6-8 is selected, go to screen 4
                            if self.level_selected == 3:
                                if not self.screen4:
                                    self.button1Rect = pygame.Rect(0, 0, 0, 0)

                                    self.screen3 = False
                                    self.display_surface.fill('black')
                                    self.started = True
                                else:
                                    self.screen4 = False

            if self.screen4:
                # screen 4
                # instruction caption
                self.caption_font = pygame.font.Font('freesansbold.ttf', 32)
                self.caption = self.caption_font.render('Select wandering protocol.', True, self.white)
                self.captionRect = self.caption.get_rect()
                self.captionRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 50)
                ###

                # arrow buttons
                self.option1 = self.button_font.render('<-', True, self.white)
                self.option1Rect = self.option1.get_rect()
                self.button1Rect = self.option1.get_rect()
                self.option1Rect.center = ((SCREEN_WIDTH / 2) - 115, (SCREEN_HEIGHT / 2) + 60)
                self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) + 40, 70, 40)

                self.option2 = self.button_font.render('->', True, self.white)
                self.option2Rect = self.option2.get_rect()
                self.button2Rect = self.option2.get_rect()
                self.option2Rect.center = ((SCREEN_WIDTH / 2) + 105, (SCREEN_HEIGHT / 2) + 60)
                self.button2Rect = pygame.Rect((SCREEN_WIDTH / 2) + 70, (SCREEN_HEIGHT / 2) + 40, 70, 40)
                ###

                # protocol value
                self.caption_font = pygame.font.Font('freesansbold.ttf', 20)
                self.value1 = self.caption_font.render(self.protocols[self.pro_index], True, self.white)
                self.value1Rect = self.value1.get_rect()
                self.value1Rect.center = ((SCREEN_WIDTH / 2) - 7, (SCREEN_HEIGHT / 2) + 60)
                ###

                # confirm button
                self.option3 = self.button_font.render('Confirm', True, self.white)
                self.option3Rect = self.option3.get_rect()
                self.button3Rect = self.option3.get_rect()
                self.option3Rect.center = ((SCREEN_WIDTH / 2) - 5, (SCREEN_HEIGHT / 2) + 152)
                self.button3Rect = pygame.Rect((SCREEN_WIDTH / 2) - 80, (SCREEN_HEIGHT / 2) + 110, 150, 80)
                ###

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONUP:
                        # left arrow is clicked
                        if self.button1Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.pro_index == 0:
                                self.pro_index = 2
                            else:
                                self.pro_index = self.pro_index - 1
                        # right arrow is clicked
                        if self.button2Rect.collidepoint(pygame.mouse.get_pos()):
                            if self.pro_index == 2:
                                self.pro_index = 0
                            else:
                                self.pro_index = self.pro_index + 1
                        # confirm button is clicked, start the game
                        if self.button3Rect.collidepoint(pygame.mouse.get_pos()):
                            if not self.screen2:
                                self.button1Rect = pygame.Rect(0, 0, 0, 0)
                                self.button2Rect = pygame.Rect(0, 0, 0, 0)
                                self.button3Rect = pygame.Rect(0, 0, 0, 0)

                                self.screen4 = False
                                self.screen3 = True
                                self.display_surface.fill('black')
                            else:
                                self.screen2 = False

    # game over screen
    # only displays once all the players have found each other
    def game_over(self):
        self.over = True

        # caption
        self.caption_font = pygame.font.Font('freesansbold.ttf', 20)
        self.caption = self.caption_font.render('All of the players have found each other!',
                                                True, self.white)
        self.captionRect = self.caption.get_rect()
        self.captionRect.center = ((SCREEN_WIDTH / 2) + 10, (SCREEN_HEIGHT / 2) - 70)
        ###

        # reset button
        self.option1 = self.button_font.render('Reset', True, self.white)
        self.option1Rect = self.option1.get_rect()
        self.button1Rect = self.option1.get_rect()
        self.option1Rect.center = ((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) + 32)
        self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 175, (SCREEN_HEIGHT / 2) - 10, 150, 80)
        ###

        # main menu button
        self.option2 = self.button_font.render('Main Menu', True, self.white)
        self.option2Rect = self.option2.get_rect()
        self.button2Rect = self.option2.get_rect()
        self.option2Rect.center = ((SCREEN_WIDTH / 2) + 120, (SCREEN_HEIGHT / 2) + 32)
        self.button2Rect = pygame.Rect((SCREEN_WIDTH / 2) + 45, (SCREEN_HEIGHT / 2) - 10, 150, 80)
        ###

        # average time stat
        self.caption_font = pygame.font.Font('freesansbold.ttf', 15)
        self.caption2 = self.caption_font.render('Average time: {}'.format(
            datetime.timedelta(seconds=round(self.average_time))), True, self.white)
        self.caption2Rect = self.caption2.get_rect()
        self.caption2Rect.center = (120, 300)
        ###

        # best time stat
        self.caption3 = self.caption_font.render('Best time: {}'.format(
            datetime.timedelta(seconds=round(self.best_time))), True, self.white)
        self.caption3Rect = self.caption3.get_rect()
        self.caption3Rect.center = (120, 350)
        ###

        # wandering protocol stat
        self.caption4 = self.caption_font.render('Best wander: {}'.format(self.wander), True, self.white)
        self.caption4Rect = self.caption4.get_rect()
        self.caption4Rect.center = (120, 400)
        ###

        # dimensions stat
        self.caption5 = self.caption_font.render(
            'Best dimensions: {} x {}'.format(round(self.best_width/64), round(self.best_height/64)), True, self.white)
        self.caption5Rect = self.caption5.get_rect()
        self.caption5Rect.center = (120, 450)
        ###

    # instructions screen
    # only displays on the 3-5 or 6-8 levels to instruct the user on how to place the players in the grid
    def instructions(self):
        self.instruction = True
        # instruction captions
        self.caption_font = pygame.font.Font('freesansbold.ttf', 20)
        self.caption = self.caption_font.render('Use arrows keys to move players.',
                                                True, self.white)
        self.captionRect = self.caption.get_rect()
        self.captionRect.center = ((SCREEN_WIDTH / 2) + 10, (SCREEN_HEIGHT / 2) - 70)

        self.caption2 = self.caption_font.render('Use the enter key to place the players.', True, self.white)
        self.caption2Rect = self.caption.get_rect()
        self.caption2Rect.center = ((SCREEN_WIDTH / 2) - 13, (SCREEN_HEIGHT / 2) - 40)
        ###

        # confirm button
        self.option1 = self.button_font.render('Confirm', True, self.white)
        self.option1Rect = self.option1.get_rect()
        self.button1Rect = self.option1.get_rect()
        self.option1Rect.center = ((SCREEN_WIDTH / 2) + 5, (SCREEN_HEIGHT / 2) + 62)
        self.button1Rect = pygame.Rect((SCREEN_WIDTH / 2) - 70, (SCREEN_HEIGHT / 2) + 20, 150, 80)
        ###

    def display(self):
        if self.level_selected == 0:
            # display title screen components
            self.display_surface.blit(self.title, self.titleRect)

            self.display_surface.blit(self.caption, self.captionRect)

            pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
            pygame.draw.rect(self.display_surface, self.dark, self.button2Rect)
            pygame.draw.rect(self.display_surface, self.dark, self.button3Rect)
            self.display_surface.blit(self.option1, self.option1Rect)
            self.display_surface.blit(self.option2, self.option2Rect)
            self.display_surface.blit(self.option3, self.option3Rect)

        if self.level_selected == 1 and not self.started:
            # display instructions for K-2 level
            self.display_surface.blit(self.caption, self.captionRect)
            self.display_surface.blit(self.caption2, self.caption2Rect)

            pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
            self.display_surface.blit(self.option1, self.option1Rect)

        if self.level_selected == 2 or self.level_selected == 3 and not self.started:
            if self.screen1:
                # display screen 1 components
                self.display_surface.blit(self.caption, self.captionRect)

                pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
                self.display_surface.blit(self.option1, self.option1Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button2Rect)
                self.display_surface.blit(self.option2, self.option2Rect)

                self.display_surface.blit(self.value1, self.value1Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button3Rect)
                self.display_surface.blit(self.option3, self.option3Rect)

            if self.screen2:
                # display screen 2 components
                self.display_surface.blit(self.caption, self.captionRect)
                self.display_surface.blit(self.caption2, self.caption2Rect)
                self.display_surface.blit(self.caption3, self.caption3Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
                self.display_surface.blit(self.option1, self.option1Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button2Rect)
                self.display_surface.blit(self.option2, self.option2Rect)

                self.display_surface.blit(self.value1, self.value1Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button3Rect)
                self.display_surface.blit(self.option3, self.option3Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button4Rect)
                self.display_surface.blit(self.option4, self.option4Rect)

                self.display_surface.blit(self.value2, self.value2Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button5Rect)
                self.display_surface.blit(self.option5, self.option5Rect)

            if self.screen3:
                # display screen 3 components
                self.display_surface.blit(self.caption, self.captionRect)
                self.display_surface.blit(self.caption2, self.caption2Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
                self.display_surface.blit(self.option1, self.option1Rect)

            if self.screen4:
                # display screen 4 components
                self.display_surface.blit(self.caption, self.captionRect)

                pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
                self.display_surface.blit(self.option1, self.option1Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button2Rect)
                self.display_surface.blit(self.option2, self.option2Rect)

                self.display_surface.blit(self.value1, self.value1Rect)

                pygame.draw.rect(self.display_surface, self.dark, self.button3Rect)
                self.display_surface.blit(self.option3, self.option3Rect)

        if self.over:
            # display game over screen components
            pygame.draw.rect(self.display_surface, self.dark,
                             pygame.Rect((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 4), 500, 350))
            pygame.draw.rect(self.display_surface, 'black',
                             pygame.Rect((SCREEN_WIDTH / 4) + 4, (SCREEN_HEIGHT / 4) + 4, 492, 342))

            self.display_surface.blit(self.caption, self.captionRect)

            pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
            self.display_surface.blit(self.option1, self.option1Rect)

            pygame.draw.rect(self.display_surface, self.dark, self.button2Rect)
            self.display_surface.blit(self.option2, self.option2Rect)

            pygame.draw.rect(self.display_surface, self.dark,
                             pygame.Rect(10, 192, 220, 350))
            pygame.draw.rect(self.display_surface, 'black',
                             pygame.Rect(14, 196, 212, 342))

            self.display_surface.blit(self.caption2, self.caption2Rect)
            self.display_surface.blit(self.caption3, self.caption3Rect)
            self.display_surface.blit(self.caption4, self.caption4Rect)
            self.display_surface.blit(self.caption5, self.caption5Rect)

        if self.instruction:
            # display instruction screen components
            pygame.draw.rect(self.display_surface, self.dark,
                             pygame.Rect((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 4), 500, 350))
            pygame.draw.rect(self.display_surface, 'black',
                             pygame.Rect((SCREEN_WIDTH / 4) + 4, (SCREEN_HEIGHT / 4) + 4, 492, 342))

            self.display_surface.blit(self.caption, self.captionRect)
            self.display_surface.blit(self.caption2, self.caption2Rect)

            pygame.draw.rect(self.display_surface, self.dark, self.button1Rect)
            self.display_surface.blit(self.option1, self.option1Rect)

    # continuously display components and handle user input
    def update(self, event_list):
        self.display()
        self.input(event_list)
