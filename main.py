import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from hand import*



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

        # Stamina bar properties
        self.stamina_bar_width = 200
        self.stamina_bar_height = 20
        self.stamina_bar_position = (50, 550)  # Example position, adjust as needed
        self.stamina_color = (0, 255, 0)  # Green color
        self.stamina_bg_color = (255, 0, 0)  # Red color

    def draw_stamina_bar(self, current_stamina):
        # Draw the background of the stamina bar
        pg.draw.rect(self.screen, self.stamina_bg_color,
                         (*self.stamina_bar_position, self.stamina_bar_width, self.stamina_bar_height))

        # Calculate the width of the foreground based on current stamina
        foreground_width = (current_stamina / 100) * self.stamina_bar_width  # Assuming max stamina is 100

        # Draw the foreground of the stamina bar
        pg.draw.rect(self.screen, self.stamina_color,
                         (*self.stamina_bar_position, foreground_width, self.stamina_bar_height))

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.hand = Hand(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.hand.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.hand.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.draw_stamina_bar(self.player.stamina)  # Pass the player's current stamina
            pg.display.flip()
            self.clock.tick(60)  # Assuming you have a clock for FPS control


if __name__ == '__main__':
    game = Game()
    game.run()
