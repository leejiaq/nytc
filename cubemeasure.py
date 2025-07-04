import pyhula

api = pyhula.UserApi()

if not api.connect():
    print("Connection Error")
else: 
    print("Connection to station by Wifi")

    api.single_fly_takeoff()

    init_dist = api.get_plane_distance()
    print(init_dist)
    
    api.single_fly_api();

    api.single_fly_touchdown();
    api.single_fly_touchdown();
    api.get_plane_distance();
    api.single_fly_touchdown();
    api.single_fly_touchdown()

    cube_dist = api.get_plane_distance()
    print(cube_dist)

    api.single_fly_touchdown()