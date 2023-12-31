import numpy as np
import math
import cv2
from utilities import time_utils, cv_draw_utils


def indexThumbTouch(img: np.ndarray, thumb_cords: tuple, index_cords: tuple, TOUCH_DIST_THRESHOLD: int = 30, show_gesture: bool = False):
    """
        # `indexThumbTouch()` Function

        This function returns True when your index finger and thumb touches. False otherwise.

        ## Parameters guidance

        - img: An img from `cap.read()`
        - thumb_cords: A 2-value tuple that represents the coordinates of your thumb.
        - index_cords: A 2-value tuple that represents the coordinates of your index.
        - TOUCH_DIST_THRESHOLD: Constant value that represents the accepted distance to consider your index finger and thumb are touching each other.
        - show_gesture: A boolean value to activate a load circle. Default value set to True.
    """
    x1, y1 = thumb_cords[1], thumb_cords[2]
    x2, y2 = index_cords[1], index_cords[2] 
    x_md, y_md = (x1 + x2)//2, (y1 + y2)//2
    

    length = round(math.hypot((x1 - x2), (y1 - y2)), 3)
    if length < TOUCH_DIST_THRESHOLD:
        if show_gesture:
            cv2.circle(img, (x_md, y_md), 5, (0, 255, 0), cv2.FILLED)
        return True
    return False


def indexThumbTouching(img: np.ndarray, thumb_cords: tuple, index_cords: tuple, timer: time_utils.Timer, c_time: bool, wait_time: int = 3, show_gesture: bool = True):
    """
        # `indexThumbTouching()` Function

        This function returns True when you are touching (for a set number of seconds) your index finger and thumb together. False otherwise.

        ## Parameters guidance

        - img: An img `from cap.read()`
        - thumb_cords: A 2-value tuple that represents the coordinates of your thumb.
        - index_cords: A 2-value tuple that represents the coordinates of your index.
        - timer: An instance of `time_utils.Timer`
        - c_time: A real value number obtained from `time.time()` (time module). Required for the `time_utils.startTimer()` method.
        - wait_time: An integer representing the number of seconds to wait until return True. Default value set to 3.
        - show_gesture: A boolean value to activate a load circle. Default value set to True.
    """

    remaining_time = timer.startTimer(c_time, wait_time, return_elapsed_time=True)
    if remaining_time == True:
        timer.stopTimer()
        return True
    
    if show_gesture:
        x1, y1 = thumb_cords[1], thumb_cords[2]
        x2, y2 = index_cords[1], index_cords[2] 
        x_md, y_md = (x1 + x2)//2, (y1 + y2)//2
        cv_draw_utils.getLoadCircle(img, remaining_time, [0, 3], False, (x_md, y_md), 15, (110, 110, 250), (48, 88, 42), 3, False, False)

    return False