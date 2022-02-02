"""
Example code showing how to create a button,
and the three ways to process button events.
"""
import arcade
import arcade.gui

# --- Method 1 for handling click events,
# Create a child class.
from GUI import pure_input_view


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class PureButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        # arcade.exit()
        # arcade.set_window(pure_input_window.PureInputWindow())
        # arcade.close_window()
        # pure_input_window.PureInputWindow()
        # arcade.close_window()
        arcade.get_window().clear()
        pure_view = pure_input_view.PureInputView()
        arcade.get_window().show_view(pure_view)


class LeadButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass
    # TODO pure run

class MainInputView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Again, method 1. Use a child class to handle events.
        pure_button = PureButton(text="Pure pursuit (heatseeking)", width=200).with_space_around(bottom=20)
        self.v_box.add(pure_button)

        lead_button = LeadButton(text="Lead collision (interceptor)", width=200).with_space_around(bottom=20)
        self.v_box.add(lead_button)

        quit_button = QuitButton(text="Quit", width=200).with_space_around(bottom=20)
        self.v_box.add(quit_button)


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()



class MainInputWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "UIFlatButton Example", resizable=True)
        main_view = MainInputView()
        self.show_view(main_view)




