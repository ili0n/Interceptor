import arcade
import numpy as np

import SAT
import pathGenerator
import enemy_projectile
import player_projectile
import target
import lead_collision


class LeadWindow(arcade.Window):

    def __init__(self, width, height, title, enemy, target, friendly):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        self._enemy = enemy
        self._target = target
        self._friendly = friendly
        # self._player = player
        # Loading the background image
        self.background = None
        self.sprites_list = arcade.SpriteList()
        self.sprites_list.append(enemy.sprite)
        self.sprites_list.append(target.sprite)
        self.sprites_list.append(friendly.sprite)
        # self.sprites_list.append(player.sprite)
        self.set_update_rate(1 / 60)
        self._counter = 0
        # self.begining_vertices = self._friendly.polygon.vertices.copy()

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing the background image
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width,
                                      self.height, arcade.load_texture("GUI/resources/suma.png"))
        # for i in self._friendly.polygon.vertices:
        #     arcade.draw_circle_filled(i[0], i[1], 2, arcade.color.BLACK)
        # for i in self.begining_vertices:
        #     arcade.draw_circle_filled(i[0], i[1], 2, arcade.color.BLACK)
        # for i in self._enemy.polygon.vertices:
        #     arcade.draw_circle_filled(i[0], i[1], 2, arcade.color.BLACK)
        # r1, r2, center, result, movement = self._friendly.plot(self._enemy)
        # result = result / np.linalg.norm(result) * 100 + self._friendly.point
        # arcade.draw_circle_filled(center[0], center[1], 10, arcade.color.BLACK)
        # arcade.draw_circle_filled(result[0], result[1], 10, arcade.color.BLACK)


        # arcade.draw_line(self._friendly.polygon.vertices[0], self._friendly.polygon.vertices[1],   2, arcade.color.BLACK)
        self.sprites_list.draw()

    def on_update(self, delta_time: float):
        arcade.start_render()
        self._counter += delta_time
        self._enemy.calculate_distance(self._counter)
        self._enemy.sprite.set_position(self._enemy.point[0], self._enemy.point[1])

        self._friendly.calculate_distance(self._counter, self._enemy)
        self._friendly.sprite.set_position(self._friendly.point[0], self._friendly.point[1])

        print((180 / np.pi) * (self._enemy.angle2 - self._enemy.previous_angle2))
        self.sprites_list[0].turn_left((180 / np.pi) * (self._enemy.angle1 - self._enemy.previous_angle1))

        self.sprites_list[2].turn_left((180 / np.pi) * (self._friendly.angle1 - self._friendly.previous_angle1))
        # self._friendly.plot(self._enemy)

        if SAT.is_colliding(self._enemy.polygon, self._target.polygon) or SAT.is_colliding(self._enemy.polygon,
                                                                                           self._friendly.polygon):
            arcade.pause(3)
            arcade.exit()

        self.sprites_list.update()

# uglovi da se podese na 90 i da se makne angle2
if __name__ == '__main__':
    pg = pathGenerator.PathGenerator()
    path = pg.generate_enemy_path(np.array([500, 800]))

    enemy = enemy_projectile.EnemyProjectile(path)
    enemy.sprite = arcade.sprite.Sprite("resources/enemy.png", 0.05)

    trgt = target.Target(pg.enemy_target)
    trgt.sprite = arcade.sprite.Sprite("resources/lab.png", trgt.scale)

    friendly = player_projectile.PlayerProjectile(np.array([1000, 800]))
    friendly.sprite = arcade.sprite.Sprite("resources/player.png", 0.05)

    LeadWindow(1500, 1000, "Lead", enemy, trgt, friendly)

    arcade.run()
