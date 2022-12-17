# Title: Wandering in the Woods
# External Files: pygame
# Created Files: N/A
# Programmers: Rachael Morrison, Benjamin Ayirifa, Shivasai Priyatham Kota, Siva Prasad Polisetty
# Emails: rachaelnmorrison@lewisu.edu, shivasaipriyathamk@lewisu.edu, benjaminayirifa@lewisu.edu
#         sivaprasadpolisett@lewisu.edu
# Course: FA22-CPSC-60500-004
# Data of Submission: 12/16/2022
# Description: Computer simulation to help K-8 students learn about computation, computational thinking, math concepts,
#              and computer science. People are “lost in the woods” where the woods are represented by a rectangular
#              grid. The woods are dense, and the people can’t see or hear each other until they are in the same cell
#              of the grid. There are three levels for students to try as they progress through their school years.
# Resources: https://www.youtube.com/watch?v=T4IX36sP_0c&t=6094s (utilized loosely as a reference)

# file: main.py
# purpose: set up and start the game

import pygame
import sys
import os
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # set screen size with width and height
                                                                              # define in settings.py
        pygame.display.set_caption('Wandering in the Woods')  # set the display caption at top of screen
        self.clock = pygame.time.Clock()  # create a clock for the game
        self.level = Level(False)  # create the level, setting reinit to false since this is the first time initializing

        # background music
        self.music = pygame.mixer.Sound('..\\CPSC60500-Project\\sound\\music.mp3')
        self.music.set_volume(.5)
        self.music.play(loops=-1)

    def run(self):
        while True:
            event_list = pygame.event.get()  # gets list of events that will be used throughout the program
            # if the user clicks the red X the game is closed
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000  # delta time = tick/1000 = about 1 ms
            self.level.run(dt, event_list)  # run the level
            pygame.display.update()  # continuously update the display


if __name__ == '__main__':
    game = Game()  # create the game
    game.run()  # run the game
