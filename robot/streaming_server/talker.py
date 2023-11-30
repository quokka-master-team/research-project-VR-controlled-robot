#!/usr/bin/env python3
# Software License Agreement (BSD License)

import rospy
from std_msgs.msg import String
from mavros_msgs.msg import OverrideRCIn

def talker():
    pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    message = OverrideRCIn()
    message.channels = [1800, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        pub.publish(message)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass