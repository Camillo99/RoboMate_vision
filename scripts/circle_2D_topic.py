#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from image_pros.msg import HoleCenterMsg2
import cv2
import numpy as np
import time



class CircleDetectionNode(Node):
    def __init__(self):
        super().__init__('circle_2D_detection')
        #subscription to zivid camera data
        self.subscription = self.create_subscription(
            Image,
            '/zivid/color/image_color',  # Replace 'image_topic' with your actual topic name
            self.image_callback,
            10)
        #pubblisher
        self.publisher_ = self.create_publisher(HoleCenterMsg2, 'hole_center_2D', 10)



        self.subscription  # prevent unused variable warning
        self.cv_bridge = CvBridge()
        self._raw_image = None

    def image_callback(self, msg):
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        # Save the image into a variable of cv2 (OpenCV)
        self._raw_image = cv_image
        self.get_logger().info("Image receved.")

        #process the image --> circle extraction
        self.get_logger().info("service called !")
        if self._raw_image is None:
            self.get_logger().warning("No raw image received yet.")
        else:

            #circle extraction process
            gray = cv2.cvtColor(self._raw_image, cv2.COLOR_BGR2GRAY)
            img = cv2.medianBlur(gray, 5)
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=30, minRadius=20, maxRadius=30)

            #create the message and pubblish on the topic --> hole_center_2D
            if circles is not None:
                circles = np.uint16(np.around(circles))
                hole_centers = circles[0, :, :2].astype(np.int16)

                msg = HoleCenterMsg2()
                msg.hole_center_x = hole_centers[:, 0].tolist()
                msg.hole_center_y = hole_centers[:, 1].tolist()
                #compute the index of the circle
                circle_values = []  # Array to store computed values for each circle
                for i in circles[0, :]:
                    value = i[0] + (i[1] * 1920)
                    circle_values.append(value)
                tmp_index = np.array(circle_values, dtype=np.int32)
                msg.point_index = tmp_index.tolist()

                self.get_logger().info("Detected hole centers: \n %s" % str(hole_centers))
                wait_time = 10
                self.get_logger().info("waiting %s second" % wait_time)
                time.sleep(wait_time)
                self.publisher_.publish(msg)
                self.get_logger().info('Publishing HoleCenterMsg')
            else:
                self.get_logger().warning("No circles detected in the image.")




def main(args=None):
    rclpy.init(args=args)
    node = CircleDetectionNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()