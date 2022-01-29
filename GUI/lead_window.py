import arcade
import numpy as np

import SAT
import pathGenerator
import enemy_projectile
import target


class PureWindow(arcade.Window):

    def __init__(self, width, height, title, enemy,target):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        self._enemy = enemy
        self._target = target
        # self._player = player
        # Loading the background image
        self.background = None
        self.sprites_list = arcade.SpriteList()
        self.sprites_list.append(enemy.sprite)
        self.sprites_list.append(target.sprite)
        # self.sprites_list.append(player.sprite)
        self.set_update_rate(1/60)
        self._counter = 0

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width,
                                      self.height, arcade.load_texture("resources/suma.png"))
        self.sprites_list.draw()

    def on_update(self, delta_time: float):
        self._counter += delta_time
        self._enemy.calculate_distance(self._counter)
        self._enemy.sprite.set_position(self._enemy.point[0],self._enemy.point[1])
        # self.
        print((180/np.pi) * (self._enemy.angle2 - self._enemy.previous_angle2))
        self.sprites_list[0].turn_right ((180/np.pi)*abs((self._enemy.angle2 - self._enemy.previous_angle2)))
        self.sprites_list.update()
        if SAT.is_colliding(self._enemy.polygon,self._target.polygon):
            arcade.exit()
            #TODO add game over message


if __name__ == '__main__':
    pg = pathGenerator.PathGenerator()
    path = pg.generate_enemy_path(np.array([500, 800]))
    enemy = enemy_projectile.EnemyProjectile(path)
    enemy.sprite = arcade.sprite.Sprite("resources/enemy.png",0.05)
    trgt = target.Target(pg.enemy_target)
    trgt.sprite = arcade.sprite.Sprite("resources/lab.png",trgt.scale)


    PureWindow(1500, 1000, "pure", enemy,trgt)

arcade.run()
