from ast import literal_eval as make_tuple
import json
import cv2

from cv_button import Button
from constants import QWERTY_PATH


class Keyboard:
    def __init__(self,
                 size: float = 100,
                 position: tuple = (200, 450)):
        self._size = size  # Size of each key
        self._position = position  # Position of centroid of Q
        self._keyboard_buttons = self.set_keyboard()  # Dictionary of buttons

    def set_keyboard(self) -> dict:
        """Initializes buttons using the JSON file with the hard-coded values.

        Args:
            None

        Returns:l
            A dictionary of buttons where the key is the letter and 
                the items is the Button object.
        """
        # Read in from the JSON file
        with open(QWERTY_PATH, 'r') as f:
            keyboard = json.load(f)
        # Initialize the dictionary of buttons
        keyboard_buttons = {}
        assert self.get_size() % 2 == 0
        half_size = self.get_size() / 2
        x_offset, y_offset = self.get_position()
        for key, coords in keyboard.items():
            (x, y) = make_tuple(coords)
            x *= self.get_size()
            y *= self.get_size()
            top_left = (int(x - half_size + x_offset),
                        int(y - half_size + y_offset))
            bottom_right = (int(x + half_size + x_offset),
                            int(y + half_size + y_offset))
            coords = top_left + bottom_right
            keyboard_buttons[key] = Button(coords=coords,
                                           text=key)
        return keyboard_buttons

    def get_size(self) -> float:
        return self._size

    def get_position(self) -> tuple:
        return self._position

    def update(self, coords: tuple) -> None:
        for key, b in self._keyboard_buttons.items():
            b.update(coords)

    def draw(self, img: cv2.UMat) -> cv2.UMat:
        for key, b in self._keyboard_buttons.items():
            img = b.draw(img)
        return img
