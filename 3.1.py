import pyhula
import time
from hula_video import hula_video
from onnxdetector import onnxdetector
import cv2
import numpy as np
import threading

uapi = pyhula.UserApi()
align = False
CM =1.25
detected = False

def correct():
    deviationdef_coords = [-uapi.get_coordinate()[0], -uapi.get_coordinate()[1]]
    uapi.single_fly_straight_flight(deviation_coords[0], deviation_coords[1], 0)

def align_to_tflite(obj):
    #uapi.single_fly_straight_flight()
    print("aligning", obj)
    correction = [0, 0]
    correction_step = 10
    if obj['x'] > 580:
        correction[0] = -1
    else:
        if obj['x'] < 700:
            correction[0] = 1
    if obj['y'] > 300:
        correction[1] = -1
    else:
        if obj['y'] < 420:
            correction[1] = 1
    print("correction to logo: ", str(correction))
    uapi.single_fly_straight_flight(correction[0]*correction_step, correction[1]*correction_step, 0)

def vid():
    global align
    global detected
    video = hula_video(hula_api=uapi,display=False)
    detector = onnxdetector(model="nytc2025-fast2.onnx",label="classes.txt")
    video.video_mode_on()
    while True:
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
            if align:
                align_to_tflite(object_found)
            detected = True
        else:
            obj_detected = None
            #cv2.imwrite(f"detected-pillar-{i}.jpg", frame)
        pos = uapi.get_coordinate()
        cv2.putText(frame, str(pos), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, "[" + str(pos[0] / CM) + ", " + str(pos[1] / CM) + ", " + str(pos[2] / CM) + "]", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)

    cv2.destroyAllWindows()
    video.close()

def qr_align(id):
    for _ in range(10):
        uapi.single_fly_Qrcode_align(0, id)
        time.sleep(0.1)

def align_to_logo(duration):
    global align
    align = True
    time.sleep(duration) 
    align = False
    time.sleep(2)

if not uapi.connect():
    print('connect error')
else:
    print('success')
    uapi.Plane_cmd_camera_angle(1,90)

    #5
    threading.Thread(target=vid).start()
    time.sleep(10) # video feed takes an abysmally long time to load
    uapi.single_fly_takeoff()
    uapi.single_fly_up(30)
    #uapi.single_fly_Qrcode_align(0, 0)
    #time.sleep(4)
    uapi.single_fly_forward(int(60/CM))
    uapi.single_fly_left(int(55/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #6
    uapi.single_fly_takeoff()
    uapi.single_fly_forward(int(40/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #1
    uapi.single_fly_takeoff()
    uapi.single_fly_right(int(40/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #2\
    uapi.single_fly_takeoff()
    uapi.single_fly_forward(int(60/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #7
    uapi.single_fly_takeoff()
    uapi.single_fly_left(int(55/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #3
    uapi.single_fly_takeoff()
    uapi.single_fly_right(int(120/CM))
    uapi.single_fly_back(int(60/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #4
    uapi.single_fly_takeoff()
    uapi.single_fly_back(int(60/CM))
    uapi.single_fly_touchdown()
    time.sleep(7)
    #8
    uapi.single_fly_takeoff()
    uapi.single_fly_left(int(65/CM))
    uapi.single_fly_touchdown()