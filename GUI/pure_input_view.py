import arcade
import arcade.gui
import player
import pure_pursuit_projectile
import GUI.pure_window as pure_window
import numpy as np


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
        width=230,
    )
    box.add(input_x.with_space_around(0, 30, 0, 30).with_border(2, (30, 40, 50)))
    # add y input
    input_y = arcade.gui.UIInputText(
        text=y_input_text,
        width=230,
    )
    box.add(input_y.with_space_around(0, 30, 0, 30).with_border(2, (30, 40, 50)))
    return box, label, input_x, input_y


class PureInputView(arcade.View):
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
        arcade.set_viewport(0, 800 - 1, 0, 600 - 1)

        # adding labels
        self.rows = arcade.gui.UIBoxLayout()


        # input of ship start dot
        self.ship_start_box, self.ship_start_label, self.ship_start_input_x, self.ship_start_input_y = generate_xy_input(
            "Ship start position: ", "X for ship start", "Y for ship start")
        self.rows.add(self.ship_start_box)

        # input of start dot
        self.projectile_start_box, self.projectile_start_label, self.projectile_start_input_x, self.projectile_start_input_y = generate_xy_input(
            "Projectile start position: ", "X for projectile start", "Y for projectile start")
        self.rows.add(self.projectile_start_box)

        self.velocity_box = arcade.gui.UIBoxLayout(vertical=False)
        self.velocity_label = arcade.gui.UILabel(text="Velocity: ", anchor_x="left", width=200, font_size=15)
        self.velocity_box.add(self.velocity_label.with_space_around(0, 10, 0, 10))
        self.velocity_input = arcade.gui.UIInputText(
            text="Velocity value",
            width=230,
        )
        self.velocity_box.add(self.velocity_input.with_space_around(0, 30, 0, 30).with_border(2, (30, 40, 50)))
        self.rows.add(self.velocity_box)

        self.look_ahead_box = arcade.gui.UIBoxLayout(vertical=False)
        self.look_ahead_label = arcade.gui.UILabel(text="Look ahead: : ", anchor_x="left", width=200, font_size=15)
        self.look_ahead_box.add(self.look_ahead_label.with_space_around(0, 10, 0, 10))
        self.look_ahead_input = arcade.gui.UIInputText(
            text="Look ahead distance value",
            width=230,
        )
        self.look_ahead_box.add(self.look_ahead_input.with_space_around(0, 30, 0, 30).with_border(2, (30, 40, 50)))
        self.rows.add(self.look_ahead_box)

        self.buttons = arcade.gui.UIBoxLayout(vertical=False)
        # submit button
        submit_btn = arcade.gui.UIFlatButton(text="Submit", width=200, anchor_x="left")

        @submit_btn.event("on_click")
        def on_click_submit_btn(event):
            print("Submited successfully")
            print("Ship start: ({0}, {1})".format(self.ship_start_input_x.text, self.ship_start_input_y.text))
            print("Projectile start: ({0}, {1})".format(self.projectile_start_input_x.text, self.projectile_start_input_y.text))
            print("Velocity: {0}".format(self.velocity_input.text))
            print("Look ahead distance: {0}".format(self.look_ahead_input.text))
            if not is_int(self.ship_start_input_x.text) or not is_int(self.ship_start_input_y.text)\
                    or not is_int(self.projectile_start_input_x.text) or not is_int(self.projectile_start_input_y.text) \
                    or not is_int(self.velocity_input.text) or not is_int(self.look_ahead_input.text):
                return None
            arcade.get_window().current_view.manager.disable()
            arcade.get_window().clear()
            projectile_start = np.array([int(self.projectile_start_input_x.text), int(self.projectile_start_input_y.text)])
            ship_start = np.array([int(self.ship_start_input_x.text), int(self.ship_start_input_y.text)])


            plr = player.Player(ship_start, int(self.velocity_input.text))
            plr.sprite = arcade.Sprite("GUI/resources/ufo.png", plr.scale)
            pp = pure_pursuit_projectile.PlayerProjectile(projectile_start)
            pp.sprite = arcade.Sprite("GUI/resources/player.png", pp.scale)
            pure_window.PlayerWindow(1500, 1000, "pure", plr, pp)
            arcade.run()

        self.submit_btn = submit_btn
        self.buttons.add(self.submit_btn.with_space_around(30, 30, 30, 30))

        # text reset button
        reset_btn = arcade.gui.UIFlatButton(text="Reset", width=200)
        @reset_btn.event("on_click")
        def on_click_reset_btn(event):
            self.ship_start_input_x.text = ""
            self.ship_start_input_y.text = ""
            self.projectile_start_input_x.text = ""
            self.projectile_start_input_y.text = ""
            self.velocity_input.text = ""
            self.look_ahead_input.text = ""
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

def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False