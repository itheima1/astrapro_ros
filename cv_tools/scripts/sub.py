#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import socket
import struct
import threading
import traceback
import numpy
import time


class Client(object):
    def __init__(self, addr_port=('172.16.0.200', 11000)):
        self.addr_port = addr_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.resolution = (640, 480)
    def connect(self):
        try:
            self.client.connect(self.addr_port)
            return True
        except Exception as e:
            traceback.print_exc()  
            return False
    def send2server(self,img):
        img_code = numpy.array(img)
        img = img_code.tostring()
        length = len(img)
        all_data = struct.pack('ihh', length, self.resolution[0], self.resolution[1]) + img
        self.client.send(all_data)
        time.sleep(0.01)



def callback(imgmsg):
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
    #print('******************')
    #print(img.shape)
    #cv2.imshow("listener", img)
    #cv2.waitKey(3)
    client.send2server(img)

client = Client()
client.connect()
if __name__ == '__main__':

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

