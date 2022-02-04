import arcade
import arcade.gui


class RunButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print("run")


class LeadInputView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_show_view(self):
        self.setup()

    def setup(self):
        # Set background color
        # arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        arcade.set_viewport(0, 800 - 1, 0, 600 - 1)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # run_button = RunButton().with_space_around(bottom=20)
        # self.v_box.add(run_button)
        # Again, method 1. Use a child class to handle events.
        # quit_button = QuitButton(text="Quit", width=200)
        # self.v_box.add(quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons

        left_column_x = self.window.width // 4
        y_slot = self.window.height // 4

        input_text = arcade.gui.UIInputText(
            anchor_x="left",
            anchor_y="top",
            text="Text",
            width=300
        )
        # input_text.cursor_index = len(input_text.text)
        self.input_text = input_text
        self.v_box.add(self.input_text.with_border(2, (30, 40, 50)))

        ui_flatbutton = arcade.gui.UIFlatButton(text="Reset", width=200)
        self.v_box.add(ui_flatbutton.with_space_around(bottom=20))

        # Handle Clicks
        @ui_flatbutton.event("on_click")
        def on_click_flatbutton(event):
            print("UIFlatButton pressed", event)
            self.input_text.text = ""
            self.manager.draw()
            self.v_box.trigger_render()

        ui_flatbutton1 = arcade.gui.UIFlatButton(text="Reset", width=200)
        self.v_box.add(ui_flatbutton1.with_space_around(bottom=20))

        # Handle Clicks
        @ui_flatbutton1.event("on_click")
        def on_click_flatbutton(event):
            print("UIFlatButton pressed", self.input_text.text)


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.manager.enable()

