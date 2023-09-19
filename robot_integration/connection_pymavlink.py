# hello
from pymavlink import mavutil
from pprint import pprint
import time
# Create the connection
master = mavutil.mavlink_connection('/dev/serial/by-id/usb-ArduPilot_fmuv3_1B0047000C51373137353433-if00')
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Create a function to send RC values
# More information about Joystick channels
# here: https://www.ardusub.com/operators-manual/rc-input-and-output.html#rc-inputs
def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(8)]
    rc_channel_values[channel_id - 1] = pwm
    # print(rc_channel_values)

    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.


# # Set some roll


while True:
    try:
        a = master.recv_match().to_dict()
        # pprint(a)
        # pprint(a)
        for i in range(1,19):

            print(str(i),'', a[f"chan{i}_raw"], end="|")
        print(end='\n')


        # if a["mavpackettype"] == "RC_CHANNELS":
        #     print("pierwszy ",a["chan1_raw"],"trzeci ",a["chan3_raw"]) 
        #     pass
    except:
        pass
# The camera pwm value sets the servo speed of a sweep from the current angle to
#  the min/max camera angle. It does not set the servo position.
# Set camera tilt to 45º (max) with full speed