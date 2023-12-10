from __future__ import annotations
import mediapipe as mp
import numpy as np
import time
import cv2
from typing import Type
from gestures import hand_gestures
from utilities import time_utils


class HandController():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # init variables
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # timer
        self.timer = time_utils.Timer()

        # changing variables
        self.c_time = 0
        self.p_time = 0
        
        # mp solutions for hand detection
        self.mpHands = mp.solutions.hands
        self.mpDetectedHands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def runProgram(self, hand_controller: Type[HandController], img: np.ndarray):
        """
        # Todo

        """

        results = hand_controller.findHands(img)
        if not results:
            return

        #Current time
        self.c_time = time.time()


        # Detect gestures
        detected_ldmks = hand_controller.findLandmarksPosition(img)
        if detected_ldmks:
            hand_controller.handGestures(img, detected_ldmks)


        #Previous time
        self.p_time = self.c_time


    

    def handGestures(self, img: np.ndarray, hand_ldmks: list):
        """ 
            # handGestures() Method

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

        doIndexThumbTouch = hand_gestures.indexThumbTouch(img, hand_ldmks[4], hand_ldmks[8])
        if doIndexThumbTouch:
            # IndexThumbTouch action


            doIndexThumbTouching = hand_gestures.indexThumbTouching(img, hand_ldmks[4], hand_ldmks[8], self.timer, self.c_time)
            if doIndexThumbTouching:
                # IndexThumbTouching Action

                pass
        else:
            self.timer.resetTimer()
    


    
    def findHands(self, img, draw_image: bool = True):
        """
            - img: An img instance from cap.read()
            - draw_image: Wheter you want to mark the landmarks detected by mediapipe.
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.mpDetectedHands.process(imgRGB) 
        if draw_image:
            if self.results.multi_hand_landmarks:
                for handLmks in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLmks, self.mpHands.HAND_CONNECTIONS)
        return self.results


    def findLandmarksPosition(self, img, handNo: int = 0, mark_ldmks: list | None = [], mark_params: dict = {}):
        """ 
            - img: An img instance from cap.read()
            - HandNo: Hand you want to get its landmarks position
            - mark_landmks: Pass the landmarks ids in a list to mark it (with a circle). 
            - mark_params: Parameters of cv2.circle(). Only if you provided landmarks to mark. Keywords: (radius, color, thickness)
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


def main():
    hand_controller = HandController()
    cap = cv2.VideoCapture(0)

    while True:
        succ, img = cap.read()
        if not succ:
            break

        img, results = hand_controller.findHands(img)
        ldmks = hand_controller.findLandmarksPosition(img, mark_ldmks=[4, 8], mark_params={"color": (0, 0, 255)})

        cv2.imshow('Image', img)
        if cv2.waitKey(1) == ord('q'):
            print("Video finished.")
            break


if __name__ == "__main__":
    main()