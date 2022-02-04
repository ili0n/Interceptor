import arcade
import arcade.gui
# import lead_window
import pathGenerator
import numpy as np
import enemy_projectile
import player_projectile
import target


class RunButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print("run")


def generate_xy_input(label_text, x_input_text, y_input_text):
    box = arcade.gui.UIBoxLayout(vertical=False)

    # add label
    label = arcade.gui.UILabel(text=label_text, anchor_x="left", width=200, font_size=15)
    box.add(label.with_space_around(0, 10, 0, 10))
    # add x input
    input_x = arcade.gui.UIInputText(
        text=x_input_text,
        width=100,
    )
    box.add(input_x.with_space_around(0, 30, 0, 30).with_border(2, (30, 40, 50)))
    # add y input
    input_y = arcade.gui.UIInputText(
        text=y_input_text,
        width=100,
    )
    box.add(input_y.with_space_around(0, 30, 0, 30).with_border(2, (30, 40, 50)))
    return box, label, input_x, input_y


class LeadInputView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.component_height = 40

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_show_view(self):
        self.setup()

    def setup(self):
        # Set background color
        # arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        arcade.set_viewport(0, 800 - 1, 0, 600 - 1)

        # adding labels
        self.rows = arcade.gui.UIBoxLayout()

        self.start_box, self.position_start_label, self.start_input_x, self.start_input_y = generate_xy_input("Start position: ", "X for start", "Y for start")
        self.rows.add(self.start_box)


        # inputs for middle dot
        self.middle_box, self.position_middle_label, self.middle_input_x, self.middle_input_y = generate_xy_input("Middle position", "X for middle", "Y for middle")
        self.rows.add(self.middle_box)

        # inputs for end dot
        self.end_box, self.position_end_label, self.end_input_x, self.end_input_y = generate_xy_input("End position: ", "X for end", "Y for end")
        self.rows.add(self.end_box)
        # buttons

        self.buttons = arcade.gui.UIBoxLayout(vertical=False)

        # submit button
        submit_btn = arcade.gui.UIFlatButton(text="Submit", width=200, anchor_x="left")

        @submit_btn.event("on_click")
        def on_click_submit_btn(event):
            print("Submited successfully")
            print("Start: ({0}, {1})".format(self.start_input_x.text, self.start_input_y.text))
            print("Middle: ({0}, {1})".format(self.middle_input_x.text, self.middle_input_y.text))
            print("End: ({0}, {1})".format(self.end_input_x.text, self.end_input_y.text))
            # arcade.get_window().current_view.manager.disable()
            # arcade.get_window().clear()
            # pg = pathGenerator.PathGenerator()
            # path = pg.generate_enemy_path(np.array([500, 800]))
            #
            # enemy = enemy_projectile.EnemyProjectile(path)
            # enemy.sprite = arcade.sprite.Sprite("resources/enemy.png", 0.05)
            #
            # trgt = target.Target(pg.enemy_target)
            # trgt.sprite = arcade.sprite.Sprite("resources/lab.png", trgt.scale)
            #
            # friendly = player_projectile.PlayerProjectile(pg.enemy_target + np.array([300, 300]))
            # friendly.sprite = arcade.sprite.Sprite("resources/player.png", 0.05)
            # # TODO
            # lead_view = lead_window.LeadView(1500, 1000, "Lead", enemy, trgt, friendly)
            # arcade.get_window().show_view(lead_view)

        self.submit_btn = submit_btn
        self.buttons.add(self.submit_btn.with_space_around(30, 30, 30, 30))

        # text reset button
        reset_btn = arcade.gui.UIFlatButton(text="Reset", width=200)
        @reset_btn.event("on_click")
        def on_click_reset_btn(event):
            self.start_input_x.text = ""
            self.start_input_y.text = ""
            self.middle_input_x.text = ""
            self.middle_input_y.text = ""
            self.end_input_x.text = ""
            self.end_input_y.text = ""
            print("Reset called")
        self.reset_btn = reset_btn
        self.buttons.add(self.reset_btn)
        self.rows.add(self.buttons)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.rows.with_border(2, (20, 30, 40)))
        )
        self.manager.enable()

