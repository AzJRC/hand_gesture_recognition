import cv2 as cv
import mediapipe as mp
import time
import math
import utils

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # Public

    def findHands(self, img, draw_image=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if draw_image:
            if self.results.multi_hand_landmarks:
                for handLmks in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLmks, self.mpHands.HAND_CONNECTIONS)
        return img, self.results


    def findPosition(self, img, handNo: int = -1, ldmks: tuple | None = None):
        ldmk_list = []

        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks if handNo == -1 else [self.results.multi_hand_landmarks[handNo]]  
            for hand_id, hand in enumerate(hands):
                current_hand_ldmks_list = []      
                for ldmk_id, ldmk in enumerate(hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(ldmk.x * w), int(ldmk.y * h)
                    if not ldmks: # Return all landmarks
                        current_hand_ldmks_list.append([hand_id, ldmk_id, cx, cy])
                    else: # Return only selected landmarks
                        for ldmk in ldmks:
                            if ldmk == ldmk_id:
                                current_hand_ldmks_list.append([hand_id, ldmk_id, cx, cy])
                ldmk_list.append(current_hand_ldmks_list)
        return ldmk_list if ldmk_list else []
    

    def distanceBetweenLandmarks():
        distance = 0

        #Todo

        return distance