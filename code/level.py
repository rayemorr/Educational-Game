# file: level.py
# purpose: backbone of the game that initializes and updates the menu, players, and overlay as needed, and keeps track
#          of other game settings as needed

import pygame

from settings import *
from player import Player
from overlay import Overlay
from menu import Menu


class Level:
    def __init__(self, reinit):
        # get the display surface
        self.display_surface = pygame.display.get_surface()  # the display's surface (where everything will be drawn)

        # sprite groups
        self.all_sprites = pygame.sprite.Group()  # group containing all sprites

        # the default grid dimensions
        self.width = 5 * 64
        self.height = 5 * 64

        self.menu = Menu()  # create the menu that the player will navigate through to start the game

        #self.grid = False  # set to true when
        self.all_found = False  # set to true once all players are found
        self.reinit = reinit  # if the user exits to the main menu, the game will be reinitialized so this is set to
                              # true; used to reset the level before updating the menu
        self.players_created = False  # true once all player objects have been created

        # these help keep track of which players have found each other and to determine who should lead
        self.p12 = False  # true when player 1 and player 2 meet
        self.p13 = False  # true when player 1 and player 3 meet
        self.p14 = False  # true when player 1 and player 4 meet
        self.p23 = False  # true when player 2 and player 3 meet
        self.p24 = False  # true when player 2 and player 4 meet
        self.p34 = False  # true when player 3 and player 4 meet

        self.reset = False  # true when the user clicks the reset button
        self.times_reset = 0  # this is used to help determine average run times over multiple resets

        self.total_time = 0  # the total amount of time over multiple resets
        self.average_time = 0  # the average time over multiple resets
        self.best_time = 0  # the best run time over multiple resets
        self.wander = ''  # the wandering protocol for the best run
        # the grid dimensions for the best run
        self.best_width = 0
        self.best_height = 0

        self.players_placed = False  # true when all players have been placed by the user
        self.instructions_read = False  # true when the player hits the confirm button on the instructions screen
        self.found_updated = False  # true when all the players and the statistics have been updated; used to make sure
                                    # these values are not updated more than once

    # update different aspects of the level once the game is started
    def update(self):
        # updates the players' wandering protocols when a different once is selected in the menu
        for player in self.players:
            player.selected_protocol = self.menu.protocols[self.menu.pro_index]

        # board, overlay, and player settings need to be updated when a reset happens to adjust for user input
        if self.reset:
            self.width = self.menu.width * 64
            self.height = self.menu.height * 64
            self.overlay.selected_pro = self.menu.protocols[self.menu.pro_index]

            self.player1.turn = 0
            self.player1.board_width = self.width
            self.player1.board_height = self.height
            self.player1.start_pos = pygame.math.Vector2(32, 32)
            self.player2.turn = 1
            self.player2.board_width = self.width
            self.player2.board_height = self.height
            self.player2.start_pos = pygame.math.Vector2(self.width - 32, self.height - 32)
            if self.menu.playerNum >= 3:
                self.player3.turn = 0
                self.player3.board_width = self.width
                self.player3.board_height = self.height
                self.player3.start_pos = pygame.math.Vector2(self.width - 32, 32)
            if self.menu.playerNum == 4:
                self.player4.turn = 1
                self.player4.board_width = self.width
                self.player4.board_height = self.height
                self.player4.start_pos = pygame.math.Vector2(32, self.height - 32)

    # only run once to create all the players needed for the level
    # players are automatically placed for K-2, but for the other levels the players are not placed and player1 is
    # selected to be placed first
    # the overlay is also created using the player settings
    def create_players(self):
        self.width = self.menu.width * 64
        self.height = self.menu.height * 64

        self.player1 = Player((32, 32), self.all_sprites, self.width, self.height,
                              '..\\CPSC60500-Project\\graphics\\player1\\')
        self.player1.turn = 0
        if self.menu.level_selected >= 2:
            self.player1.selected = True
        else:
            self.player1.placed = True

        self.player2 = Player((self.width - 32, self.height - 32), self.all_sprites, self.width, self.height,
                              '..\\CPSC60500-Project\\graphics\\player2\\')
        self.player2.turn = 1
        if self.menu.level_selected == 1:
            self.player2.placed = True
            self.players_placed = True

        if self.menu.playerNum == 2:
            self.players = [self.player1, self.player2]
        if self.menu.playerNum >= 3:
            self.player3 = Player((self.width - 32, 32), self.all_sprites, self.width, self.height,
                                  '..\\CPSC60500-Project\\graphics\\player3\\')
            self.player3.turn = 0
            self.players = [self.player1, self.player2, self.player3]
        if self.menu.playerNum == 4:
            self.player4 = Player((32, self.height - 32), self.all_sprites, self.width, self.height,
                                  '..\\CPSC60500-Project\\graphics\\player4\\')
            self.player4.turn = 1
            self.players = [self.player1, self.player2, self.player3, self.player4]

        self.overlay = Overlay(self.players, self.menu.playerNum, self.menu.protocols[self.menu.pro_index])
        self.players_created = True

    # repeatedly draws the grid depending on the current width and height settings
    # also creates lines around the overlay
    def render_grid(self):
        white = (255, 255, 255)
        for x in range(0, self.height + 1, 64):
            pygame.draw.line(self.display_surface, white, (1, x), (self.width+1, x), 2)
        for x in range(0, self.width + 1, 64):
            pygame.draw.line(self.display_surface, white, (x, 1), (x, self.height+1), 2)
        pygame.draw.line(self.display_surface, white, (SCREEN_WIDTH-2, 1), (SCREEN_WIDTH-2, SCREEN_WIDTH-2), 2)
        pygame.draw.line(self.display_surface, white, (768, 1), (768, 768), 2)
        pygame.draw.line(self.display_surface, white, (768, 0), (960, 0), 2)
        pygame.draw.line(self.display_surface, white, (768, 768), (960, 768), 2)

    # uses player collisions to determine when players are found and which players will lead the others
    # once all the players are found, the menu is updated to show the game over screen, and the overlay is updated
    # to stop the timer. the level detects when the main menu or reset buttons are pressed, so it can either reset or
    # reinitialize the level along with the menu, player, and overlay settings
    def input(self, event_list):
        if self.menu.level_selected == 1:
            if self.player1.rect.collidepoint(self.player2.pos):
                self.player1.found = True
                self.player2.found = True
                self.all_found = True

        if self.menu.level_selected == 2 or self.menu.level_selected == 3:
            if self.menu.playerNum == 2:
                if self.player1.rect.collidepoint(self.player2.pos):
                    self.player1.found = True
                    self.player2.found = True
                    self.all_found = True

            if self.menu.playerNum >= 3:
                if self.player1.rect.collidepoint(self.player2.pos) or self.p12:
                    self.p12 = True
                    self.player1.found = True
                    self.player2.found = True
                    self.player2.follow(self.player1)
                    self.player1.lead = True
                if self.player1.rect.collidepoint(self.player3.pos) or self.p13:
                    self.p13 = True
                    self.player1.found = True
                    self.player3.found = True
                    self.player3.follow(self.player1)
                    self.player1.lead = True
                if self.player2.rect.collidepoint(self.player3.pos) or self.p23:
                    self.p23 = True
                    self.player2.found = True
                    self.player3.found = True
                    self.player3.follow(self.player2)
                    self.player2.lead = True
                if self.menu.playerNum != 4 and self.player1.found and self.player2.found and self.player3.found:
                    self.all_found = True
                    self.player1.lead = False
                    self.player2.lead = False
                    self.p12 = False
                    self.p13 = False
                    self.p23 = False

            if self.menu.playerNum == 4:
                if self.player1.rect.collidepoint(self.player4.pos) or self.p14:
                    self.p14 = True
                    self.player1.found = True
                    self.player4.found = True
                    self.player4.follow(self.player1)
                    self.player1.lead = True
                if self.player2.rect.collidepoint(self.player4.pos) or self.p24:
                    self.p24 = True
                    self.player2.found = True
                    self.player4.found = True
                    self.player4.follow(self.player2)
                    self.player2.lead = True
                if self.player3.rect.collidepoint(self.player4.pos) or self.p34:
                    self.p34 = True
                    self.player3.found = True
                    self.player4.found = True
                    self.player4.follow(self.player3)
                    self.player3.lead = True
                if self.player1.found and self.player2.found and self.player3.found and self.player4.found\
                        and self.player1.pos == self.player2.pos == self.player3.pos == self.player4.pos:
                    self.all_found = True
                    self.player1.lead = False
                    self.player2.lead = False
                    self.player3.lead = False
                    self.p12 = False
                    self.p13 = False
                    self.p23 = False
                    self.p14 = False
                    self.p24 = False
                    self.p34 = False

        if self.all_found:
            if not self.found_updated:
                self.times_reset = self.times_reset + 1
                self.total_time = self.total_time + self.overlay.game_time
                self.average_time = self.total_time / self.times_reset

                if self.best_time == 0 or self.best_time > self.overlay.game_time:
                    self.best_time = self.overlay.game_time
                    self.wander = self.overlay.selected_pro
                    self.best_width = self.width
                    self.best_height = self.height

                self.menu.total_time = self.total_time
                self.menu.average_time = self.average_time
                self.menu.best_time = self.best_time
                self.menu.wander = self.wander
                self.menu.best_width = self.best_width
                self.menu.best_height = self.best_height
                self.found_updated = True

            self.menu.game_over()
            self.overlay.game_over = True
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.menu.button1Rect.collidepoint(pygame.mouse.get_pos()):
                        self.reset = True
                        self.menu.over = False
                        self.overlay.game_over = False
                        self.instructions_read = False
                        self.all_found = False
                        self.found_updated = False
                        self.display_surface.fill('black')
                        if self.menu.level_selected == 3:
                            self.menu.started = False
                            self.menu.screen2 = True
                    if self.menu.button2Rect.collidepoint(pygame.mouse.get_pos()):
                        self.display_surface.fill('black')
                        self.__init__(True)

        if self.menu.started and not self.players_placed and self.menu.level_selected >= 2:
            if not self.instructions_read:
                self.menu.instructions()
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.menu.button1Rect.collidepoint(pygame.mouse.get_pos()):
                        self.menu.instruction = False
                        self.instructions_read = True

    # continuously run the level to update various level, menu, player, and overlay settings
    def run(self, dt, event_list):
        self.display_surface.fill('black')

        if self.menu.started:  # do this once the player hits the confirm button after the instructions
            if self.reset:  # run this only once to update player and overlay settings
                self.players_placed = False
                self.update()
                self.player1.reset()
                self.player2.reset()
                if self.menu.playerNum >= 3:
                    self.player3.reset()
                if self.menu.playerNum == 4:
                    self.player4.reset()

                if self.menu.level_selected >= 2:
                    self.player1.placed = False
                    self.player1.all_placed = False
                    self.player1.selected = True
                    self.player2.placed = False
                    self.player2.all_placed = False
                    self.player2.selected = False
                    if self.menu.playerNum >= 3:
                        self.player3.placed = False
                        self.player3.all_placed = False
                        self.player3.selected = False
                    if self.menu.playerNum == 4:
                        self.player4.placed = False
                        self.player4.all_placed = False
                        self.player4.selected = False

                self.overlay.reset()
                self.player1.selected = True

                self.reset = False

            self.render_grid()  # should always render the grid once the game is started
            self.all_sprites.draw(self.display_surface)  # always draw the sprites once game is starting
            self.all_sprites.update(dt)  # continuously update the sprites

            if self.players_created:  # update the level and overlay settings once the players are created
                self.update()
                self.overlay.display(dt)
            else:  # create the players if they have not already been created
                self.create_players()

            self.input(event_list)  # detect collisions and button clicks once the game is started

            if self.menu.level_selected >= 2:  # player placement will only be checked for 3-5 and 6-8 levels
                # once a player, the next once is selected until all players are placed
                if self.player1.placed:
                    self.player1.selected = False
                    self.player2.selected = True
                if self.menu.playerNum == 2:
                    if self.player2.placed:
                        self.player2.selected = False
                        self.players_placed = True
                if self.menu.playerNum == 3:
                    if self.player2.placed:
                        self.player2.selected = False
                        self.player3.selected = True
                    if self.player3.placed:
                        self.player3.selected = False
                        self.players_placed = True
                if self.menu.playerNum == 4:
                    if self.player2.placed:
                        self.player2.selected = False
                        self.player3.selected = True
                    if self.player3.placed:
                        self.player3.selected = False
                        self.player4.selected = True
                    if self.player4.placed:
                        self.player4.selected = False
                        self.players_placed = True

            # once all the players are placed, update the players, so they can start moving
            if self.players_placed:
                self.player1.all_placed = True
                self.player2.all_placed = True
                if self.menu.playerNum >= 3:
                    self.player3.all_placed = True
                if self.menu.playerNum == 4:
                    self.player4.all_placed = True

        # after the level is reinitialized, all the above code is run first before updating the menu
        if not self.reinit:
            self.menu.update(event_list)

        self.reinit = False
