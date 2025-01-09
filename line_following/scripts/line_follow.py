#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:56:53 2025

@author: furkan
"""


import cv2
import numpy as np 
import rospy
import time
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
from sensor_msgs.msg import Image



class HectorQuadrotor():
    def __init__(self):
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.bridge = CvBridge()
        rospy.Subscriber("/front_cam/camera/image", Image, self.kameraCallback)
        self.hiz_mesaj = Twist()             
        rospy.sleep(1)
        
    
    def kalkis_yap(self):
        self.hiz_mesaj.linear.z = 1.0
        self.hiz_mesaj.angular.z = 0.0
        self.pub.publish(self.hiz_mesaj)

        time.sleep(0.5)
        
        self.hiz_mesaj.linear.z = 0.0
        self.hiz_mesaj.angular.z = 0.0
        self.pub.publish(self.hiz_mesaj)
        time.sleep(1)
    

    def kameraCallback(self, mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        alt_sari = np.array([20,100,100])
        ust_sari = np.array([40,255,255])
        maske = cv2.inRange(hsv,alt_sari,ust_sari)
        h,w,d = img.shape
        cv2.circle(img,(int(w/2),int(h/2)),3,(0,0,255),-1)
        M = cv2.moments(maske)
        if M['m00'] > 0:
            ax = int(M['m10']/M['m00'])
            ay = int(M['m01']/M['m00'])
            cv2.circle(img,(ax,ay),3,(0,255,0),-1)
            sapma = ax - w/2
            self.hiz_mesaj.linear.x = 0.3
            self.hiz_mesaj.angular.z = -sapma / 50.0
            self.pub.publish(self.hiz_mesaj)
        else:
            self.hiz_mesaj.linear.x = 0.0
            self.hiz_mesaj.angular.z = 0.0
            self.pub.publish(self.hiz_mesaj)
                

                
        cv2.imshow("Kamera", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    rospy.init_node('hector_linefollow', anonymous=True)
    hector = HectorQuadrotor()
    hector.kalkis_yap()
    rospy.spin()

