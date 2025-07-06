import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    api.single_fly_takeoff()
    api.single_fly_Qrcode_align(0, 0)
    api.single_fly_down(20)
    api.single_fly_forward(85) #subject to changes
    api.single_fly_up(150)
    api.single_fly_forward(129)
    api.single_fly_down(100)
    api.single_fly_forward(200)
    api.single_fly_touchdown()