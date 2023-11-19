from sprite_object import *
import settings

class Hand(AnimatedSprite):
    def __init__(self, game, path='GameForIA/resources/sprites/hand/lamp/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])

        # Use HALF_WIDTH and HEIGHT from settings
        self.hand_pos = (settings.HALF_WIDTH - self.images[0].get_width() // 2,
                         settings.HEIGHT - self.images[0].get_height())
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.current_frame_time = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.hand_pos)

    def update(self):
        # Update the frame based on the animation time, using delta_time from the game
        self.current_frame_time += self.game.delta_time
        if self.current_frame_time >= self.animation_time:
            self.current_frame_time = 0
            self.images.rotate(-1)  # Move to the next frame
            self.frame_counter = (self.frame_counter + 1) % self.num_images
