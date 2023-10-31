import pygame as pg
from settings import *

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1, _, 1, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        self.doors = {}  # {position: (state, timer)}

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        for pos, value in self.world_map.items():
            if value == 2:  # if it's a door
                pg.draw.rect(self.game.screen, 'blue', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
            else:
                pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)

    def toggle_door(self, pos):
        if pos not in self.doors:
            self.doors[pos] = ("opening", 0)
        else:
            state, _ = self.doors[pos]
            self.doors[pos] = ("closing" if state == "opening" else "opening", 0)

    def update_doors(self):
        to_remove = []
        for pos, (state, timer) in self.doors.items():
            if state == "opening":
                timer += DOOR_SPEED
                if timer >= 1:
                    self.mini_map[pos[1]][pos[0]] = _  # open the door
                    to_remove.append(pos)
            elif state == "closing":
                timer -= DOOR_SPEED
                if timer <= 0:
                    self.mini_map[pos[1]][pos[0]] = 2  # close the door
                    to_remove.append(pos)
            self.doors[pos] = (state, timer)

        for pos in to_remove:
            del self.doors[pos]
