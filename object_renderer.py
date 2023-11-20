import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.ceiling_image = self.get_texture('GameForIA/resources/textures/bubong.png', (WIDTH, HALF_HEIGHT))
        self.floor_image = self.get_texture('GameForIA/resources/textures/boolapag.png', (WIDTH, HALF_HEIGHT)) # Load floor texture
        self.ceiling_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        self.ceiling_offset = (self.ceiling_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.ceiling_image, (-self.ceiling_offset, 0))
        self.screen.blit(self.ceiling_image, (-self.ceiling_offset + WIDTH, 0))
        #FLOOR
        self.screen.blit(self.floor_image, (0, HALF_HEIGHT)) # Draw floor texture

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('GameForIA/resources/textures/1.png'),
            2: self.get_texture('GameForIA/resources/textures/2.png'),
            3: self.get_texture('GameForIA/resources/textures/3.png'),
            4: self.get_texture('GameForIA/resources/textures/4.png'),
            5: self.get_texture('GameForIA/resources/textures/5.png'),
            6: self.get_texture('GameForIA/resources/textures/5.png'),
        }
