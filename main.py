from time import sleep

import arcade


# Press the green button in the gutter to run the script.
import numpy as np

from GUI import main_input_window, lead_window
from GUI import pure_input_view


if __name__ == '__main__':
    lead_window.LeadWindow(1500, 1000, "Lead", np.array([0,0]), np.array([1000,0]), np.array([1000,800]))
    main_input_window.MainInputWindow()
    # pure_input_window.PureInputWindow()
    arcade.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
