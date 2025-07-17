import pyhula
import threading
import time

CM = 1.15
api = pyhula.UserApi()

def coords():
    while True: print(api.get_coordinate())

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    #thread = threading.Thread(target=coords).start()

    api.single_fly_takeoff()
    # api.single_fly_down(50)
    # api.single_fly_Qrcode_align(0,0)
    # api.single_fly_up(50)
    api.single_fly_down(int(20/CM))
    api.single_fly_Qrcode_align(0,0)
    api.single_fly_Line_walking(0, int(215 / CM), 0)
    api.single_fly_up(int(200 /CM))
    api.single_fly_Line_walking(0, int(150 / CM), 0)
    api.single_fly_down(int(200/ CM))
    time.sleep(2)
    api.single_fly_Line_walking(0, int(200 / CM), 0)
    api.single_fly_down(50)
    time.sleep(5)
    api.single_fly_touchdown()
