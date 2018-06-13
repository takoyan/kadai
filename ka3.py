#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

import socket
from time import sleep
import re

class move():
    def __init__(self):
        pub =rospy.init_node('ControlTurtleBot', anonymous=False)

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        r = rospy.Rate(10)
        twist = Twist()

        #twist.linear.x = 2
        #twist.angular.z =0

        #pub = rospy.Publisher('chatter', String, queue_size=10)
        #rospy.init_node('talker', anonymous=True)
        #r = rospy.Rate(10)
        while not rospy.is_shutdown():
            HOST = "localhost"
            PORT = 10500
            cliant = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            cliant.connect((HOST,PORT))

            while 1:
                try:
                    data = ""
                    while 1:
                        response = cliant.recv(1024)
                        if '<RECOGOUT>\n' in response and '</RECOGOUT>\n' in response:
                            data = response
                        if '<RECOGOUT>\n' in response or '</RECOGOUT>\n' in response:
                            data = data + response
                        else:
                            data = ""

                        if '</RECOGOUT>' in data:
                            text = ""
                            line_list = data.split('\n')
                            for line in line_list:
                                if 'WHYPO' in line:
                                    word = re.compile('WORD="((?!").)+"').search(line)
                                    if word:
                                        text = text + word.group().split('"')[1]
                                        print (text)
                            if text is not "":
                                if '前'in  text:
                                    twist.linear.x = 2
                                    twist.angular.z =0
                                elif '後ろ' in text:
                                    twist.linear.x =-2
                                    twist.angular.z =0
                                elif '右' in text:
                                    twist.linear.x=2
                                    twist.angular.z=2

                                self.cmd_vel.publish(twist)
                                r.sleep

                            data = ""

                except KeyboardInterrupt:
                    client.close()
                    sleep(3)
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((HOST, PORT))



    def shutdown(self):
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


if __name__ == '__main__':
    move()
