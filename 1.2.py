import pyhula
import time
from hula_video import hula_video
from tflite_detector import tflite_detector
import cv2
import numpy as np
import threading

api = pyhula.UserApi()

def vid():
    global detected
    video = hula_video(hula_api=api,display=False)
    detector = tflite_detector(model="nytc-balanced-4Aug.tflite",label="label.txt")
    video.video_mode_on()
    while True:
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
            detected = True
            #cv2.imwrite(f"detected-pillar-{i}.jpg", frame)
        pos = api.get_coordinate()
        cv2.putText(frame, str(pos), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)

    cv2.destroyAllWindows()
    video.close()

def qr_align(id):
    for _ in range(10):
        api.single_fly_Qrcode_align(0, id)
        time.sleep(0.1)

if not api.connect():
    print('connect error')
else:
    print('success')

    threading.Thread(target=vid).start()
    time.sleep(10)
    api.single_fly_takeoff()
    api.single_fly_Qrcode_align(0,0)
    