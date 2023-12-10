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


# Variables

MIN_VOL = -96
MAX_VOL = 0

vol = volume.GetMasterVolumeLevel()

p_time = 0
c_time = 0

prev_length = 0
length = 0

bar_height = np.interp(vol, [MIN_VOL, MAX_VOL], [400, 150])

prev_index_pos = None
prev_thumb_pos = None
t1 = None

index_velocity = None
thumb_velocity = None

FINGER_MOVEMENT_PARAM = 150

TIMER = 2
time_mark = 0
elapsed_time = 0
fingers_touch = False
fingers_touching = False

volume_controller = False


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


    # Gesture detection
    img, results = hand_detector.findHands(img)
    ldmk_list = hand_detector.findPosition(img, ldmks=(4, 8))
    
    if len(ldmk_list) != 0:

        x1, y1 = ldmk_list[0][0][2], ldmk_list[0][0][3] #thumb
        x2, y2 = ldmk_list[0][1][2], ldmk_list[0][1][3] #index
        t2 = time.time()

        if prev_thumb_pos and prev_index_pos and t1:
            thumb_velocity = abs(round(math.dist(prev_thumb_pos, (x1, y1)) / (t1 - t2), 2))
            index_velocity = abs(round(math.dist(prev_index_pos, (x2, y2)) / (t1 - t2), 2))

            index_is_moving = index_velocity > FINGER_MOVEMENT_PARAM
            index_is_static = index_velocity <= FINGER_MOVEMENT_PARAM 
            thumb_is_moving = thumb_velocity > FINGER_MOVEMENT_PARAM 
            thumb_is_static = thumb_velocity <= FINGER_MOVEMENT_PARAM

        prev_thumb_pos, prev_index_pos, t1 = (x1, y1), (x2, y2), t2      

        x_md = (x1 + x2)//2
        y_md = (y1 + y2)//2
        
        length = round(math.hypot((x1 - x2),(y1 - y2)), 3) #Todo in module


        # Volume controller
        if length < 10 and fingers_touch == False:
            fingers_touch = True

        elif length > 30 and fingers_touch == True:
            fingers_touch = False
            fingers_touching = False


        if volume_controller:
            if c_time > time_mark:
                time_mark = c_time + TIMER

            if thumb_is_static and index_is_static:
                elapsed_time = round(max(time_mark - time.time(), 0), 2)
                load_rgb = (0, 255 - elapsed_time / TIMER * 255, elapsed_time / TIMER * 255)
                cv.circle(img, (x1, y1), 20, load_rgb, 2)
                cv.circle(img, (x2, y2), 20, load_rgb, 2)

                if elapsed_time == 0:
                    volume_controller = False
            else:
                time_mark = c_time + TIMER
                cv.circle(img, (x1, y1), 20, (0, 0, 255), 2)
                cv.circle(img, (x2, y2), 20, (0, 0, 255), 2)
                
            
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

        else:
            if c_time > time_mark or fingers_touch == True:
                if not fingers_touching:
                    if fingers_touch:
                        fingers_touching = True
                    time_mark = c_time + TIMER
                
                if fingers_touching:
                    elapsed_time = round(max(time_mark - time.time(), 0), 2)
                    angle = 360 - elapsed_time / TIMER * 360

                    load_rgb = (0, 255 - elapsed_time / TIMER * 255, elapsed_time / TIMER * 255)
                    cv.ellipse(img, (x_md, y_md), (15, 15), 0, 0, angle, load_rgb, 5)

                    if elapsed_time == 0:
                        volume_controller = True
                        print("VOLUME CONTROLLER ACTIVE")


    # Close program
    cv.imshow('Image', img)
    if cv.waitKey(1) == ord('q'):
        print("Video finished.")
        break


cap.release()
cv.destroyAllWindows()