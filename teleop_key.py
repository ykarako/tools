#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

pub_vehicle_l = rospy.Publisher('vehicle_driver/motor_speed/left', Int16, queue_size=1)
pub_vehicle_r = rospy.Publisher('vehicle_driver/motor_speed/right', Int16, queue_size=1)

def cb_teleop(msg):
    duty_l = msg.linear.x * 20 - msg.angular.z * 10
    duty_r = msg.linear.x * 20 + msg.angular.z * 10
    pub_vehicle_l.publish(duty_l)
    pub_vehicle_r.publish(duty_r)
    print("L:{} | R:{}".format(duty_l, duty_r))

if __name__ == '__main__':
    rospy.init_node('teleop_key')
    sub_teleop = rospy.Subscriber('cmd_vel', Twist, cb_teleop)
    rospy.spin()
