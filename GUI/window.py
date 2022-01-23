import arcade


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, True)
        self.set_location(200, 200)
        self.background = arcade.load_texture("suma.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background)
        


if __name__ == '__main__':
    Window(1000, 700, "Main window")
    arcade.run()