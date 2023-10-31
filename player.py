from settings import *
import pygame as pg
import math
import sys


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        pg.mouse.set_visible(False)  # Hide the mouse cursor
        pg.event.set_grab(True)  # Keep the mouse inside the game window

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        #self.x += dx
        #self.y += dy
        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        # Add mouse controls for rotation
        rel_x, rel_y = pg.mouse.get_rel()  # get relative mouse movement
        self.angle += rel_x * MOUSE_SENSITIVITY  # Adjust this value for your needs

        self.angle %= math.tau

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_e:
                self.player.interact()

    def check_wall(self, x, y):
        return (x,y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
                self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
                self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #             (self.x * 100 + WIDTH * math.cos(self.angle),
        #              self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def interact(self):
        # Check the tile in front of the player
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        check_distance = 0.5  # Adjust based on your liking
        x_check = self.x + check_distance * cos_a
        y_check = self.y + check_distance * sin_a

        tile_check = int(x_check), int(y_check)

        if tile_check in self.game.map.world_map:
            tile_value = self.game.map.world_map[tile_check]
            if tile_value == 2:  # It's a door
                self.game.map.toggle_door(tile_check)




    def update (self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
