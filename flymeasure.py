import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    api.single_fly_takeoff()
    api.single_fly_forward(50)
    
    print(api.get_plane_distance())

    api.single_fly_touchdown()