import pyhula
import time
from hula_video import hula_video
from tflite_detector import tflite_detector
import cv2
import numpy as np
import threading

uapi = pyhula.UserApi()

CM = 1.2

def detect_ball(frame, Lcol, Ucol, col):
    # Define HSV range for red color
    
    # Convert frame to HSV color  space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for blue color
    mask_col = cv2.inRange(hsv, Lcol, Ucol)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask_col, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Draw the detected contour and center
        cv2.drawContours(frame, [largest_contour], -1, col, 3)  # Blue color
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Green dot at center #00A37D
        
        return center_x, center_y, frame
    else:
        return None, None, frame

Lred = np.array([0, 50, 70])
Ured = np.array([30, 255, 255])

Lblue = np.array([85, 150, 70])
Ublue = np.array([160, 255, 255])

Lyell = np.array([20, 150, 70])
Uyell = np.array([58, 255, 255 ])

def vid():
    video = hula_video(hula_api=uapi,display=False)
    video.video_mode_on()

    while True:
        frame = video.get_video()
        redball = detect_ball(frame, Lred, Ured, (0, 0,255))
        redballs = detect_ball(frame, Lred, Ured, (0, 0,255))
        blueball = detect_ball(frame, Lblue, Ublue, (255, 0, 0))
        yellball = detect_ball(frame, Lyell, Uyell, (0, 255, 255))
        print(redball, blueball, yellball)
        pos = uapi.get_coordinate()
        cv2.putText(frame, str(pos), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, "[" + str(pos[0] / CM) + ", " + str(pos[1] / CM) + ", " + str(pos[2] / CM) + "]", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("NASS", frame)
        cv2.waitKey(1)
        #break       
        time.sleep(0.03)
    
    cv2.destroyAllWindows()
    video.close()

if not uapi.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")
    threading.Thread(target=vid).start()
    time.sleep(5) # abysmal video loading time

    uapi.single_fly_takeoff()
    uapi.single_fly_up(int(50 / CM))
    time.sleep(2)
    uapi.single_fly_left(int(80 / CM))
    uapi.single_fly_forward(int(75 / CM))
    uapi.single_fly_down(int(40 / CM))
    uapi.single_fly_up(int(40 / CM))
    uapi.single_fly_back(int(65 / CM))

    uapi.single_fly_right(int(80 / CM))
    uapi.single_fly_right(int(80 / CM))
    uapi.single_fly_forward(int(75 / CM))
    uapi.single_fly_down(int(40 / CM))
    uapi.single_fly_up(int(40 / CM))
    uapi.single_fly_back(int(65 / CM))

    uapi.single_fly_left(int(80 / CM))
    uapi.single_fly_forward(int(50 / CM))
    uapi.single_fly_down(int(40 / CM))
    uapi.single_fly_up(int(40 / CM))
    uapi.single_fly_back(int(65 / CM))

    uapi.single_fly_touchdown()
