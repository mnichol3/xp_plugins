"""
aircraft.py

Class providing methods to determine the state of an aircraft.

Notes
-----
* Unit conversions
    * 1 meter = 3.28084 ft
    * 1 m/s = 1.94384 kts
"""
from XPPython3 import xp


class Aircraft:

    DATAREFS = {
        "altitude_agl": "sim/flightmodel/position/y_agl",
        "altitude_msl": "sim/flightmodel/position/elevation",
        "eng_num": "sim/aircraft/engine/acf_num_engines",
        "eng_throttle": "sim/flightmodel/engine/ENGN_thro",
        "eng_running": "sim/flightmodel/engine/ENGN_running",
        "gear_fnrml": "sim/flightmodel/forces/fnrml_gear",
        "icao_type": "sim/aircraft/view/acf_ICAO",
        "latitude": "sim/flightmodel/position/latitude",
        "longitude": "sim/flightmodel/position/longitude",
        "parking_brake": "sim/flightmodel/controls/parkbrake",
        "speed_ground": "sim/flightmodel/position/groundspeed",
        "speed_ias": "sim/flightmodel/position/indicated_airspeed",
        "speed_vertical": "sim/flightmodel/position/vh_ind_fpm",
        "sun_pitch": "sim/graphics/scenery/sun_pitch_degrees",
        "wheels_on_ground": "sim/flightmodel/failures/onground_any",
    }

    @classmethod
    def altitude_agl(cls):
        """
        Altitude of aircraft above ground level (AGL), in meters.

        Dataref type: float

        Returns
        -------
        float
        """
        return xp.getDataf(cls.get_dataref("altitude_agl"))

    @classmethod
    def altitude_msl(cls):
        """
        Altitude of aircraft above mean sea level (MSL), in meters.

        Dataref type: float

        Returns
        -------
        float
        """
        return xp.getDataf(cls.get_dataref("altitude_msl"))

    @classmethod
    def get_dataref(cls, data_str):
        d_ref = cls.DATAREFS.get(data_str)
        return xp.findDataRef(d_ref)

    @classmethod
    def icao_type(cls):
        """
        Aircarft ICAO type code.

        Dataref type: byte[40]

        Returns
        -------
        str
        """
        return xp.getDatas(cls.get_dataref("icao_type"))

    @classmethod
    def is_engine_running(cls):
        """
        Check if at least one of the aircraft engines are running.

        Dataref types:
          * eng_num : int
          * eng_running : int

        Returns
        -------
        bool
        """
        is_running = False
        n_engines = xp.getDatai(cls.get_dataref("eng_num"))
        running = xp.getDatai(cls.get_dataref("eng_running"), n_engines)

        if 1 in running:
            is_running = True

        return is_running

    @classmethod
    def is_night(cls):
        return xp.getDataf(cls.dataRefs.get("sunPitch")) <= 6.0

    @classmethod
    def is_on_ground(cls):
        """
        Check if the aircraft is on the ground using the amount of upward
        force acting on the landing gear.

        Dataref type: float

        Returns
        -------
        bool
        """
        gear_force = xp.getDataf(cls.get_dataref("gear_fnrml"))
        return gear_force > 1

    @classmethod
    def is_parking_brake_set(cls):
        """
        Is the parking brake set?

        Dataref type: float

        Returns
        -------
        bool
        """
        return xp.getDataf(cls.get_dataref("parking_brake")) > 0.1

    @classmethod
    def is_stopped(cls):
        """
        Is the aircraft moving?

        Dataref type: float

        Returns
        -------
        bool
        """
        return xp.getDataf(cls.get_dataref("speed_ground")) < 1

    @classmethod
    def nearest_airport(cls):
        """
        Find the airport nearest to the aircraft's current position.

        Returns
        -------
        xppython3.NavAidInfo object
        """
        return cls.nearest_navaid(xp.Nav_Airport)

    @classmethod
    def nearest_navaid(cls, nav_type=None):
        """
        Find the navigational aid closest to the aircraft's current position.

        Parameters
        ----------
        nav_type : xppython3.XPLMNavType, optional
            Type of NavAid to find.

        Returns
        -------
        xppython3.NavAidInfo object
        """
        lon, lat, _, _ = cls.position()
        if nav_type:
            nav_ref = xp.findNavAid(lon=lon, lat=lat, navType=nav_type)
        else:
            nav_ref = xp.findNavAid(lon=lon, lat=lat)
        nav_aid = xp.getNavAidInfo(nav_ref)

        return nav_aid

    @classmethod
    def position(cls):
        """
        Get the aircraft's longitude, latitude, and altitudes in both AGL & MSL.

        Dataref types:
            * longitude: float
            * latitude: float
            * altitude_msl: float
            * altitude_agl: float

        Returns
        -------
        tuple
            * longitude, in decimal degrees
            * latitude, in decimal degrees
            * altitude MSL, in meters
            * altitude AGL, in meters
        """
        lon = xp.getDataf(cls.get_dataref("longitude"))
        lat = xp.getDataf(cls.get_dataref("latitude"))
        alt_msl = xp.getDataf(cls.get_dataref("altitude_msl"))
        alt_agl = xp.getDataf(cls.get_dataref("altitude_agl"))

        return lon, lat, alt_msl, alt_agl

    @classmethod
    def speed_ground(cls):
        """
        Aircraft's ground speed, in meters/second.

        Dataref type: float

        Returns
        -------
        float
        """
        return xp.getDataf(cls.get_dataref("speed_ground"))

    @classmethod
    def speed_ias(cls):
        """
        Aircraft's indicated airspeed.

        Dataref type: float

        Returns
        -------
        float
            Indicated airspeed, in knots (KIAS)
        """
        return xp.getDataf(cls.get_dataref("speed_ias"))

    @classmethod
    def speed_vertical(cls):
        """
        Aircraft's vertical speed, in feet/minute.

        Dataref type: float

        Returns
        -------
        float
        """
        return xp.getDataf(cls.get_dataref("speed_vertical"))

    @classmethod
    def throttle_setting(cls):
        """
        Engine throttle setting, as a percentage.

        Dataref type:
            * eng_num: int
            * eng_throttle: float

        Returns
        -------
        float
        """
        n_engines = xp.getDatai(cls.get_dataref("eng_num"))
        throttle_ratio = xp.getDataf(cls.get_dataref("eng_throttle", n_engines))
        throttle_avg = sum(throttle_ratio) / len(throttle_ratio)

        return throttle_avg
