from ugot import ugot
import cv2
import numpy as np
import time

got = ugot.UGOT()

SPEED = 100
SIDE_SPEED = 100
ANGULAR_SPEED = 90
MAX_ATTEMPTS = 5
control = 1

def forward(n):
    got.mecanum_move_speed_times(0, SPEED, n, 1) # 1 is backward
    got.mecanum_turn_speed_times(3,ANGULAR_SPEED,control,2)
def backward(n):
    got.mecanum_move_speed_times(1, SPEED, n, 1)
    got.mecanum_turn_speed_times(3,ANGULAR_SPEED,control,2)
def turn_right(angle):
    got.mecanum_turn_speed_times(3, ANGULAR_SPEED, angle, 2)
def turn_left(angle):
    got.mecanum_turn_speed_times(2, ANGULAR_SPEED, angle, 2) # 3 is right
def pan_right(n):
    for _ in range(n): got.mecanum_move_xyz(SIDE_SPEED, 0, 0)
def pan_left(n):
    for _ in range(n): got.mecanum_move_xyz(-SIDE_SPEED, 0, 0)

def pick_up():
    """
    Attempt to pick up an object directly beneath the gripper.
    Returns True on successful grasp (no AprilTag detected after closing),
    False otherwise.
    """
    # Halt all wheel motion
    got.mecanum_stop()
    # Lower the arm to approach object
    got.mechanical_joint_control(0, -10, -40, 500)
    time.sleep(1)
    # Close gripper on object
    got.mechanical_clamp_close()
    time.sleep(1)
    # Lift the arm back up
    got.mechanical_joint_control(0, 30, 30, 500)
    time.sleep(1)


    # Verify pick by checking for tag visibility
    if got.get_apriltag_total_info():
        # Tag still visible -> failed grasp
        got.screen_display_background(3)  # red background
        got.mechanical_clamp_release()     # drop object
        return False
    else:
        # Tag no longer visible -> successful grasp
        got.screen_display_background(6)  # green background
        return True
    
def unpick_down():
    """
    it unpickup so unpick down
    """

    got.mecanum_stop()
    got.mechanical_joint_control(0, -10, -40, 500)
    time.sleep(1)
    got.mechanical_clamp_release()
    time.sleep(2)
    got.mechanical_joint_control(0, 30, 30, 500)

def seek_qrcode(speed):
    """
    Continuously capture frames, detect AprilTags, align and approach them,
    and attempt pickup when within threshold distance.
    """
    attempts = 0
    close_to_tag = False
    while True:
        # Read raw JPEG from camera and decode to OpenCV image
        frame = got.read_camera_data()
        if not frame:
            break
        frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)


        # Retrieve all detected AprilTags
        tags = got.get_apriltag_total_info()
        if tags:
            # Unpack properties of the first detection
            _, cx, cy, h, w, _, distance, *_ = tags[0]


            # If within pickup range, try grasp
            if distance < 0.25: close_to_tag = True
            if distance < 0.18 or (distance == "NaN" and close_to_tag):
                close_to_tag = False
                if not pick_up():
                    attempts += 1
                else:
                    break  # success, exit loop


                if attempts > MAX_ATTEMPTS:
                    break  # too many failures, give up


                # Back up slightly before retrying
                got.mecanum_move_speed_times(1, 30, 20, 1)


            # Strafe to center the tag in camera FOV
            if cx > 340:
                got.mecanum_move_xyz(speed, speed, 0)
            elif cx < 300:
                got.mecanum_move_xyz(-speed, speed, 0)
            else:
                got.mecanum_move_xyz(0, speed, 0)


            # Draw detection bounding box
            x1, y1 = int(cx - w/2), int(cy - h/2)
            x2, y2 = int(cx + w/2), int(cy + h/2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


        else:
            # No tag detected: stop movement and mark values as NaN
            distance = cx = "NaN"
            #got.mecanum_stop()

        # Overlay distance and center-x information on frame
        cv2.putText(
            frame,
            f'Distance: {distance} {close_to_tag} | Center X: {cx} / 320',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # Display processed image; exit on 'q' keypress
        cv2.imshow('Image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Clean up on exit
    got.mecanum_stop()
    cv2.destroyAllWindows()


def main():
    """Initialize systems, perform search-and-fetch routine, then return home."""
    got.initialize('192.168.88.1')             # Connect to robot over network
    got.open_camera()                              # Start video stream
    got.load_models(['apriltag_qrcode'])        # Enable AprilTag/QR detection
    # Pre-position arm and open gripper
    got.mechanical_joint_control(0, 0, -20, 500)
    got.mechanical_clamp_release()
    got.screen_clear()                             # Clear any previous display


if __name__ == "__main__":
    main()
    turn_left(90)
    forward(85)
    turn_right(90)
    forward(200)
    turn_left(90)
    forward(60)
    turn_right(90)
    forward(165)
    turn_right(90)
    seek_qrcode(10)
    backward(60)
    turn_right(90)
    forward(165)
    turn_left(90)
    forward(60)
    turn_right(90)
    forward(200)
    turn_left(90)
    forward(20)
    unpick_down()
    backward(20)
    turn_left(90)
    forward(190)
    turn_left(90)
    forward(70)
    turn_left(90)
    seek_qrcode(10)
    backward(190)
    turn_left(90)
    forward(70)
    turn_right(90)
    forward(190)
    turn_left(90)
    unpick_down()
