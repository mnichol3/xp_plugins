"""
Relevant DataRefs
-----------------
sim/flightmodel/engine/
    * ENGN_thro : Throttle (per engine) as set by user, 0 = idle, 1 = max; float
    * ENGN_running : Engine on and using fuel; bool
sim/flightmodel/controls/
    * parkbrake : Parking Brake, 1 = max; float
sim/flightmodel/position/
    * groundspeed : Acft ground speed, in meters/sec; float
    * vh_ind_fpm : vertical velocity in feet per second; float
sim/time/
    * zulu_time_sec : Zulu time, in seconds; float
    * local_time_sec : local time, in seconds; float
sim/graphics/scenery/
    * sun_pitch_degrees : sun pitch from flat in OGL coordinates, in degrees; float
sim/flightmodel/failures/
    * onground_any : User Aircraft is on the ground when this is set to 1; int
"""
from datetime import datetime, timezone
from pathlib import Path

from XPPython3 import xp

from logbook.aircraft import Aircraft
from logbook.flight_log import FlightLog
from logbook.flight_phase import FlightPhase


class PythonInterface:

    def XPluginStart(self):
        self.Name = "Logbook v1.0"
        self.Sig = "xppython3.PI_Logbook"
        self.Desc = "A simple logbook."

        # The values of these variables can be changed to write the file
        # wherever you'd like.
        output_dir = Path(__file__).parent.joinpath('logbook')
        output_file = 'logbook.txt'

        # This variable determines whether to use sim time or system time.
        # Set to "sim" to sim time, or "system" to use system time.
        self.time_src = "sim"

        self.output_file = output_dir.joinpath(output_file)
        self.flight_log = FlightLog()
        self.flight_phase = FlightPhase(Aircraft)

        self.flight_log.aircraft_type = Aircraft.icao_type()
        self.flight_log.origin = Aircraft.nearest_airport()
        # TODO: try to get origin/dest from FMS

        # Register our FL callback with initial callback freq of 1 second
        xp.registerFlightLoopCallback(self.FlightLoopCallback, 1.0, 0)

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        # Unregister the callback
        xp.unregisterFlightLoopCallback(self.FlightLoopCallback, 0)

        # Close the file
        #self.output_file.close()
        self.flight_log.write(self.output_file)

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        # TODO: simple GUI to enable/disable
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        # TODO: Case for touch-n-go

        # Return 1.0 to indicate that we want to be called again in 1 second.
        return 1.0

    def get_real_time(self):
        """
        Get the current real-world time, as the total number of seconds
        since midnight.

        Returns
        -------
        int, int
            Local and zulu time
        """
        time_local = datetime.now().time()
        time_local = self.total_time(time_local)

        time_zulu = datetime.now(tz=timezone.utc).time()
        time_zulu = self.total_time(time_zulu)

        return time_local, time_zulu

    def get_sim_time(self):
        """
        Get the current time of day in the simulator, as the total number
        of seconds since midnight.

        Returns
        -------
        int, int
            Local and zulu time
        """
        time_local = xp.getDatai("sim/time/local_time_sec")
        time_zulu = xp.getDatai("sim/time/zulu_time_sec")

        return time_local, time_zulu

    @staticmethod
    def total_time(dt):
        """
        Return the time from a Datetime object as the total number of seconds
        since midnight.

        Parameters
        ----------
        dt : Datetime object

        Returns
        -------
        int
        """
        total = dt.hour * 3600
        total += dt.minute * 60
        total += dt.second

        return total
