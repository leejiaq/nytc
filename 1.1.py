import pyhula

CM = 1.2
api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    api.single_fly_takeoff()
    api.single_fly_Qrcode_align(0, 0)
    api.single_fly_down(20/CM)
    api.single_fly_forward(200 / CM) #subject to changes
    api.single_fly_up(200 /CM)
    api.single_fly_forward(120 / CM)
    api.single_fly_down(150/ CM)
    # time.sleep(2)
    api.single_fly_forward(200/ CM)
    api.single_fly_touchdown()