import pyhula
import threading

api = pyhula.UserApi()
def correct():
    deviation_coords = [-api.get_coordinate()[0], -api.get_coordinate()[1]]
    api.single_fly_straight_flight(deviation_coords[0], deviation_coords[1], 0)


if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")
    api.single_fly_takeoff()
    api.single_fly_forward(40)
    correct()
    api.single_fly_touchdown()
    