import pyhula
import time
from hula_video import hula_video
from onnxdetector import onnxdetector
import cv2
import numpy as np
import threading

uapi = pyhula.UserApi()

CM = 1.2

def vid():
    video = hula_video(hula_api=uapi, display=False)
    detector = onnxdetector(model="ball-fast2.onnx", label="balls.txt")
    video.video_mode_on()
    while True:
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
        pos = uapi.get_coordinate()
        cv2.putText(frame, str(pos), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, "[" + str(pos[0] / CM) + ", " + str(pos[1] / CM) + ", " + str(pos[2] / CM) + "]", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)

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
