import cv2 as cv
import time
import utils
import math
import numpy as np
from handTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Dependencies

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Constants

MIN_VOL = -96
MAX_VOL = 0

# Global variables
vol = volume.GetMasterVolumeLevel()

p_time = 0
c_time = 0

prev_length = 0
length = 0

bar_height = np.interp(vol, [MIN_VOL, MAX_VOL], [400, 150])

    # Gesture for activating volume control
reset_time = 0
finger_touch_count = 0
gesture = 0

    #Gesture for deactivating volume control

# Video capture from cv2
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


# Module HandDetector
hand_detector = HandDetector(maxHands=1 ,detectionCon=0.75)


while True:
    # Read video capture
    succ, img = cap.read()
    if not succ:
        print("Can't receive frame (stream end?). Exiting ...")
        break


    # Show FPS
    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    # Gesture detection
    img, results = hand_detector.findHands(img)
    ldmk_list = hand_detector.findPosition(img, ldmks=(4, 8))
    
    if len(ldmk_list) != 0:
        x1, y1 = ldmk_list[0][0][2], ldmk_list[0][0][3]
        x2, y2 = ldmk_list[0][1][2], ldmk_list[0][1][3]

        x_md = (x1 + x2)//2
        y_md = (y1 + y2)//2
        
        length = round(math.hypot((x1 - x2),(y1 - y2)), 3)

        ## touch your fingers quickly two times to modify the volume
        if not gesture:
            if c_time > reset_time:
                reset_time = c_time + 1
                finger_touch_count = 0
                continue

            if length < 30 and finger_touch_count % 2 != 1:  
                cv.circle(img, (x_md, y_md), 5, (0, 255, 0), cv.FILLED)
                finger_touch_count += 1
            
            if length > 80 and finger_touch_count % 2 == 1:
                finger_touch_count += 1

            if finger_touch_count >= 4:
                    st_x1, st_y1 = x1, y1
                    st_x2, st_y2 = x2, y2
                    finger_touch_count = 0
                    reset_time = c_time + 1
                    gesture = 1
        
        else:
            if c_time > reset_time:
                if math.dist((x1, y1),(st_x1, st_y1)) < 20 and math.dist((x2, y2),(st_x2, st_y2)):
                    gesture = 0
                reset_time = c_time + 1 
                st_x1, st_y1 = x1, y1
                st_x2, st_y2 = x2, y2

            cv.circle(img, (st_x1, st_y1), 20, (255, 255, 255), 2)
            cv.circle(img, (st_x2, st_y2), 20, (255, 255, 255), 2)

            cv.circle(img, (x1, y1), 10, (0, 255, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (0, 255, 0), cv.FILLED)
            cv.circle(img, (x_md, y_md), 5, (0, 255, 0), cv.FILLED)

            cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            vol = np.interp(length, [20, 200], [MIN_VOL, MAX_VOL])
            vol_percent = np.interp(vol, [MIN_VOL, MAX_VOL], [0, 100])
            bar_height = np.interp(length, [20, 220], [400, 150])
            volume.SetMasterVolumeLevel(vol, None)

            # Volume in screen
            cv.circle(img, (85, 400), 5, (255, 0, 255), cv.FILLED)
            cv.rectangle(img, (85, 400), (50, 150), (0, 255, 0), 3)
            cv.rectangle(img, (85, 400), (50, int(bar_height)), (0, 255, 0), cv.FILLED)
            cv.putText(img, f"{int(vol_percent)}%", (40, 440), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)


    # Close program
    cv.imshow('Image', img)
    if cv.waitKey(1) == ord('q'):
        print("Video finished.")
        break


cap.release()
cv.destroyAllWindows()


# img = hand_detector.findHands(img)
#     hand_pos = hand_detector.findHandPosition(img=img, draw_ldmks=[4, 8])
    
#     if hand_pos:
#         if hand_pos[0]:
#             thumb_pos_x, thumb_pos_y = hand_pos[0][4][2], hand_pos[0][4][3]
#             finger_pos_x, finger_pos_y = hand_pos[0][8][2], hand_pos[0][8][3]

#             delta_x, delta_y = pow(finger_pos_x - thumb_pos_x, 2), pow(finger_pos_y - thumb_pos_y, 2)
#             finger_thumb_dist = int(math.sqrt(delta_x + delta_y))
#             region_size = hand_detector.getHandRegionSize(img, -1, (14, 16, 20, 18))
#             ratio = round(finger_thumb_dist / (region_size / 100), 3)
            
#             cv.line(img, (thumb_pos_x, thumb_pos_y), (finger_pos_x, finger_pos_y), (0, 255, 0), 3)