# Hand Gesture Recognition

This is my first project related to computer vision and machine learning. The hand gesture detection is possible thanks to MediaPipe library.

I want this project to be a very big program for hand gesture recognition with lots of capabilities. Maybe in the future, I'll include more gestures besides the hands.

## How to use this program

just run `py .\hand_tracking\app.py`

## Current gestures

1. Enable Volume Controler
    - Approach your index finger and your thumb.
    - Wait 3 seconds.
    - Adjust volume using the distance between your index finger and your thumb.
    - Stay 3 seconds in the desired volume.

## What if not works?

The following list could be one of the reasons the program is not working for you.

- You haven´t installed the dependencies. Use `pip install -r .\dependencies.txt`.
- In the `app.py` file, there is a line of code that selects your camera. This line: `cap = cv.VideoCapture(0)`. Change the value 0 for your desired camera; however, the number 0 should be your default camera.
- Maybe your antivirus is not allowing python to use your camera. Deactivate it or include the file in the whitelist.

If any of the previous reasons is your case, feel free to add an issue so everybody can try fix it. Thank you for your collaboration.

## Ways to improve this

- **Depth detection:** Currently there is no way to detect how far away you are of the camera. This leads to undesired behavior if you are not in the range (around 30 to 50 cm).
  - *Note:* There is a `utils.py` file with a function that calculates the area of a polygon. That could be useful for a temporary depth detection algortihm that uses the area of the hand or a section of it.
- **Gesture timing:** Right now it works pretty fine, but surely there are better ways to handle gesture timing.
- **Gesture detection:** You'll notice that if you flip your hand or put it behind something, the algorithm still tries to detect the position of the fingers, which can lead to unexpected behavior.

## How to colaborate?

Feel free to colaborate in this project. Just clone the work and when you finish your changes make a pull request. Thank you very much! I'll appreciate your work.
