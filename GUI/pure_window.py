import arcade
import numpy as np

import SAT
import pathGenerator
import enemy_projectile
import player


class PlayerWindow(arcade.Window):

    def __init__(self, width, height, title, enemy, player):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        self._enemy = enemy
        # self._player = player
        # Loading the background image
        self.background = None
        self.sprites_list = arcade.SpriteList()
        self.sprites_list.append(enemy.sprite)
        # self.sprites_list.append(player.sprite)
        self.set_update_rate(1 / 60)
        self._counter = 0

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width,
                                      self.height, arcade.load_texture("resources/suma.png"))
        self.sprites_list.draw()


if __name__ == "__main__":
    plr = player.Player(np.array([800, 800]))
    plr.sprite = arcade.Sprite("resources/ufo.png", plr.scale)

