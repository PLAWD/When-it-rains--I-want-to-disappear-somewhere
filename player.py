from settings import *
import pygame as pg
import math
import sys


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.sprint_speed = PLAYER_SPEED * 2  # Sprint speed is twice the normal speed
        self.is_sprinting = False
        self.stamina = 500  # Maximum stamina
        self.stamina_depletion_rate = 1  # Stamina depletion rate per frame
        self.stamina_recovery_rate = 0.5  # Stamina recovery rate per frame

        pg.mouse.set_visible(False)  # Hide the mouse cursor
        pg.event.set_grab(True)  # Keep the mouse inside the game window

    def movement(self):
        self.is_moving = False

        # Basic speed setup
        speed = PLAYER_SPEED
        keys = pg.key.get_pressed()

        # Check for sprinting
        self.is_sprinting = keys[pg.K_LSHIFT] and self.stamina > 0
        if self.is_sprinting:
            speed = self.sprint_speed

        # Apply delta time
        speed *= self.game.delta_time

        # Movement calculations
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0

        if keys[pg.K_w]:
            dx += speed * cos_a
            dy += speed * sin_a
        if keys[pg.K_s]:
            dx -= speed * cos_a
            dy -= speed * sin_a
        if keys[pg.K_d]:
            dx -= speed * sin_a
            dy += speed * cos_a
        if keys[pg.K_a]:
            dx += speed * sin_a
            dy -= speed * cos_a

        # Set moving status
        if dx != 0 or dy != 0:
            self.is_moving = True

        # Update stamina
        if self.is_sprinting:
            self.stamina -= self.stamina_depletion_rate
            self.stamina = max(0, self.stamina)  # Prevent negative stamina
        elif self.stamina < 100:
            self.stamina += self.stamina_recovery_rate
            self.stamina = min(100, self.stamina)  # Cap stamina at 100

        # Collision and position update
        self.check_wall_collision(dx, dy)





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
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
                self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
                self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #             (self.x * 100 + WIDTH * math.cos(self.angle),
        #              self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

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
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
