import pygame as pg
import settings
from sprite_object import AnimatedSprite
import math
from collections import deque

class Hand(AnimatedSprite):
    def __init__(self, game, path='GameForIA/resources/sprites/hand/lamp/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.base_hand_pos = (settings.HALF_WIDTH - self.images[0].get_width() // 2,
                              settings.HEIGHT - self.images[0].get_height())
        self.hand_sway = 0
        self.sway_speed = 1  # Adjust the sway speed as needed
        self.sway_amount = 50  # Adjust how much the hand sways
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.current_frame_time = 0

    def update(self):
        # Update the frame based on the animation time
        self.current_frame_time += self.game.delta_time
        if self.current_frame_time >= self.animation_time:
            self.current_frame_time = 0
            self.images.rotate(-1)  # Move to the next frame
            self.frame_counter = (self.frame_counter + 1) % self.num_images

        # Update hand sway based on player movement
        if self.game.player.is_moving:  # Assuming you have a way to determine if the player is moving
            self.hand_sway = math.sin(pg.time.get_ticks() * 0.005 * self.sway_speed) * self.sway_amount
        else:
            self.hand_sway = 0

        self.hand_pos = (self.base_hand_pos[0] + self.hand_sway, self.base_hand_pos[1])

    def draw(self):
        self.game.screen.blit(self.images[0], self.hand_pos)
