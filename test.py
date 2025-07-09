import pyhula
import time

CM = 1.2

api = pyhula.UserApi()

def correct(desired = [0, 0]):
    print("curr pos",api.get_coordinate())
    deviation_coords = [desired[0]-api.get_coordinate()[0], desired[1]-api.get_coordinate()[1]]
    print("correct", deviation_coords)
    api.single_fly_straight_flight(deviation_coords[0], deviation_coords[1], 0)
if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")
    api.single_fly_takeoff()
    api.single_fly_forward(int(100 / CM))
    time.sleep(2)
    correct([0, int(100 / CM)])
    api.single_fly_down(int(50/CM))
    correct([0, int(100 / CM)])
    api.single_fly_touchdown()