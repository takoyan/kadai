#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class move():
    def __init__(self):
        pub =rospy.init_node('ControlTurtleBot', anonymous=False)

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        r = rospy.Rate(10)
        twist = Twist()

        twist.linear.x = 2
        twist.angular.z = 0.5

        while not rospy.is_shutdown():
            print("aaa")
            self.cmd_vel.publish(twist)
            r.sleep

    def shutdown(self):
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    move()
