import cv2
import numpy as np
import math
from utilities import time_utils, cv_draw_utils
# Audio imports
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControllerFeature():
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.volume_range = self.volume.GetVolumeRange()

        self.active = False


    def __setVolume(self, vol: int):
        """
            Todo
        """

        self.volume.SetMasterVolumeLevel(vol, None)


    def runVolumeController(self, img: np.ndarray, thumb_cords: tuple, index_cords: tuple, timer: time_utils.Timer, c_time: bool, wait_time: int = 3):
        """
            Todo
        """

        # Timer until controller is deactivated
        remaining_time = timer.startTimer(c_time, wait_time, return_elapsed_time=True)
        if remaining_time == True:
            timer.resetTimer()
            self.active = False
        
        x1, y1 = thumb_cords[1], thumb_cords[2]
        x2, y2 = index_cords[1], index_cords[2]

        # CV drawings
        color = cv_draw_utils.colorTransition(remaining_time, [0, 3], False, (0, 255, 0), (0, 0, 255))
        cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), color, 3)

        # Volume parameters
        length = round(math.hypot((x1 - x2),(y1 - y2)), 3) 
        vol = np.interp(length, [20, 200], [self.volume_range[0], self.volume_range[1]])
        vol_percent = np.interp(vol, [self.volume_range[0], self.volume_range[1]], [0, 100])
        bar_height = np.interp(length, [20, 220], [400, 150])
        self.__setVolume(vol)

        # Volume in screen
        cv2.circle(img, (85, 400), 5, (255, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (85, 400), (50, 150), (0, 255, 0), 3)
        cv2.rectangle(img, (85, 400), (50, int(bar_height)), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(vol_percent)}%", (40, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
