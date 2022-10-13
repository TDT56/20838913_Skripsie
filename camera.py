#!/usr/bin/env python3

from .orientation import *
from std_msgs.msg import Int16
from std_msgs.msg import Int16MultiArray
from rclpy.node import Node
import cv2
import rclpy

class Camera(Node):

    def __init__(self):
        super().__init__('camera')
        self.publisher_0 = self.create_publisher(Int16, 'id_0_orientation', 10)
        self.publisher_1 = self.create_publisher(Int16, 'id_1_orientation', 10)
        self.publisher_0_xy = self.create_publisher(Int16MultiArray, 'id_0_coordinates', 10)
        self.publisher_1_xy = self.create_publisher(Int16MultiArray, 'id_1_coordinates', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.window_name = 'Camera View'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        self.get_logger().info('Initialized')

    def timer_callback(self):

        cv2.waitKey(30)


        frame, id, orientation, robot_coordinates = orientation_function()

        cv2.imshow(self.window_name, frame)

        coordinates = Int16MultiArray()
        coordinates.data = [int(robot_coordinates[0]), int(robot_coordinates[1])]

        orient = Int16()
        orient.data = orientation
        if id == 0:
            self.publisher_0.publish(orient)
            self.publisher_0_xy.publish(coordinates)
        elif id == 1:
            self.publisher_1.publish(orient)
            self.publisher_1_xy.publish(coordinates)


def main(args=None):
    rclpy.init(args=args)
    camera = Camera()
    rclpy.spin(camera)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
