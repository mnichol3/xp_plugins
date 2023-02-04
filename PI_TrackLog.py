"""
PI_TrackLog.py

Simple aircraft track logger.

M Nicholson
21 NOV 2022
"""
from datetime import datetime, timedelta

import XPLMProcessing

from XPPython3 import xp


class Util:

    @staticmethod
    def ms_2_mph(ms):
        """
        Convert a velocity in meters/second to miles/hour.

        Parameters
        ----------
        ms : float
            Meters/second value.

        Returns
        -------
        float
        """
        return ms * 2.23694

    @staticmethod
    def m_2_ft(m):
        """
        Convert a distance in meters to feet.

        Parameters
        ----------
        m : float
            Distance, in meters.

        Returns
        -------
        float
        """
        return m * 3.28084


class PythonInterface:
    def XPluginStart(self):
        self.Name = "AircraftTracker v1.0"
        self.Sig = "mnichol3.AircraftTracker1"
        self.Desc = "Record aircraft position and altitude."

        self.dataRefs = {
            "total_flight_time": "sim/time/total_flight_time_sec",
            "acft_type": "sim/aircraft/view/currPosition",
            "latitude": "sim/flightmodel/position/latitude",
            "longitude": "sim/flightmodel/position/longitude",
            "elevation": "sim/flightmodel/position/elevation",
            "gnd_speed": "sim/flightmodel/position/groundspeed",
            "air_speed": "sim/flightmodel/position/indicated_airspeed",
            "vert_speed": "sim/flightmodel/position/vh_ind_fpm",
            "zulu_time": "sim/time/zulu_time_sec"
        }

        self.enabled = True
        self.timeStamp = datetime.now().strftime("%Y_%m_%d-%H%M")
        self.acftType = self.getAircraftType()
        self.trackFilename = self.parseTrackFilename()

        # Set flight loop params & instantiate flight loop callback
        self.trackRate = 15  # Seconds
        self.loopSkip = -10  # Negative to indicate loops to skip

        self.floop = self.floopCallback
        XPLMProcessing.XPLMRegisterFlightLoopCallback(self.floop, -1, 0)

        #mySubMenuItem = xp.appendMenuItem(xp.findPluginsMenu(), "Python - Sim Data 1", 0)
        #self.myMenu = xp.createMenu("Sim Data", xp.findPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCallback, 0)
        #xp.appendMenuItem(self.myMenu, "Decrement Nav1", -1000)
        #xp.appendMenuItem(self.myMenu, "Increment Nav1", +1000)
        #self.DataRef = xp.findDataRef("sim/cockpit/radios/nav1_freq_hz")

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        xp.destroyMenu(self.myMenu)
        XPLMProcessing.XPLMUnregisterFlightLoopCallback(self.floop, 0)

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def floopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        """
        Flight loop callback method.

        Parameters
        ----------
        elapsedMe : int?
            Wall time since last callback.
        elapsedSim : int?
            Wall time since any flight loop was dispatched.
        counter : int?
            Monotonically increasing counter, bumped once per flight loop
            dispatch from the sim.
        refcon : idk
            Ptr constant from callback registration.

        Returns
        -------
        int
            Determines next call:
                * 0 -> receiving callbacks
                * Positive int -> how many seconds until next callback
                * Negative int -> how many loops must pass until next callback.
        """
        if self.enabled:
            #fltTime = xp.getDatai(self.dataRefs.get("total_flight_time"))
            #if fltTime % self.trackRate == 0:
            # Dont need the above time check if we're returning the positive
            # trackRate parameter
            currPosition = self.getPosition()
            self.writePosition(currPosition)

        return self.trackRate

    def getAircraftType(self):
        return xp.getDatai(self.dataRefs.get("acft_type"))

    def getSimTime(self):
        """
        Get the sim zulu time.

        Returns
        -------
        str
            Zulu time. Format: HH:MM:SS
        """
        now = xp.getDatai(self.dataRefs.get("zulu_time"))
        zuluTime = str(timedelta(now)).zfill(8)  # Add padding 0 if hr < 10

        return zuluTime

    def getPosition(self):
        """
        Get aircraft position.

        Returns
        -------
        dict

        DataRefs
        ---------
        * Lat & lon: decimal degrees
        * Elevation: Elevation of acft above MSL, in meters.
        * Ground speed: meters/sec
        * IAS: knots
        * Vertical speed: fpm
        """
        position = {
            "currTime": self.getSimTime(),
            "currLat": xp.getDatai(self.dataRefs.get("latitude")),
            "currLon": xp.getDatai(self.dataRefs.get("longitude")),
            "currEle": xp.getDatai(self.dataRefs.get("elevation")),
            "currGndSpeed": xp.getDatai(self.dataRefs.get("gnd_speed")),
            "currAirSpeed": xp.getDatai(self.dataRefs.get("air_speed")),
            "currVerSpeed": xp.getDatai(self.dataRefs.get("vert_speed")),
        }
        # Convert meter units to imperial
        footEle = Util.m_2_ft(position["currEle"])
        mphGndSpeed = Util.ms_2_mph(position["currGndSpeed"])
        position.update({"currEle": footEle, "currGndSpeed": mphGndSpeed})

        return position

    def parseTrackFilename(self):
        """
        Parse the name of the track log file to write.

        Returns
        -------
        str
        """
        fname = f'TrackLogFile-{self.timeStamp}-{self.acftType}.txt'
        return fname

    def writePosition(self, position):
        """
        Write latest position to file.

        Parameters
        ----------
        position : dict
            Position information.

        Returns
        -------

        """

