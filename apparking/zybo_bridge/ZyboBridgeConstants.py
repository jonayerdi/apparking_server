#!/usr/bin/python

MESSAGE_TYPES_IN = {
    'ServerIdRequest': 0x10101010,
    'ParkingIdUpdate': 0x11111111,
    'ParkingSpotUpdate': 0x12121212,
    'ImageUpdate': 0x13131313
}

MESSAGE_TYPES_OUT = {
    'ParkingSpotUpdate': 0x22222222,
}

PARKING_SPOT_STATES = {
    0 : 'Unknown',
    1 : 'Freeing',
    2 : 'Free',
    3 : 'Taking',
    4 : 'Taken'
}

PARKING_SPOT_FORCED = {
    0 : False,
    1 : True
}
