import pyhula
import time
from hula_video import hula_video
from tflite_detector import tflite_detector
import cv2
import numpy as np
import threading

uapi = pyhula.UserApi()

detected = False

def correct():
    deviation_coords = [-uapi.get_coordinate()[0], -uapi.get_coordinate()[1]]
    uapi.single_fly_straight_flight(deviation_coords[0], deviation_coords[1], 0)

def vid():
    global detected
    video = hula_video(hula_api=uapi,display=False)
    detector = tflite_detector(model="nytc-balanced-4Aug.tflite",label="label.txt")
    video.video_mode_on()
    while True:
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
            detected = True
            #cv2.imwrite(f"detected-pillar-{i}.jpg", frame)
        pos = uapi.get_coordinate()
        cv2.putText(frame, str(pos), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)

    cv2.destroyAllWindows()
    video.close()

def qr_align(id):
    for _ in range(10):
        uapi.single_fly_Qrcode_align(0, id)
        time.sleep(0.1)

if not uapi.connect():
    print('connect error')
else:
    print('success')

    threading.Thread(target=vid).start()

#5
uapi.single_fly_takeoff()
uapi.single_fly_Qrcode_align(0, 0)
time.sleep(4)
uapi.single_fly_forward(70)
time.sleep(3)
uapi.single_fly_left(55)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#6
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_forward(60)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#1
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_right(55)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#2\
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_forward(60)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#7
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_left(55)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#3
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_right(120)
time.sleep(3)
uapi.single_fly_back(60)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#4
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_back(60)
time.sleep(3)
uapi.single_fly_touchdown()
time.sleep(7)
#8
uapi.single_fly_takeoff()
correct()
time.sleep(3)
uapi.single_fly_left(65)
time.sleep(3)
uapi.single_fly_touchdown()