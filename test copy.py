import pyhula
import threading
import time

api = pyhula.UserApi()

def coords():
    while True: print(api.get_coordinate())

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")
    threading.Thread(target=coords).start()
    api.single_fly_takeoff()
    api.single_fly_forward(40)
    time.sleep(6)
    api.single_fly_touchdown()