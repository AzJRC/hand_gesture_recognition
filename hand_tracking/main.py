import cv2
import time
from controllers.hand_controller import HandController


def main():

    # Dependencies
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        exit()

    # Constants


    # Variables
    hand_controller = HandController(maxHands=2, detectionCon=0.60)
    p_time = 0
    c_time = 0

    # Program starts
    while True:
        succ, img = cap.read()
        if not succ:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        ## Use this to create custom functionality
        # results = hand_controller.findHands(img)
        # ldmk_list = hand_controller.findLandmarksPosition(img)

        # Show FPS
        c_time = time.time()
        fps = int(1/(c_time - p_time))

        # Run default app
        hand_controller.runProgram(hand_controller, img)

        # Update previous time
        p_time = c_time
        cv2.putText(img, f"{str(fps)}", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Close program
        cv2.imshow('Image', img)
        if cv2.waitKey(1) == ord('q'):
            print("Video finished.")
            break


if __name__ == "__main__":
    main()