import random

import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.time_elapsed = 0
        self.game_time = 0

        self.curr_x = self.pos.x
        self.curr_y = self.pos.y
        self.moves = 0

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = '..\\CPSC60500-Project\\graphics\\player1\\' + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    # def input(self):
    #     keys = pygame.key.get_pressed()
    #
    #     if keys[pygame.K_UP]:
    #         self.direction.y = -1
    #         self.status = 'up'
    #     elif keys[pygame.K_DOWN]:
    #         self.direction.y = 1
    #         self.status = 'down'
    #     else:
    #         self.direction.y = 0
    #
    #     if keys[pygame.K_RIGHT]:
    #         self.direction.x = 1
    #         self.status = 'right'
    #     elif keys[pygame.K_LEFT]:
    #         self.direction.x = -1
    #         self.status = 'left'
    #     else:
    #         self.direction.x = 0

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def move_randomly(self, dt):
        self.time_elapsed += dt

        if self.time_elapsed > 2:
            rand = random.randint(0, 3)
            # print("rand: " + str(rand))

            if rand == 0:
                self.direction.y = -1
                self.status = 'up'
            elif rand == 1:
                self.direction.y = 1
                self.status = 'down'

            if rand == 2:
                self.direction.x = 1
                self.status = 'right'
            elif rand == 3:
                self.direction.x = -1
                self.status = 'left'

            self.time_elapsed = 0

        if self.curr_x - self.pos.x >= 32 or self.curr_x - self.pos.x <= -32:
            self.direction.x = 0
            self.curr_x = self.pos.x
            self.moves += 1
            print("moves: " + str(self.moves))
            print("time: " + str(self.game_time))

        if self.curr_y - self.pos.y >= 32 or self.curr_y - self.pos.y <= -32:
            self.direction.y = 0
            self.curr_y = self.pos.y
            self.moves += 1
            print("moves: " + str(self.moves))
            print("time: " + str(self.game_time))

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        #self.input()
        self.get_status()
        self.game_time += dt

        self.move_randomly(dt)
        self.move(dt)
        self.animate(dt)
