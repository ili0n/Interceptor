import arcade
import arcade.gui


class RunButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.get_window().current_view.manager.disable()



class PureInputView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        # arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # arcade.set_viewport(0, 800 - 1, 0, 600 - 1)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        player_x_input = arcade.gui.UIInputText(text="Player X coordinate", width=400).with_space_around(bottom=20)
        self.v_box.add(player_x_input)
        player_y_input = arcade.gui.UIInputText(text="Player Y coordinate", width=400).with_space_around(bottom=20)
        self.v_box.add(player_y_input)
        projectile_x_input = arcade.gui.UIInputText(text="Projectile X coordinate", width=400).with_space_around(
            bottom=20)
        self.v_box.add(projectile_x_input)
        projectile_y_input = arcade.gui.UIInputText(text="Player Y coordinate", width=400).with_space_around(bottom=20)
        self.v_box.add(projectile_y_input)
        player_speed_input = arcade.gui.UIInputText(text="Player speed", width=400).with_space_around(bottom=20)
        self.v_box.add(player_speed_input)

        run_button = RunButton(text="Run", width=400).with_space_around(bottom=20)
        self.v_box.add(run_button)
        # Again, method 1. Use a child class to handle events.

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.manager.draw()

    def on_show_view(self):
        arcade.start_render()
