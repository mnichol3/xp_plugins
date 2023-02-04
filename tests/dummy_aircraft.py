"""
dummy_aircraft.py

Replicate the logbook aircraft class without requiring an X-Plane SDK dependency.
"""


class DummyAircraft(object):

    def __init__(self):
        self._altitude_agl = 0
        self._altitude_msl = 0
        self._eng_num = 0
        self._eng_throttle = 0
        self._eng_running = False
        self._gear_fnrml = 0
        self._icao_type = None
        self._latitude = 0
        self._longitude = 0
        self._parking_brake = False
        self._speed_ground = 0
        self._speed_ias = 0
        self._speed_vertical = 0
        self._wheels_on_ground = False

    def altitude_agl(self):
        return self._altitude_agl

    def set_altitude_agl(self, altitude):
        self._altitude_agl = altitude

    def altitude_msl(self):
        return self._altitude_msl

    def set_altitude_msl(self, altitude):
        self._altitude_msl = altitude

    def eng_num(self):
        return self._eng_num

    def set_eng_num(self, num):
        self._eng_num = num

    def is_engine_running(self):
        return self._eng_running

    def set_eng_running(self, running):
        self._eng_running = running

    def gear_fnrml(self):
        return self._gear_fnrml

    def set_gear_fnrml(self, force):
        self._gear_fnrml = force

    def icao_type(self):
        return self._icao_type

    def set_icao_type(self, icao):
        self._icao_type = icao

    def latitude(self):
        return self._latitude

    def set_latitude(self, lat_val):
        self._latitude = lat_val

    def longitude(self):
        return self._longitude

    def set_longitude(self, lon_val):
        self._longitude = lon_val

    def is_parking_brake_set(self):
        return self._parking_brake

    def set_parking_brake(self, is_set):
        self._parking_brake = is_set

    def speed_ground(self):
        return self._speed_ground

    def is_stopped(self):
        return self._speed_ground == 0

    def set_speed_ground(self, speed):
        self._speed_ground = speed

    def speed_ias(self):
        return self._speed_ias

    def set_speed_ias(self, speed):
        self._speed_ias = speed

    def speed_vertical(self):
        return self._speed_vertical

    def set_speed_vertical(self, speed):
        self._speed_vertical = speed

    def is_on_ground(self):
        return self._wheels_on_ground

    def set_wheels_on_ground(self, on_ground):
        self._wheels_on_ground = on_ground

