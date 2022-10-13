#!/usr/bin/env python3

# files
from .straight_driving import *
from .driving_functions import *

# libraries
from rclpy.node import Node

import cv2
import time
import rclpy

from std_msgs.msg import Int16
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
# -----------------------------------------------------------------------------
# Node class
# -----------------------------------------------------------------------------


class Controller(Node):

    def __init__(self):
        super().__init__('controller')

# -----------------------------------------------------------------------------
# Publishers
# -----------------------------------------------------------------------------
        self.publisher_0 = self.create_publisher(
            String, 'robot1_pwm_values', 10)
        self.publisher_1 = self.create_publisher(
            String, 'robot2_pwm_values', 10)

# -----------------------------------------------------------------------------
# Subscribers
# -----------------------------------------------------------------------------
        self.number_subscriber_0 = self.create_subscription(
            Int16, "id_0_orientation", self.callback_number_0, 10)
        self.number_subscriber_1 = self.create_subscription(
            Int16, "id_1_orientation", self.callback_number_1, 10)

        self.xy_subscriber_1 = self.create_subscription(
            Int16MultiArray, "id_0_coordinates", self.xy_callback_number_0, 10)
        self.xy_subscriber_1 = self.create_subscription(
            Int16MultiArray, "id_1_coordinates", self.xy_callback_number_1, 10)

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.window_name = 'Keyboard Input'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        self.get_logger().info('Initialized')

        self.pass3 = 1
        self.pass4 = 0

        self.accuracy = 20  # degrees of accuracy
        self.time_step = 0.9
        self.time_start = 0
        self.time_stop = 0

        self.robot_0 = 0
        self.robot_1 = 1
        self.control_robot = self.robot_0

        self.turn_permission_factor = 1
        self.enter_3 = 0

        self.req_orientation = 0
        self.enabled_straight_driving = 0
        self.end_coordinates_set = 1

        self.dest_x = 0
        self.dest_y = 0

        self.turn = 1

        self.seek_orientation = 0
        self.orientation = 0

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

    def callback_number_0(self, msg):
        self.orientation = msg.data

    def callback_number_1(self, msg):
        self.orientation = msg.data

    def xy_callback_number_0(self, msg):
        self.robot_coordinates = msg.data

    def xy_callback_number_1(self, msg):
        self.robot_coordinates = msg.data

# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
    def timer_callback(self):

# -----------------------------------------------------------------------------
# Read inputs and correct ascii numbers to characters
# -----------------------------------------------------------------------------
        action = cv2.waitKey(1)
        action = correcting_action_values(action)

# -----------------------------------------------------------------------------
# Switching between robots
# -----------------------------------------------------------------------------
        if action == '1' or action == '2':
            self.control_robot, action = change_robot(action)

# -----------------------------------------------------------------------------
# Controlling to which direction the robot is facing
# PUT INTO A SEPERATE FILE??
# -----------------------------------------------------------------------------

        # stop turning
        if action == 'q':
            self.turn = 1
            self.enabled_straight_driving = 0
            self.end_coordinates_set = 1


        # if a turning command is given continue
        if (action == 't' or action == 'y' or action == 'u' or action == 'g' or
            action == 'h' or action == 'v' or action == 'b' or action == 'n') \
                and self.turn:

            self.seek_orientation = set_orientation_to_seek(action)
            self.turn = 0

        if self.turn == 0:
            degrees_abs_difference = abs(self.seek_orientation
                                         - self.orientation)
            print(f'{degrees_abs_difference} = {self.orientation} \
                - {self.seek_orientation}')
            if degrees_abs_difference >= self.accuracy:

                # turning robot
                if time.time() > (self.time_stop + self.time_step) \
                        and self.pass3:
                    self.time_start = time.time()
                    action = 'a'
                    self.pass3 = 0
                    self.pass4 = 1

                # pausing robot
                elif time.time() > (self.time_start + self.time_step) \
                        and self.pass4:
                    self.time_stop = time.time()
                    self.pass3 = 1
                    self.pass4 = 0
                    action = 'q'
            # stop
            elif degrees_abs_difference < self.accuracy:
                action = 'q'
                self.turn = 1


# -----------------------------------------------------------------------------
# Enable/disable straight driving
# -----------------------------------------------------------------------------

        forward_moving_indicator = is_moving_forward()

        if action == 'p':
            self.enabled_straight_driving = 1
        elif action == 'o' or action == 'q':
            self.enabled_straight_driving = 0
            self.end_coordinates_set = 1

        if self.enabled_straight_driving:
            if forward_moving_indicator:

                if self.end_coordinates_set == 1:

                    set_destination_coordinates(
                        self.robot_coordinates[0],
                        self.robot_coordinates[1],
                        self.orientation)
                    self.end_coordinates_set = 0


                self.req_orientation, self.dest_x, self.dest_y\
                     = calculate_angle_difference(
                    self.robot_coordinates[0],
                    self.robot_coordinates[1],
                    self.orientation)                

                value_1 = self.orientation
                value_2 = self.orientation
                value_3 = self.orientation

                for num in range(7):
                    value_1 += 10*num
                    if value_1 == -10:
                        value_1 = 350
                    elif value_1 == 360:
                        value_1 = 0

                    value_2 -= 10*num
                    if value_2 == -10:
                        value_2 = 350
                    elif value_2 == 360:
                        value_2 = 0

                    if value_1 == self.req_orientation and \
                        self.turn_permission_factor > 0:
                        action = 'a'
                        self.turn_permission_factor -= 1
                        self.enter_3 = 1
                        break

                    elif value_2 == self.req_orientation and \
                        self.turn_permission_factor < 2:
                        action = 'd'
                        self.turn_permission_factor += 1
                        self.enter_3 = 1
                        break

                    if value_3 == self.req_orientation and \
                        self.turn_permission_factor > 0 and \
                            self.enter_3 == 1:
                        self.enter_3 = 0
                        action = 'a'
                        self.turn_permission_factor == 1
                        break
                    elif value_3 == self.req_orientation and \
                        self.turn_permission_factor < 2 and \
                            self.enter_3 == 1:
                        self.enter_3 = 0
                        action = 'd'
                        self.turn_permission_factor == 1
                        break


        
# -----------------------------------------------------------------------------
# Driving logic
# -----------------------------------------------------------------------------
        quick_actions(action)
        operations_standing_still(action)
        operations_moving_forward(action)
        operations_moving_backwards(action)
        set_turn_factor_when_moving()

        prep_data_for_code_logic()

        prep_data_for_code_logic()
        key = prep_data_for_topic()

# -----------------------------------------------------------------------------
# Live feedback
# -----------------------------------------------------------------------------

        print(action)
        print(f'Robot: {self.control_robot + 1}')
        print(f'Straight Driving: {self.enabled_straight_driving}')
        print(f'Coordinates Set: {self.end_coordinates_set}')
        print('Orientation and Seek Orientation')
        print(self.orientation)
        print(self.req_orientation)
        print(f'Moving forward: {forward_moving_indicator}')
        print(f'Destination: [{self.dest_x}, {self.dest_y}]')
# -----------------------------------------------------------------------------
# Publishing logic
# -----------------------------------------------------------------------------
        msg = String()
        msg.data = f'{key}'
        if action != -1:
            if action == 'q':
                self.publisher_0.publish(msg)
                self.publisher_1.publish(msg)
            elif self.control_robot == self.robot_0:
                self.publisher_0.publish(msg)
            elif self.control_robot == self.robot_1:
                self.publisher_1.publish(msg)
            #self.get_logger().info(f'Key press: {msg.data}')

# -----------------------------------------------------------------------------
# def main
# -----------------------------------------------------------------------------


def main(args=None):
    rclpy.init(args=args)
    controller = Controller()
    rclpy.spin(controller)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
