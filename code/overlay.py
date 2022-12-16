# file: overlay.py
# purpose: displays current statistics for the level being played on the right side of the screen

import pygame
from settings import *
import datetime


class Overlay:
    def __init__(self, players, player_num, selected_pro):
        # general setup
        self.display_surface = pygame.display.get_surface()  # display's surface
        self.p_names = ['player1', 'player2', 'player3', 'player4']  # player names used for importing images
        self.players = players  # player objects
        self.game_time = 0  # game time that starts once the level starts and all players are placed
        self.playerNum = player_num  # number of players being used in the level
        self.selected_pro = selected_pro  # selected wandering protocol

        # import the player surfaces
        overlay_path = '..\\CPSC60500-Project\\graphics\\overlay\\'
        self.players_surf = {player: pygame.image.load(f'{overlay_path}{player}.png').convert_alpha() for player in
                             self.p_names}

        # labels
        self.white = (255, 255, 255)
        self.time_font = pygame.font.Font('freesansbold.ttf', 25)
        self.label_font = pygame.font.Font('freesansbold.ttf', 16)

        self.time_lbl = self.time_font.render('Time:', True, self.white)
        self.time_lblRect = self.time_lbl.get_rect()
        self.time_lblRect.center = (SCREEN_WIDTH - 98, 30)

        # timer
        self.time = self.time_font.render('{}'.format(datetime.timedelta(seconds=round(self.game_time))), True,
                                          self.white)
        self.timeRect = self.time.get_rect()
        self.timeRect.center = (SCREEN_WIDTH - 98, 60)

        # move counters for player 1 and player 2
        self.p1_moves_lbl = self.label_font.render('Moves:', True, self.white)
        self.p1_moves_lblRect = self.p1_moves_lbl.get_rect()
        self.p1_moves_lblRect.center = (SCREEN_WIDTH - 98, 215)

        self.p1_moves = self.label_font.render('{}'.format(self.players[0].moves), True, self.white)
        self.p1_movesRect = self.p1_moves.get_rect()
        self.p1_movesRect.center = (SCREEN_WIDTH - 98, 235)

        self.p2_moves_lbl = self.label_font.render('Moves:', True, self.white)
        self.p2_moves_lblRect = self.p2_moves_lbl.get_rect()
        self.p2_moves_lblRect.center = (SCREEN_WIDTH - 98, 335)

        self.p2_moves = self.label_font.render('{}'.format(self.players[1].moves), True, self.white)
        self.p2_movesRect = self.p2_moves.get_rect()
        self.p2_movesRect.center = (SCREEN_WIDTH - 98, 355)

        # move counter for player 3
        if self.playerNum >= 3:
            self.p3_moves_lbl = self.label_font.render('Moves:', True, self.white)
            self.p3_moves_lblRect = self.p3_moves_lbl.get_rect()
            self.p3_moves_lblRect.center = (SCREEN_WIDTH - 98, 455)

            self.p3_moves = self.label_font.render('{}'.format(self.players[2].moves), True, self.white)
            self.p3_movesRect = self.p3_moves.get_rect()
            self.p3_movesRect.center = (SCREEN_WIDTH - 98, 475)

        # move counter for player 4
        if self.playerNum == 4:
            self.p4_moves_lbl = self.label_font.render('Moves:', True, self.white)
            self.p4_moves_lblRect = self.p4_moves_lbl.get_rect()
            self.p4_moves_lblRect.center = (SCREEN_WIDTH - 98, 575)

            self.p4_moves = self.label_font.render('{}'.format(self.players[3].moves), True, self.white)
            self.p4_movesRect = self.p4_moves.get_rect()
            self.p4_movesRect.center = (SCREEN_WIDTH - 98, 655)

        # dimensions
        self.dim_lbl = self.label_font.render('Board Size:', True, self.white)
        self.dim_lblRect = self.dim_lbl.get_rect()
        self.dim_lblRect.center = (SCREEN_WIDTH - 98, 670)

        self.dim = self.label_font.render('{} x {}'.format(int(self.players[0].board_width/64),
                                                           int(self.players[0].board_height/64)), True, self.white)
        self.dimRect = self.dim.get_rect()
        self.dimRect.center = (SCREEN_WIDTH - 98, 690)

        self.pattern_lbl = self.label_font.render('Wandering:', True, self.white)
        self.pattern_lblRect = self.pattern_lbl.get_rect()
        self.pattern_lblRect.center = (SCREEN_WIDTH - 98, 720)

        self.pattern = self.label_font.render('{}'.format(self.selected_pro), True, self.white)
        self.patternRect = self.pattern.get_rect()
        self.patternRect.center = (SCREEN_WIDTH - 98, 740)

        self.game_over = False  # level will set this to true when all the players are together

    # reset game time, dimensions, and the movement protocol
    def reset(self):
        self.game_time = 0

        self.dim = self.label_font.render('{} x {}'.format(int(self.players[0].board_width / 64),
                                                           int(self.players[0].board_height / 64)), True, self.white)
        self.dimRect = self.dim.get_rect()
        self.dimRect.center = (SCREEN_WIDTH - 98, 690)

        self.pattern = self.label_font.render('{}'.format(self.selected_pro), True, self.white)
        self.patternRect = self.pattern.get_rect()
        self.patternRect.center = (SCREEN_WIDTH - 98, 740)

    # continuously displays all the components while the game is active
    def display(self, dt):
        # update time
        if not self.game_over and self.players[0].all_placed:
            self.game_time += dt

        # time
        self.display_surface.blit(self.time_lbl, self.time_lblRect)

        self.time = self.time_font.render('{}'.format(datetime.timedelta(seconds=round(self.game_time))), True,
                                          self.white)
        self.timeRect = self.time.get_rect()
        self.timeRect.center = (SCREEN_WIDTH - 98, 60)
        self.display_surface.blit(self.time, self.timeRect)

        # players
        player1_surf = self.players_surf['player1']
        player1_rect = player1_surf.get_rect(midright=OVERLAY_POSITIONS['player1'])
        self.display_surface.blit(player1_surf, player1_rect)

        player2_surf = self.players_surf['player2']
        player2_rect = player2_surf.get_rect(midright=OVERLAY_POSITIONS['player2'])
        self.display_surface.blit(player2_surf, player2_rect)

        self.display_surface.blit(self.p1_moves_lbl, self.p1_moves_lblRect)

        self.p1_moves = self.label_font.render('{}'.format(self.players[0].moves), True, self.white)
        self.p1_movesRect = self.p1_moves.get_rect()
        self.p1_movesRect.center = (SCREEN_WIDTH - 98, 235)
        self.display_surface.blit(self.p1_moves, self.p1_movesRect)

        self.display_surface.blit(self.p2_moves_lbl, self.p2_moves_lblRect)

        self.p2_moves = self.label_font.render('{}'.format(self.players[1].moves), True, self.white)
        self.p2_movesRect = self.p2_moves.get_rect()
        self.p2_movesRect.center = (SCREEN_WIDTH - 98, 355)
        self.display_surface.blit(self.p2_moves, self.p2_movesRect)

        if self.playerNum >= 3:
            player3_surf = self.players_surf['player3']
            player3_rect = player3_surf.get_rect(midright=OVERLAY_POSITIONS['player3'])
            self.display_surface.blit(player3_surf, player3_rect)

            self.display_surface.blit(self.p3_moves_lbl, self.p3_moves_lblRect)

            self.p3_moves = self.label_font.render('{}'.format(self.players[2].moves), True, self.white)
            self.p3_movesRect = self.p3_moves.get_rect()
            self.p3_movesRect.center = (SCREEN_WIDTH - 98, 475)
            self.display_surface.blit(self.p3_moves, self.p3_movesRect)

        if self.playerNum == 4:
            player4_surf = self.players_surf['player4']
            player4_rect = player4_surf.get_rect(midright=OVERLAY_POSITIONS['player4'])
            self.display_surface.blit(player4_surf, player4_rect)

            self.display_surface.blit(self.p4_moves_lbl, self.p4_moves_lblRect)

            self.p4_moves = self.label_font.render('{}'.format(self.players[3].moves), True, self.white)
            self.p4_movesRect = self.p4_moves.get_rect()
            self.p4_movesRect.center = (SCREEN_WIDTH - 98, 595)
            self.display_surface.blit(self.p4_moves, self.p4_movesRect)

        # dimensions
        self.display_surface.blit(self.dim_lbl, self.dim_lblRect)
        self.display_surface.blit(self.dim, self.dimRect)

        # movement protocol
        self.display_surface.blit(self.pattern_lbl, self.pattern_lblRect)
        self.display_surface.blit(self.pattern, self.patternRect)
