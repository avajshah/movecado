"""Button class

This class is an abstraction for a button

http://kiranthepro.epizy.com/projects/flappy_bird/?i=1 <-- website
"""

import cv2
import logging
import pyautogui


class Button:
    def __init__(self,
                 color: tuple = (128, 0, 128),
                 coords: tuple = (0, 0, 50, 50),
                 duration: float = 0.1,
                 text: str = "",
                 alpha: float = 0.314,
                 ):
        """
        Args:
            color (tuple): a tuple of (B, G, R)
            coords (tuple): a tuple of (x_min, y_min, x_max, y_max)
            duration (float): duration (in ms) needed for button to be selected

        Returns:
            None
        """
        self._color = color
        self._coords = coords
        self._duration = duration
        self._default_alpha = alpha  # 0 is transparent; 1 is opaque
        self._text = text

        self.alpha = alpha  # 0 is transparent; 1 is opaque
        self.is_selected = False
        self.toggled = False
        self.time = 0

    def __str__(self) -> str:
        return (f"Button:\n"
                f"Color: {self._color}\n"
                f"Coordinates: {self._coords}\n"
                f"Duration: {self._duration} ms\n"
                f"Alpha: {self.alpha}\n"
                f"Is Selected: {self.is_selected}\n"
                f"Time: {self.time}\n"
                f"Text: {self._text}\n")

    def update(self, coords: tuple) -> None:
        # Default selected state is false
        self.is_selected = False
        (x, y) = coords
        top_left_x, top_left_y = self.top_left()
        bottom_right_x, bottom_right_y = self.bottom_right()
        # If the cursor (hand landmark) is within the button
        if top_left_x <= x <= bottom_right_x and top_left_y <= y <= bottom_right_y:
            # Update time and progress
            self.time += 1
            self.time = max(0, min(self.time, self._duration))
            progress = self.time / self._duration
            # linear interpolation
            self.alpha = self._default_alpha + \
                (1 - self._default_alpha) * progress
            # Reach duration
            if self.time == self._duration:
                # Set selected to true only if it hasn't been toggled yet
                if not self.toggled:
                    self.toggled = True
                    self.is_selected = True
                    logging.getLogger("movementum").info(f"{self}")
                    # actually do the clicking
                    if self._text == 'UP':
                        pyautogui.press('up')
                    #if self._text == 'DOWN':
                        #pyautogui.press('down')
                    if self._text == 'LEFT':
                        pyautogui.press('left')
                    if self._text == 'RIGHT':
                        pyautogui.press('right')
                    if self._text == 'SPACE':
                        pyautogui.press('space')
                if self.toggled:
                    self.alpha = self._default_alpha
        # Otherwise reset
        else:
            self.alpha = self._default_alpha
            self.time = 0
            self.toggled = False

    def draw(self, img: cv2.UMat) -> cv2.UMat:
        # Add rectangle
        overlay = img.copy()
        cv2.rectangle(overlay, self.top_left(), self.bottom_right(),
                      self.get_color(), cv2.FILLED)
        img = cv2.addWeighted(overlay, self.get_alpha(),
                              img, 1-self.get_alpha(), 0)
        # Draw the key letter on top of the box
        key_label_position = (self.get_center()[0] - 10,
                              self.get_center()[1] + 10)
        cv2.putText(img, self.get_text(), key_label_position,
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img

    def top_left(self) -> tuple:
        """Returns the coordinate of the top left corner of the button
        """
        return (self._coords[0], self._coords[1])

    def bottom_right(self) -> tuple:
        """Returns the coordinate of the bottom right corner of the button
        """
        return (self._coords[2], self._coords[3])

    def get_center(self) -> tuple:
        """Returns the coordinate of the center of the button
        """
        a, b = self.top_left()
        c, d = self.bottom_right()
        return ((a + c) // 2, (b + d) // 2)

    def get_color(self) -> tuple:
        return self._color

    def get_alpha(self) -> tuple:
        return self.alpha

    def get_text(self) -> str:
        return self._text
