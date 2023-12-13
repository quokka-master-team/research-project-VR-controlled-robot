#!/usr/bin/env python3
# Software License Agreement (BSD License)

import rospy
import os
import subprocess
import time
from std_msgs.msg import String
from mavros_msgs.msg import OverrideRCIn

class RobotController:
    ros_launch_command = "roslaunch mavros px4.launch"
    ros_arm_command = "rosservice call /mavros/cmd/arming 'value: true'"
    ros_disarm_command = "rosservice call /mavros/cmd/arming 'value: false'"

    def __init__(self):
        self.ros_launch_process = None

    def init_node(self):
        self.ros_launch_process = subprocess.Popen(self.ros_launch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        self.init_node = rospy.init_node('talker', anonymous=True)
        self.pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
        self.message = OverrideRCIn()
        self.rate = rospy.Rate(10)  # 10Hz
        print("Node initialized")

    def terminate_pixhawk(self):
        self.disarm_pixhawk()
        self.kill_process_by_name('px4.launch')
        del self

    def arm_pixhawk(self):
        os.system(self.ros_arm_command)

    def disarm_pixhawk(self):
        os.system(self.ros_disarm_command)

    def move_forward(self):
        self.message.channels = [1600, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(self.message)
        self.rate.sleep()

    def move_backward(self):
        self.message.channels = [1400, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(self.message)
        self.rate.sleep()

    def move_left(self):
        self.message.channels = [1500, 1600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(self.message)
        self.rate.sleep()

    def move_right(self):
        self.message.channels = [1500, 1400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(self.message)
        self.rate.sleep()

    def stop(self):
        self.message.channels = [1500, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(self.message)
        self.rate.sleep()

    def kill_process_by_name(self, process_name):
        try:
            # Use pgrep to find process IDs by name
            pgrep_command = f"pgrep -f {process_name}"
            process_ids = subprocess.check_output(pgrep_command, shell=True).decode().split()

            if process_ids:
                # Use kill to terminate processes by PID
                kill_command = f"kill -9 {' '.join(process_ids)}"
                subprocess.run(kill_command, shell=True)
                print(f"Processes with name '{process_name}' terminated.")
            else:
                print(f"No processes found with name '{process_name}'.")

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
