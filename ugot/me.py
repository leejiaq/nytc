from ugot import ugot
import cv2
import numpy as np
import time

got = ugot.UGOT()

SPEED = 15
SIDE_SPEED = 10
def forward():
    got.mecanum_move_speed_times(0, 30, 50, 1) # 1 is backward
def backward():
    got.mecanum_move_speed_times(1, 30, 50, 1)
def right(n):
    got.mecanum_turn_speed_times(3, 90, n, 2)
def left():
    got.mecanum_turn_speed_times(2, 45, 90, 2) # 3 is right
def pick_up():
    got.mechanical_clamp_release()
    time.sleep(1)
    got.mechanical_joint_control(0,0,0, 500)
    time.sleep(1)
    got.mechanical_join_control(45,0,0,500) # can change numbers
    time.sleep(1)
    got.mechanical_clamp_close()

    if got.get_apriltag_total_info():
        got.screen_display_background(3) # red background
        got.mechanical_claim_release()
        return False
    else:
        got.screen_display_background(6) #green background
        return True
def seek_qrcode():
    attempts = 2 
    while True:
            frame = got.read_camera_data()
            if not frame:
                break
            frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)

            tags = got.get_apriltag_total_info()
            if tags:
                _, cx, cy, h, w, _, distance,*_= tag [0]
                if distance < 0.19:
                    if not pick_up():
                        attempts += 1
                    else:
                        break
                if attempts > 3:
                        break #too many failures, give up
                # back backwards before retrying
                got.mecanum_move_speed_times(1,30,20,1)
                if cx > 340:
                    got.mecanum_move_xyz(SIDE_SPEED, SPEED, 0)
                elif cx < 300:
                    got.mecanum_move_xyz(-SIDE_SPEED,SPEED,0)
                else:
                    got.mecanum_move_xyz(0,SPEED,0)
                
                x1,y1 = int(cx - w/2), int(cy-h/2)
                x2,y2 = int(cx + w/2), int(cy + h/2)
                cv2.rectangle(frame, (x1,y1),(x2,y2)(0, 255, 0), 2)
            else:
                distance = cx = "NaN"
                got.mecanum_stop()
            
def main():
   """Initialize systems, perform search-and-fetch routine, then return home."""
   got.initialize('192.168.88.1')           # Connect to robot over network
   got.open_camera()                         # Start video stream
   got.load_models(['apriltag_qrcode'])      # Enable AprilTag/QR detection
   # Pre-position arm and open gripper
   got.mechanical_joint_control(0, 0, -20, 500)
   got.mechanical_clamp_release()
   got.screen_clear()                        # Clear any previous display


   go_there()    # Navigate to search area
   seek_qrcode()   # Locate tag, approach, and pick up
   go_back()     # Return and drop object


if __name__ == "__main__":
   main()