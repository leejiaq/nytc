import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    api.single_fly_takeoff()
    api.single_fly_radius_around(50, {'r': 255, 'g': 255, 'b': 0, 'mode': 1})
    api.single_fly_radius_around(50, {'r': 0, 'g': 255, 'b': 255, 'mode': 1})
    api.single_fly_touchdown()