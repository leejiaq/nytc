import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    api.single_fly_takeoff()

    api.single_fly_forward(50)

    if api.single_fly_recognition_Qrcode(0, 0)["result"]:
        api.single_fly_lamplight(0, 0, 255, 5, 32)

        api.single_fly_Qrcode_align(0, 0)

    api.single_fly_touchdown()