from math import sqrt
from math import atan
import numpy as np

'''
An internal function is a function used within this file
An external function is a function that is called outside this file
'''

class var():

    y_zero = 0
    y_max = 480
    x_zero = 0
    x_max = 640
    destination = [0, 0]

# interal function
def calculate_slope(y0, y1, x0, x1):
    slope = (y0-y1)/(x0-x1)
    return slope

# interal function
def convert_degrees_to_slope(degrees):
    slope = np.tan(np.deg2rad(90-degrees))
    return slope

# interal function
def convert_slope_to_degrees(slope):
    degrees = np.rad2deg(atan(slope))
    return degrees

def set_destination_coordinates(x_robot, y_robot, orientation):
    if orientation == 0:
        var.destination = [x_robot, var.y_max]

    elif orientation == 90:
        var.destination = [var.x_max, y_robot]

    elif orientation == 180:
        var.destination = [x_robot, var.y_zero]

    elif orientation == 270:
        var.destination = [var.x_zero, y_robot]

    else:
        slope = convert_degrees_to_slope(orientation)

        if orientation > 270:
            xx = (slope*x_robot + var.y_max - y_robot)/slope
            yy = (var.x_zero - x_robot)*slope + y_robot

            xx_length = sqrt(pow(var.y_max - y_robot, 2) + pow(xx - x_robot, 2))
            yy_length = sqrt(pow(yy - y_robot, 2) + pow(var.x_zero - x_robot, 2))

            if xx_length < yy_length:
                x = xx
                y = var.y_max
            else:  # yy_length < xx_length
                y = yy
                x = var.x_zero

        elif orientation > 180:
            xx = (x_robot*slope + var.y_zero - y_robot) / slope
            yy = (var.x_zero - x_robot)*slope + y_robot

            xx_length = sqrt(pow(var.y_zero - y_robot, 2) + pow(xx - x_robot, 2))
            yy_length = sqrt(pow(yy - y_robot, 2) + pow(var.x_zero - x_robot, 2))

            if xx_length < yy_length:
                x = xx
                y = var.y_zero
            else:  # yy_length < xx_length
                y = yy
                x = var.x_zero

        elif orientation > 90:
            xx = (var.y_zero - y_robot + x_robot*slope)/slope
            yy = (var.x_max - x_robot)*slope + y_robot

            xx_length = sqrt(pow(var.y_zero - y_robot, 2) + pow(xx - x_robot, 2))
            yy_length = sqrt(pow(yy - y_robot, 2) + pow(var.x_max - x_robot, 2))

            if xx_length < yy_length:
                x = xx
                y = var.y_zero
            else:  # yy_length < xx_length
                y = yy
                x = var.x_max

        elif orientation > 0:
            xx = (var.y_max - y_robot + x_robot * slope) / slope
            yy = (var.x_max - x_robot)*slope + y_robot

            xx_length = sqrt(pow(var.y_max - y_robot, 2) + pow(xx - x_robot, 2))
            yy_length = sqrt(pow(yy - y_robot, 2) + pow(var.x_max - x_robot, 2))

            if xx_length < yy_length:
                x = xx
                y = var.y_max
            else:  # yy_length < xx_length
                y = yy
                x = var.x_max

        var.destination = [int(x), int(y)]

    return var.destination



    
# external function
def calculate_angle_difference(x_robot, y_robot, orientation):
    if (x_robot - var.destination[0]) != 0:
        required_slope = calculate_slope( \
            y_robot, \
            var.destination[1], \
            x_robot, \
            var.destination[0])

        additional_orientation = convert_slope_to_degrees(required_slope)

    xd = var.destination[0]
    yd = var.destination[1]

    xr = x_robot
    yr = y_robot

    if yd == yr:
        if xd > xr:
            req_orientation = 90
        else: # xd < xr
            req_orientation = 270
    elif xd == xr:
        if yd > yr:
            req_orientation = 0
        else: # yd < yr
            req_orientation = 180

    elif yd > yr:
        if xd > xr:
            req_orientation = 90 - abs(additional_orientation)
        else: # xd < xr
            req_orientation = abs(additional_orientation) + 270
    else: # yd < yr
        if xd > xr:
            req_orientation = abs(additional_orientation) + 90
        else: # xd < xr
            req_orientation = 270 - abs(additional_orientation)

    #angle_diff = req_orientation - orientation
    # convert to a multiple of 10
    #req_orientation = int(round(req_orientation, -1))

    return int(round(req_orientation,-1)), xd, yd 
