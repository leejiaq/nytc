import pyhula
import time
from hula_video import hula_video
from onnxdetector import onnxdetector
import cv2
import numpy as np
import threading

uapi = pyhula.UserApi()

align = False
logo_target = ""

def correct(desired = [0, 0]):
    print("curr pos",uapi.get_coordinate())
    deviation_coords = [desired[0]-uapi.get_coordinate()[0], desired[1]-uapi.get_coordinate()[1]]
    print("correct", deviation_coords)
    uapi.single_fly_straight_flight(deviation_coords[0], deviation_coords[1], 0)

def align_to_tflite(obj): #xrange: 300-500 ; yrange: 200-350
    #uapi.single_fly_straight_flight()
    print("aligning", obj)
    correction = [0, 0]
    correction_step = 10
    if obj['x'] < 350:
        correction[0] = -1
    elif obj['x'] > 450:
        correction[0] = 1
    if obj['y'] < 200:
        correction[1] = 1
    elif obj['y'] > 350:
        correction[1] = -1
    print("correction to logo: ", str(correction))
    uapi.single_fly_straight_flight(correction[0]*correction_step, correction[1]*int(round(correction_step/2)), 0)
    correction = [0, 0]

def vid():
    global align
    global logo_target
    video = hula_video(hula_api=uapi,display=False)
    detector = onnxdetector(model="summit-fast2.onnx",label="summit.txt")
    video.video_mode_on()
    while True:
        frame = video.get_video()
        object_found, frame, all_object_found = detector.detect(frame)
        if object_found:
            print(F"Found object: {object_found}")
            print(f"OBJECTS: {all_object_found}")
            if align and logo_target in all_object_found:
                align_to_tflite(all_object_found[logo_target])
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

CM = 1.2

if not uapi.connect():
    print('connect error')
else:
    print('success')

    threading.Thread(target=vid).start()

    time.sleep(10)
    uapi.single_fly_takeoff() # MAKE SURE CAM ANGLE IS DOWN
    # SCAN ALL
    uapi.single_fly_Qrcode_align(0, 0)
    uapi.single_fly_up(int(200/CM))
    uapi.single_fly_forward(int(120/CM))
    time.sleep(2)
    uapi.single_fly_forward(int(70/CM))
    uapi.single_fly_back(int(60/CM))
    
    logo_target = "IMDA"
    align = True
    time.sleep(10)
    logo_target = ""
    align = False
    uapi.single_fly_down(int(50/CM))
    uapi.single_fly_touchdown()
    time.sleep(10)
    uapi.single_fly_takeoff()
    uapi.single_fly_up(int(50/CM))
    uapi.single_fly_straight_flight(int(55/CM),int(60/CM),0)
    logo_target = "GOOGLE"
    align = True
    time.sleep(10)
    logo_target = ""
    align = False
    uapi.single_fly_down(int(50/CM))
    uapi.single_fly_touchdown()

    time.sleep(10)
    uapi.single_fly_takeoff()
    uapi.single_fly_up(int(50/CM))
    uapi.single_fly_straight_flight(int(120/CM),int(120/CM),0)
    logo_target = "IMC"
    align = True
    time.sleep(10)
    logo_target = ""
    align = False
    uapi.single_fly_down(int(50/CM))
    uapi.single_fly_down(int(30/CM))
    uapi.single_fly_touchdown()

    time.sleep(10)
    uapi.single_fly_takeoff()
    uapi.single_fly_left(int(65/CM))
    uapi.single_fly_touchdown()
