import time
from pymavlink import mavutil

# Define the PWM value (in microseconds) for channel 1 (adjust as needed)
pwm_value = 1043

# Connect to the Pixhawk autopilot (adjust the connection string as needed)
# For example, you can use serial connection: '/dev/ttyACM0' for USB or 'udp:0.0.0.0:14550' for UDP.
# Replace it with the appropriate connection string.
connection_string = '/dev/serial/by-id/usb-ArduPilot_fmuv3_1B0047000C51373137353433-if00'  # Replace with your connection string

# Create a Mavlink connection
master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat()


try:
    # Arm the Pixhawk (assuming it's not already armed)
    master.arducopter_arm()
    # master.motors_armed_wait()

    # Send PWM command to channel 1
    # for i in range(10000):
    master.mav.rc_channels_override_send(
        target_system=master.target_system,  # Target system ID
        target_component=master.target_component,  # Target component ID
        chan1_raw=1944,
        chan2_raw=1492, 
        chan3_raw=1497, 
        chan4_raw=1494, 
        chan5_raw=982, 
        chan6_raw=1490, 
        chan7_raw=2006, 
        chan8_raw=2006
    )

    print(f"Sent PWM command (Channel 1) with PWM value {pwm_value}")

    # Allow some time for the command to take effect
    time.sleep(5)


except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the Mavlink connection
    master.close()
