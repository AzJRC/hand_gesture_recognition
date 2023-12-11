# Hand Gesture Recognition

This is my first project related to computer vision and machine learning. The hand gesture detection is possible thanks to MediaPipe library.

I want this project to be a very big program for hand gesture recognition with lots of capabilities. Maybe in the future, I'll include more gestures besides the hands.

## How to use this program

just run `py .\hand_tracking\main.py`

## Project Structure and Files

Before contributing to this project, familiarize yourself with the project structure to understand how it's organized and written. The project follows a combination of Object-Oriented Programming (OOP) and Functional Programming, chosen based on specific needs. This choice is crucial for future code maintenance, changes, and updates.

- **controllers directory:** This directory houses gesture recognition code related to specific targets, such as hands or the body. Controllers are implemented as classes. Currently, only hand recognition is available.
- **features directory:** Here, you'll find code for "features," which are functionalities activated by performing specific gestures in sequence. Features are implemented as classes. Examples include the volume control feature and mouse control feature.
- **gestures directory:** This directory contains functions responsible for detecting gestures. A gesture function should return either True or False. Any logic following the detection of a gesture should be implemented in the respective controller file or the corresponding feature if the gesture is intended to activate one.
- **utilities directory:** This directory includes specific files for functions related to specific purposes other than gestures. These functions should serve general purposes rather than anything specific.
- **```main.py``` file:** This file serves as the entry point for the entire program, functioning like a facade. Note that this file contains the infinite loop for capturing video.

*Note: Do not confuse the term "control" in the feature name with the controllers directory.*

## Available gestures

1. Index and Thumb touch
2. Index and Thumb continuos touching

## Available Features

1. Enable Volume Controler
    - Approach your index finger and your thumb.
    - Wait 3 seconds.
    - Adjust volume using the distance between your index finger and your thumb.
    - Volume controller will deactivate automatically after 3 seconds.

## What if not works?

The following list could be one of the reasons the program is not working for you.

- You haven´t installed the dependencies. Use `pip install -r .\dependencies.txt`.
- In the `main.py` file, there is a line of code that selects your camera. This line: `cap = cv.VideoCapture(0)`. Change the value 0 for your desired camera; however, the number 0 should be your default camera.
- Maybe your antivirus is not allowing python to use your camera. Deactivate it or include the file in the whitelist.

If any of the previous reasons is your case, feel free to share the issue so everybody can try fix it. Thank you for your collaboration.

## Ways to improve this

- **Depth detection:** Currently there is no way to detect how far away you are of the camera. This leads to undesired behavior if you are not in the range (around 30 to 50 cm).
  - *Note:* There is a `utils.py` file with a function that calculates the area of a polygon. That could be useful for a temporary depth detection algortihm that uses the area of the hand or a section of it.
- **Gesture timing:** Right now it works pretty fine, but surely there are better ways to handle gesture timing.
- **Gesture detection:** You'll notice that if you flip your hand or put it behind something, the algorithm still tries to detect the position of the fingers, which can lead to unexpected behavior.
- **Refactoring and design:** Right know the code is following a OOP design pattern with functional programming. You'll find out that some files are just standalone functions written to be used in many cases rather than for a specific funcionality, and specific features or "controllers" are defined as python classes. However, there are many functions and classes that aren't yet separated as described previously. Additionally, some function are missing its documentation.
- **Program config class:** Almost all functionality of this program cannot be changed by the user unless he or she modifies the code, which is not very user friendly. A class for configuration of the whole program could be useful to define specific constant parameters and values, such as default waiting times for the timer and default landmarks colors.
- **Legacy framework:** The mediapipe framework used in this program have been recently deprecated. This is not good in the long term although the functionality is still working. Take a look at the `eg_new_framework` directory, where a face recognition example program was written using the updated solutions.
 
## How to colaborate?

Feel free to colaborate in this project. Just clone the work and when you finish your changes make a pull request. Thank you very much! I'll appreciate your work.
