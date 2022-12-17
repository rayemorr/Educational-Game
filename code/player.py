# file: player.py
# purpose: represents a player that will randomly walk around the grid, staying within the grid's boundaries, until
#          all players are found

import random

from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, width, height, path):
        super().__init__(group)

        self.path = path  # path in files to player sprites

        self.import_assets()  # import player animations
        self.status = 'down_idle'  # set initial status to the idle down position
        self.frame_index = 0  # set initial frame to the first index for the current status

        # general setup
        self.image = self.animations[self.status][self.frame_index]  # set the players current image depending on the
                                                                     # status and frame index
        self.rect = self.image.get_rect(center=pos)  # player's rectangular object

        # movement attributes
        self.direction = pygame.math.Vector2()  # vector representing the direction the player is facing when moving
        self.start_pos = pygame.math.Vector2(pos)  # vector representing the position that the player should start in
        self.pos = pygame.math.Vector2(pos)  # vector representing the current position of the player
        self.speed = 200  # the speed of the player when they are moving

        self.time_elapsed = 0  # this value is used to determine how long it's been since the player last moved

        # these values save the position of the player before moving so that it can be determined how far they've moved
        self.curr_x = self.pos.x
        self.curr_y = self.pos.y

        self.moves = 0  # the amount of moves the player had made before meeting up with another player

        # board width and height is saved to set the boundaries in which the player is allowed to move around and to
        self.board_width = width
        self.board_height = height

        self.found = False  # True when the player has found at least one other player
        self.stop_moving = False  # True when a player is found and not leading another player
        self.lead = False  # True when a player finds another player, and they have the lower number

        self.selected_protocol = 'random'  # what the player's current wandering protocol is
        self.turn = 0  # when using the 'every other' protocol, this value determines whether they move vertically or
                       # horizontally

        self.selected = False  # this value is true when it is the players turn to be placed on the board
        self.placed = False  # if playing the 3-5 or 6-8 levels, this value will stay false until enter is pressed to
                             # place the player on the board
        self.all_placed = False  # this value is set true for all players when self.place is true for all players

        self.move_time = 0  # this value is used to determine how long it's been since the player was last moved by the
                            # user with the arrow keys

    # import player animations
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = self.path + animation
            self.animations[animation] = import_folder(full_path)

    # animate the player by setting the player image depending on their current status and frame index
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    # this will only be used when the user is placing players on the board
    #
    def input(self, dt):
        self.status = 'down_idle'  # set status to default
        self.move_time += dt  # update the move_time with delta time
        keys = pygame.key.get_pressed()  # keeps track of which key is currently being pressed

        # set player position
        if not self.placed:  # only when the player isn't already placed
            if self.move_time > .3:  # time of .3 ensures the player won't move more than one spot at once
                if keys[pygame.K_UP] and self.pos.y != 32:
                    self.pos.y -= 64
                    self.start_pos.y = self.pos.y
                elif keys[pygame.K_DOWN] and self.pos.y != self.board_height - 32:
                    self.pos.y += 64
                    self.start_pos.y = self.pos.y
                elif keys[pygame.K_LEFT] and self.pos.x != 32:
                    self.pos.x -= 64
                    self.start_pos.x = self.pos.x
                elif keys[pygame.K_RIGHT] and self.pos.x != self.board_width - 32:
                    self.pos.x += 64
                    self.start_pos.x = self.pos.x
                elif keys[pygame.K_RETURN]:  # once enter is pressed, the player is placed and no longer selected
                    self.selected = False
                    self.placed = True

                # update the rect position
                self.rect.centerx = self.pos.x
                self.rect.centery = self.pos.y

                # since the player just moved, set this time back to 0
                self.move_time = 0

    # if the player is not moving, set the status to idle in whichever direction they are facing
    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    # 'random' protocol
    # when using this protocol, a random number 0,3 is picked and the player moves in a direction based on the random
    # number that was picked
    def move_randomly(self, dt):
        if not self.stop_moving:  # only do this if the player is placed and not found
            self.time_elapsed += dt
            if self.time_elapsed > 2:
                rand = random.randint(0, 3)

                if rand == 0:
                    # move up unless at the very top of the grid
                    if self.pos.y == 32:
                        self.direction.y = 1
                        self.status = 'down'
                    else:
                        self.direction.y = -1
                        self.status = 'up'
                elif rand == 1:
                    # move down unless at the very bottom of the grid
                    if self.pos.y == self.board_height-32:
                        self.direction.y = -1
                        self.status = 'up'
                    else:
                        self.direction.y = 1
                        self.status = 'down'

                if rand == 2:
                    # move right unless at the very right side of the grid
                    if self.pos.x == self.board_width-32:
                        self.direction.x = -1
                        self.status = 'left'
                    else:
                        self.direction.x = 1
                        self.status = 'right'
                elif rand == 3:
                    # move left unless at the very left side of the grid
                    if self.pos.x == 32:
                        self.direction.x = 1
                        self.status = 'right'
                    else:
                        self.direction.x = -1
                        self.status = 'left'

                self.time_elapsed = 0

    # 'every other' protocol
    # when using this protocol, when the turn is 0, the player will only move vertically, and they will only move
    # horizontally when the turn is 1. the two turns are alternated and both utilize a random number 0 or 1 to determine
    # if the player should move down/left or up/right
    def every_other(self, dt):
        self.time_elapsed += dt
        if self.turn == 0:
            if not self.stop_moving:  # only do this if the player is placed and not found
                if self.time_elapsed > 2:
                    rand = random.randint(0, 1)

                    if rand == 0:
                        # move up unless at the very top of the grid
                        if self.pos.y == 32:
                            self.direction.y = 1
                            self.status = 'down'
                        else:
                            self.direction.y = -1
                            self.status = 'up'
                    elif rand == 1:
                        # move down unless at the very bottom of the grid
                        if self.pos.y == self.board_height-32:
                            self.direction.y = -1
                            self.status = 'up'
                        else:
                            self.direction.y = 1
                            self.status = 'down'
                    self.time_elapsed = 0
                    self.turn = 1
        if self.turn == 1:
            if not self.stop_moving:
                if self.time_elapsed > 2:
                    rand = random.randint(0, 1)

                    if rand == 0:
                        # move right unless at the very right side of the grid
                        if self.pos.x == self.board_width - 32:
                            self.direction.x = -1
                            self.status = 'left'
                        else:
                            self.direction.x = 1
                            self.status = 'right'
                    elif rand == 1:
                        # move left unless at the very left side of the grid
                        if self.pos.x == 32:
                            self.direction.x = 1
                            self.status = 'right'
                        else:
                            self.direction.x = -1
                            self.status = 'left'
                    self.time_elapsed = 0
                    self.turn = 0

    # when the random protocols set the direction and status of the player, this is used to actually move the player,
    # which only moves 64 pixels at once
    def move(self, dt):
        # moving left
        if self.curr_x - self.pos.x >= 64:
            self.pos.x = self.curr_x - 64
            self.direction.x = 0
            self.curr_x = self.pos.x
            if not self.found:  # increase moves as long as the player isn't found
                self.moves += 1
            if self.found and not self.lead:
                self.stop_moving = True  # stop moving when the player is found and not leading another player

        # moving right
        if self.curr_x - self.pos.x <= -64:
            self.pos.x = self.curr_x + 64
            self.direction.x = 0
            self.curr_x = self.pos.x
            if not self.found:  # increase moves as long as the player isn't found
                self.moves += 1
            if self.found and not self.lead:
                self.stop_moving = True  # stop moving when the player is found and not leading another player

        # moving up
        if self.curr_y - self.pos.y >= 64:
            self.pos.y = self.curr_y - 64
            self.direction.y = 0
            self.curr_y = self.pos.y
            if not self.found:  # increase moves as long as the player isn't found
                self.moves += 1
            if self.found and not self.lead:
                self.stop_moving = True  # stop moving when the player is found and not leading another player

        # moving down
        if self.curr_y - self.pos.y <= -64:
            self.pos.y = self.curr_y + 64
            self.direction.y = 0
            self.curr_y = self.pos.y
            if not self.found:  # increase moves as long as the player isn't found
                self.moves += 1
            if self.found and not self.lead:
                self.stop_moving = True  # stop moving when the player is found and not leading another player

        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    # reset the player to their default settings and starting position
    def reset(self):
        self.direction.x = 0
        self.direction.y = 0
        self.status = 'down_idle'
        self.time_elapsed = 0

        self.found = False
        self.stop_moving = False
        self.lead = False

        self.pos.x = self.start_pos.x
        self.rect.centerx = self.start_pos.x
        self.pos.y = self.start_pos.y
        self.rect.centery = self.start_pos.y
        self.curr_x = self.pos.x
        self.curr_y = self.pos.y

        self.moves = 0

    # the player will move with the same direction, status, and position of the player provided
    def follow(self, player):
        self.direction.x = player.direction.x
        self.direction.y = player.direction.y
        self.status = player.status
        self.pos.x = player.pos.x
        self.pos.y = player.pos.y

    # this is continuously run to update player variables
    def update(self, dt):
        self.get_status()
        self.animate(dt)

        if self.placed and self.all_placed:  # once all players have been placed, the player will start moving
                                             # depending on the selected protocol
            self.move(dt)
            if self.selected_protocol == 'random':
                self.move_randomly(dt)
            if self.selected_protocol == 'every other':
                self.every_other(dt)
        elif self.selected:  # if the player is not placed and is currently selected, the user will be able to move them
            self.input(dt)
