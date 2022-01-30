import arcade
import numpy as np

import SAT
import pathGenerator
import enemy_projectile
import player


class PlayerWindow(arcade.Window):

    def __init__(self, width, height, title, player):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        # self._enemy = enemy
        self._player = player
        # Loading the background image
        self.background = None
        self.sprites_list = arcade.SpriteList()
        # self.sprites_list.append(enemy.sprite)
        self.sprites_list.append(player.sprite)
        self.set_update_rate(1 / 60)
        self._counter = 0
        self._player_x_sign = 0
        self._player_y_sign = 0
        self._left = False
        self._right = False
        self._up = False
        self._down = False

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width,
                                      self.height, arcade.load_texture("resources/suma.png"))
        self.sprites_list.draw()

    def on_key_press(self, symbol, modifiers: int):
        if symbol == arcade.key.W:
            self._up = True
        if symbol == arcade.key.S:
            self._down = True
        if symbol == arcade.key.D:
            self._right = True
        if symbol == arcade.key.A:
            self._left = True

    def on_key_release(self, symbol, modifiers: int):
        if symbol == arcade.key.W:
            self._up = False
        if symbol == arcade.key.S:
            self._down = False
        if symbol == arcade.key.D:
            self._right = False
        if symbol == arcade.key.A:
            self._left = False

    def on_update(self, delta_time: float):
        if self._up:
            self._player_y_sign = 1
        if self._down:
            self._player_y_sign = -1
        if self._right:
            self._player_x_sign = 1
        if self._left:
            self._player_x_sign = -1

        if not self._up and not self._down:
            self._player_y_sign = 0
        if not self._left and not self._right:
            self._player_x_sign = 0

        x_move = self._player.speed * self._player_x_sign * delta_time
        y_move = self._player.speed * self._player_y_sign * delta_time

        self._player.move(x_move, y_move)
        self._player.sprite.set_position(self._player.point[0],self._player.point[1])

if __name__ == "__main__":
    plr = player.Player(np.array([800, 800],dtype="f"),250)
    plr.sprite = arcade.Sprite("resources/ufo.png", plr.scale)
    PlayerWindow(1500,1000,"pure",plr)
    arcade.run()


