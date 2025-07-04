import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    bat = api.get_battery()
    print(bat)

    if bat < 50:
        api.single_fly_lamplight(0, 0, 255, 5, 1)