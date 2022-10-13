import cv2 as cv
from cv2 import aruco
import numpy as np
import math
import os

class var():
    
    print(os.getcwd())
    calib_data_path = "/home/tian/ros2_ws/build/robot_controller/robot_controller/MultiMatrix.npz"

    calib_data = np.load(calib_data_path)
    print(calib_data.files)

    cam_mat = calib_data["camMatrix"]
    dist_coef = calib_data["distCoef"]
    r_vectors = calib_data["rVector"]
    t_vectors = calib_data["tVector"]

    MARKER_SIZE = 8  # centimeters

    marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

    param_markers = aruco.DetectorParameters_create()

    cap = cv.VideoCapture(0)
    #cap.set(cv.CAP_PROP_FRAME_WIDTH, int(1280))
    #cap.set(cv.CAP_PROP_FRAME_HEIGHT, int(720))

    distance_list_1 = []
    distance_list_0 = []
    distance_list_2 = []
    distance_list_3 = []
    distance_list_4 = []
    distance_list_5 = []

    aruco_width = 200
    new_orientation = 0

    memory_buffer = 20

    id = 0

    robot_coordinates = [0, 0]

def get_orientation(x, y, angle):
        # quadrant 1
    if x > 0 and y < 0:
        orientation = angle

    # quadrant 2
    elif x < 0 and y < 0:
        orientation = 90 + (90 - angle)
    #quadrant 3
    elif x < 0 and y > 0:
        orientation = 180 + angle
    
    #quadrant 4
    elif x > 0 and y > 0:
        orientation = 270 + (90 - angle)

    # line cases
    elif x == 0 and y != 0:
        if y < 0:
            orientation = 90
        elif y > 0:
            orientation = 270

    elif y == 0 and x != 0:
        if x < 0:
            orientation = 180
        elif x > 0:
            orientation = 0

    elif x == 0 and y == 0:
        print('ERROR x and y equals 0')

    # convert angle to the correct convention
    # this is not recommended method if fast run time is required
    # takes 0.0005 seconds
    for _ in range(18):
        orientation = orientation - 10
        if orientation < 0:
            orientation += 360
    return orientation

def consistantly_display_markers_distances(ids, distance):
    if ids == 0:
        var.distance_list_0.append(distance)
        distance = (max(var.distance_list_0) + min(var.distance_list_0))/2
        if (len(var.distance_list_0) > var.memory_buffer):
            del var.distance_list_0[0]
    if ids == 1:
        var.distance_list_1.append(distance)
        distance = (max(var.distance_list_1) + min(var.distance_list_1))/2
        if (len(var.distance_list_1) > var.memory_buffer):
            del var.distance_list_1[0]
    if ids == 2:
        var.distance_list_2.append(distance)
        distance = (max(var.distance_list_2) + min(var.distance_list_2))/2
        if (len(var.distance_list_2) > var.memory_buffer):
            del var.distance_list_2[0]
    if ids == 3:
        var.distance_list_3.append(distance)
        distance = (max(var.distance_list_3) + min(var.distance_list_3))/2
        if (len(var.distance_list_3) > var.memory_buffer):
            del var.distance_list_3[0]
    if ids == 4:
        var.distance_list_4.append(distance)
        distance = (max(var.distance_list_4) + min(var.distance_list_4))/2
        if (len(var.distance_list_4) > var.memory_buffer):
            del var.distance_list_4[0]
    if ids == 5:
        var.distance_list_5.append(distance)
        distance = (max(var.distance_list_5) + min(var.distance_list_5))/2
        if (len(var.distance_list_5) > var.memory_buffer):
            del var.distance_list_5[0]
    return distance

def orientation_function():

    _, frame = var.cap.read()

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, var.marker_dict, parameters=var.param_markers
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, var.MARKER_SIZE, var.cam_mat, var.dist_coef
        )
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[2].ravel()
            top_left = corners[3].ravel()
            bottom_right = corners[1].ravel()
            bottom_left = corners[0].ravel()

            # create lists from Numpy ndArray
            top_right_array = top_right.tolist()
            top_left_array = top_left.tolist()
            bottom_right_array = bottom_right.tolist()
            bottom_left_array = bottom_left.tolist()

            center_array = \
            [(top_left_array[0] + \
            top_right_array[0] + \
            bottom_left_array[0] + \
            bottom_right_array[0])/4, \
            (top_left_array[1] + \
            top_right_array[1] + \
            bottom_left_array[1] + \
            bottom_right_array[1])/4]

            var.robot_coordinates = center_array

            center = [(top_left[0] + top_right[0] + bottom_left[0] + \
                bottom_right[0])/4, (top_left[1] + top_right[1] + \
                    bottom_left[1] + bottom_right[1])/4]
            right_side_ref = [(top_right[0] + bottom_right[0])/2, \
                (top_right[1] + bottom_right[1])/2]
            
            x = (right_side_ref[0] - center[0])/(var.aruco_width/2)
            y = (right_side_ref[1] - center[1])/(var.aruco_width/2)

            x_abs = abs(x)
            y_abs = abs(y)

            angle = math.degrees(math.atan(y_abs/x_abs))

            orientation = get_orientation(x, y, angle)
            
            calc_orientation = int(orientation) - orientation%5

            if calc_orientation == 350 and (var.new_orientation == 0):
                var.new_orientation = calc_orientation
            elif calc_orientation == 0 and (var.new_orientation == 350):
                var.new_orientation = calc_orientation
            elif (calc_orientation > (var.new_orientation + 10)) or \
                (calc_orientation < (var.new_orientation - 10)):
                var.new_orientation = calc_orientation

            var.new_orientation = int(round(var.new_orientation, -1))

            if ids < 7:

                # PRINT PRINT PRINT PRINT PRINT
                # PRINT PRINT PRINT PRINT PRINT
                
                print('========')
                
                print(f'ID {ids}')
                print(f'Orientation: {var.new_orientation}')
                print(f'Coordinates 1: [{round(tVec[i][0][0],1)},{round(tVec[i][0][1],1)}]')
                print(f'Coordinates 2: {center_array}')

            
                #width  = var.cap.get(3)
                #height = var.cap.get(4) 
                #print(f'{width},{height},{cv.CAP_PROP_FRAME_COUNT}')

                # PRINT PRINT PRINT PRINT PRINT
                # PRINT PRINT PRINT PRINT PRINT

                

            # Calculating the distance
                distance = np.sqrt(
                    tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
                )
                # Draw the pose of the marker
                point = cv.drawFrameAxes(frame, var.cam_mat, var.dist_coef, rVec[i], tVec[i], 4, 4)

                distance = consistantly_display_markers_distances(ids, distance)
                
                cv.putText(
                    frame,
                    f"{int(var.new_orientation)}",
                    top_left,
                    cv.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255),
                    1,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"#{ids[0]}",
                    bottom_left,
                    cv.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255),
                    1,
                    cv.LINE_AA,
                )

                cv.putText(
                    frame,
                    f"{int(distance)} cm",
                    top_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255),
                    1,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"[{round(tVec[i][0][0],1)},{round(tVec[i][0][1],1)}]",
                    bottom_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255),
                    1,
                    cv.LINE_AA,
                )
                var.id = ids[0]

    return frame, var.id, var.new_orientation, var.robot_coordinates
    