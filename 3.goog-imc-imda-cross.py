import pyhula
import time
from hula_video import hula_video
from onnxdetector import onnxdetector
import cv2
import numpy as np
import threading

CM = 1.15
api = pyhula.UserApi()

def vid():
    video = hula_video(hula_api=api,display=False)
    detector = onnxdetector(model="nytc2025-fast2.onnx",label="classes.txt")
    video.video_mode_on()
    while True:
        frame = video.get_video()
        object_found, frame, all_object_found = detector.detect(frame)
        if object_found:
            print(F"Found object: {object_found}")
            print(f"OBJECTS: {all_object_found}")
        pos = api.get_coordinate()
        cv2.putText(frame, str(pos), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, "[" + str(pos[0] / CM) + ", " + str(pos[1] / CM) + ", " + str(pos[2] / CM) + "]", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)

def coords():
    while True: print(api.get_coordinate())

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    thread = threading.Thread(target=vid).start()

    time.sleep(5)

    api.single_fly_takeoff()
    api.single_fly_up(int(200/CM))
    # api.single_fly_Qrcode_align(0,0)
    api.single_fly_forward(int(120/CM))
    api.single_fly_forward(int(70/CM))
    api.single_fly_Qrcode_align(0,0)
    api.single_fly_touchdown()
    time.sleep(12)
    api.single_fly_takeoff()
    api.single_fly_up(int(30/CM))
    api.single_fly_Qrcode_align(0,0)
    api.single_fly_back(int(120/CM))
    api.single_fly_right(int(90/CM))
    api.single_fly_Qrcode_align(0,2)
    api.single_fly_touchdown()
    time.sleep(12)
    api.single_fly_takeoff()
    api.single_fly_up(int(120/CM))
    api.single_fly_Qrcode_align(0,2)
    api.single_fly_left(int(50/CM))
    api.single_fly_forward(int(50/CM))
    api.single_fly_Qrcode_align(0,1)
    api.single_fly_touchdown()
    time.sleep(12)
    api.single_fly_takeoff()
    api.single_fly_Qrcode_align(0,1)
    api.single_fly_back(int(45/CM))
    api.single_fly_right(int(20/CM))
    api.single_fly_touchdown()
