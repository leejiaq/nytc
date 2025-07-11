import pyhula
import threading

CM = 1.3
api = pyhula.UserApi()

def coords():
    while True: print(api.get_coordinate())

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    thread = threading.Thread(target=coords).start()

    api.single_fly_takeoff()
    api.single_fly_Qrcode_align(0, 0)
    api.single_fly_down(int(20/CM))
    api.single_fly_forward(int(215 / CM)) #subject to changes
    api.single_fly_up(int(300 /CM))
    api.single_fly_forward(int(150 / CM))
    api.single_fly_down(int(200/ CM))
    # time.sleep(2)
    api.single_fly_forward(int(200/ CM))
    api.single_fly_touchdown()