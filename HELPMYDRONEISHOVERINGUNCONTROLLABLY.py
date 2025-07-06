import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")
    api.single_fly_touchdown()