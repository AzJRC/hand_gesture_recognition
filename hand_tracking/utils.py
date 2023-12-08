import numpy as np
import math

# shoelace formula
def calculate_area(*cords: tuple):
    if len(cords) < 3:
        raise ValueError("At least three (x, y) coordinates are required.")

    # Convert the coordinates to a NumPy array
    polygon_vertexes = list(cords) + [cords[0]]

    # Calculate the area using the shoelace formula
    sum = 0
    for prev in range(len(polygon_vertexes) - 1):
        next = prev + 1
        if next >= len(polygon_vertexes):
            next = next - prev
    
        matrix = [polygon_vertexes[prev], polygon_vertexes[next]]
        sum += np.linalg.det(matrix)

    return abs(math.ceil(sum) / 2)
