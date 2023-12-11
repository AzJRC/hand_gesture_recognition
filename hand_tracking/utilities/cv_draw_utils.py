import cv2
import numpy as np


def colorTransition(variable: int, variable_range: list, asc_var: bool, begin_color: tuple = (0, 0, 255), end_color: tuple = (0, 255, 0)):
    """ 
        Todo
    """
    
    if not asc_var:
        begin_color, end_color = end_color, begin_color

    inital_B, end_B = begin_color[0], end_color[0]
    inital_G, end_G = begin_color[1], end_color[1]
    inital_R, end_R = begin_color[2], end_color[2]

    B_range = [inital_B, end_B]
    G_range = [inital_G, end_G] 
    R_range = [inital_R, end_R]

    curr_B = int(np.interp(variable, variable_range, B_range))
    curr_G = int(np.interp(variable, variable_range, G_range))
    curr_R = int(np.interp(variable, variable_range, R_range))

    return (curr_B, curr_G, curr_R)


def getLoadCircle(img: np.ndarray, variable: bool, variable_range: list, asc_var: bool, center: tuple, radius: int = 10,
                  begin_color: tuple = (0, 0, 255), end_color: tuple = (0, 255, 0),
                  thickness: int = cv2.FILLED, unload: bool = False, anti_clockwise: bool = False):
    """ 
        # getLoadCircle() Function

        It creates a loading animation in a capture video image.

        ## Parameters guidance

        - img: An img instance from cap.read()
        - variable: A changing variable that will define the load state.
        - variable range: A 2-value list representing the minimum and maximum values of the changing variable.
        - asc_var: Set it to true if the variable starts at the minimum and ends at the maximum. False otherwise. (If not provided correctly, may lead to unexpected behavior)
        - center: A 2-value tuple representing the center of the loading circle.
        - radius: Radius of the loading circle. By default the radius is 10.
        - begin_color: Initial color of the loading circle. By default the starting color is red. Color format is BGR,
        - end_color: Final color of the loading circle. By default the end volor is green. Color format is BGR.
        - thickness: Thickness of the loading circle. By default the circle will be filled.
        - unload: True to create an unloading circle. By default is set to False.
        - anti_clockwise: True to load/unload the circle in the other direction. By default is set to False.
    """

    curr_color = colorTransition(variable, variable_range, asc_var, begin_color, end_color)

    if anti_clockwise:
        loading_angle = 360 - int(np.interp(variable, variable_range, [360, 0]))
        if unload:
            start_angle, end_angle = 0, loading_angle #anti-clockwise unload
        else:
            start_angle, end_angle = loading_angle, 360 # anti-clockwise load

    else:
        loading_angle = int(np.interp(variable, variable_range, [360, 0]))   
        if unload:
            start_angle, end_angle = loading_angle, 360 #clockwise unload 
        else:
            start_angle, end_angle = 0, loading_angle #clockwise load
    
    cv2.ellipse(img, center, (radius, radius), 0, start_angle, end_angle, curr_color, thickness)
        