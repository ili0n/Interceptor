import arcade
import numpy as np

import pathGenerator
import projectile


class PureWindow(arcade.Window):

    def __init__(self, width, height, title, enemy):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        self._enemy = enemy
        self._player = player
        # Loading the background image
        self.background = None
        self.sprites_list = arcade.SpriteList()
        self.sprites_list.append(enemy.sprite)
        self.sprites_list.append(player.sprite)

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width,
                                      self.height, arcade.load_texture("resources/suma.png"))


if __name__ == '__main__':
    pg = pathGenerator.PathGenerator()
    path = pg.generate_enemy_path(np.array([500, 500]))
    enemy = projectile.Projectile(path)
    enemy.sprite = arcade.sprite.Sprite("resources/enemy.png")

    PureWindow(1500, 1000, "pure", enemy)

arcade.run()
