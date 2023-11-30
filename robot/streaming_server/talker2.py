#!/usr/bin/env python3
# Software License Agreement (BSD License)

import rospy
from std_msgs.msg import String
from mavros_msgs.msg import OverrideRCIn

class RobotController:
    # Map commands to corresponding methods
    # command_handlers = {
    #     'establish_connection': 'establish_connection',
    #     'forward': 'move_forward',
    #     'backward': 'move_backward',
    #     'left': 'move_left',
    #     'right': 'move_right',
    #     'stop': 'stop',
    #     'lose_connection': 'lose_connection',
    # }

    def __init__(self):
        pass

    def establish_connection(self):
        # probably needs to be changed when we have a connection to the robot
        self.pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
        self.init_node = rospy.init_node('talker', anonymous=True)
        self.message = OverrideRCIn()
        self.message.channels = [1800, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rate = rospy.Rate(10)  # 10hz

    def move_forward(self):
        self.message.channels = [1800, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(self.message)
        self.rate.sleep()

    def move_left(self):
        # Add logic for moving left
        print("ROS")
        pass

    def move_right(self):
        # Add logic for moving right
        pass

    def move_backward(self):
        # Add logic for moving backward
        pass

    def stop(self):
        # Add logic for moving backward
        pass

    def lose_connection(self):
        # Add logic for stopping
        pass

    # def execute_command(self, command):
    #     handler = self.command_handlers.get(command.lower())
    #     if handler:
    #         handler()
    #     else:
    #         print(f"Unknown command: {command}")

# if __name__ == '__main__':
#     try:
#         robot_controller = RobotController()
#         robot_controller.establish_connection()

#         # Example usage of the execute_command method
#         # robot_controller.stop()

#     except rospy.ROSInterruptException:
#         pass
