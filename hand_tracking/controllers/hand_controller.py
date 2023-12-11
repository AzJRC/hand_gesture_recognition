from __future__ import annotations
import mediapipe as mp
import numpy as np
import time
import cv2
from typing import Type
from gestures import hand_gestures
from features import volume_feature
from utilities import time_utils


class HandController():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # init variables
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # features
        self.volume_controller_feature = volume_feature.VolumeControllerFeature()

        # timers
        self.hand_gestures_timer = time_utils.Timer()

        # changing variables
        self.c_time = 0
        self.p_time = 0

        self.waitUntilOpen = True
        self.touchCounter = 0
        
        # mp solutions for hand detection
        self.mpHands = mp.solutions.hands
        self.mpDetectedHands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        # Run default configuration
        self.handControllerConfig()

    
    def handControllerConfig(self, WAIT_TIME: int = 3, NUMBER_OF_HANDS: int = 0, MARK_HANDS_LANDMARKS: bool = True):
        """
            Todo
        """

        self.WAIT_TIME = WAIT_TIME
        self.NUMBER_OF_HANDS = NUMBER_OF_HANDS
        self.MARK_HANDS_LANDMARKS = MARK_HANDS_LANDMARKS


    def runProgram(self, hand_controller: Type[HandController], img: np.ndarray):
        """
        # `runProgram()` Method

        Call this method to run the program.

        ## Parameters guidance

        - hand_controller: An instance of this class.
        - img: An img from `cap.read()`

        """

        results = hand_controller.__findHands(img, self.MARK_HANDS_LANDMARKS)
        if not results:
            return

        #Current time
        self.c_time = time.time()

        # Detect gestures
        detected_ldmks = hand_controller.__findLandmarksPosition(img, self.NUMBER_OF_HANDS)
        if detected_ldmks:
            hand_controller.__handGesturesDetection(img, detected_ldmks)

        #Previous time
        self.p_time = self.c_time
    

    def __handGesturesDetection(self, img: np.ndarray, hand_ldmks: list):
        """ 
            # `__handGesturesDetection()` Method

            This method will handle the following gesture operations:
            - IndexThumbTouch
                - It activates when your index finger touches your thumb.
                - Left click operation
            - IndexThumbTouching [Todo]
                - It activates when your index finger touches for 3 seconds your thumb.
                - Volume control feature.
            - IndexPointing [Todo]
                - It activates only when your index finger points to the camera.
                - Cursor control feature.
        """

        # ldmks
        thumb_tip_ldmk = hand_ldmks[4]
        index_tip_ldmk = hand_ldmks[8]

        # features
        if self.volume_controller_feature.active:
            self.volume_controller_feature.runVolumeController(img, thumb_tip_ldmk, index_tip_ldmk, self.hand_gestures_timer, self.c_time, self.WAIT_TIME)
        

        # Gestures
        else:

            # IndexThumb Gestures
            if self.touchCounter > 3:
                self.touchCounter = 0

            doIndexThumbTouch = hand_gestures.indexThumbTouch(img, thumb_tip_ldmk, index_tip_ldmk)
            if doIndexThumbTouch:

                if self.waitUntilOpen:
                    self.waitUntilOpen = False
                    self.touchCounter += 1

                if self.touchCounter == 1:
                    doIndexThumbTouching = hand_gestures.indexThumbTouching(img, thumb_tip_ldmk, index_tip_ldmk, self.hand_gestures_timer, self.c_time, self.WAIT_TIME)
                    if doIndexThumbTouching:
                        self.volume_controller_feature.active = True

            else:
                self.hand_gestures_timer.stopTimer()
                self.waitUntilOpen = True

            #Index pointing gesture
            pass


        # CV2 draws
        cv2.putText(img, f"{str(self.touchCounter)}", (600, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                
    


    
    def __findHands(self, img, draw_image: bool = True):
        """
            #` __findHands()` Method

            Use this method to detect your hands using mediapipe.

            ## Parameters guidance

            - img: An img from `cap.read()`
            - draw_image: True if you want to mark the landmarks detected by mediapipe. Default value is set to True
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.mpDetectedHands.process(imgRGB) 
        if draw_image:
            if self.results.multi_hand_landmarks:
                for handLmks in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLmks, self.mpHands.HAND_CONNECTIONS)
        return self.results


    def __findLandmarksPosition(self, img, handNo: int = 0, mark_ldmks: list | None = [], mark_params: dict = {}):
        """ 
            # `__findLandmarksPosition()` Method

            Use this method to obtain the coordinates of hand landmarks in a list. You can access a specific landmark by its ID, 
            as defined in the official [MediaPipe Hand Landmarks documentation](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker "Hand landmarks detection guide").

            ## Parameters Guidance

            - img: An instance of the image obtained from `cap.read()`.
            - HandNo: Specify the hand for which you want to retrieve landmark positions.
            - mark_landmks: Provide a list of landmark IDs to mark them with circles on the image.
            - mark_params: Parameters for the `cv2.circle()` function. Only necessary if you provided landmark IDs to mark. 
                Keywords: `(radius, color, thickness)`.
        """

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            ldmks = []   
            for ldmk_id, ldmk in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(ldmk.x * w), int(ldmk.y * h)
                ldmks.append((ldmk_id, cx, cy))
                if mark_ldmks:
                    for mark_ldmk in mark_ldmks:
                        if mark_ldmk == ldmk_id:
                            radius = mark_params["radius"] if "radius" in mark_params else 10
                            color = mark_params["color"] if "color" in mark_params else (255, 255, 255)
                            thinkness = mark_params["thickness"] if "thickness" in mark_params else cv2.FILLED
                            cv2.circle(img, (cx, cy), radius, color, thinkness)
            self.ldmks_list = ldmks
            return ldmks      


##############################
##############################


def main():
    hand_controller = HandController()
    cap = cv2.VideoCapture(0)

    while True:
        succ, img = cap.read()
        if not succ:
            break

        img, results = hand_controller.__findHands(img)
        if not results:
            continue

        ldmks = hand_controller.__findLandmarksPosition(img, mark_ldmks=[4, 8], mark_params={"color": (0, 0, 255)})

        cv2.imshow('Image', img)
        if cv2.waitKey(1) == ord('q'):
            print("Video finished.")
            break


if __name__ == "__main__":
    main()